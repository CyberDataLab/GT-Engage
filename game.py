# ============================================================
# game.py — CPD-GAME v3 Engine (Signaling + Bayes + Hypergames)
# ============================================================

from attacker import Attacker
from defender import Defender
from environment import Environment
from signals import generate_signals, update_attacker_belief
from mitre_effects import MITRE_ENV_EFFECTS, MITRE_META
from utils import clip01


class Game:
    """
    Dynamic game involving:
      - Attacker: expected_utility + hypergame + signals
      - Defender: MITRE + fatigue + lightweight learning + hypergame
      - Environment: S1, S2, sweetness, C, rho, asset_value_if_real
      - Signals -> beliefs -> actions -> utility
    """

    def __init__(self, attacker_type, defender_type, env_init, T: int = 5):
        # ===========================
        #   ATTACKER
        # ===========================
        self.attacker = Attacker(
            attacker_id=int(attacker_type["id"]),
            mot=attacker_type["mot"],
            skill=attacker_type["skill"],
            knowl=attacker_type["knowl"],
            auto=attacker_type["auto"],
            att=attacker_type["att"],
            risk=attacker_type["risk"],
            affil=attacker_type["affil"],
            obj=attacker_type["obj"],
        )

        # ===========================
        #   DEFENDER
        # ===========================
        self.defender = Defender(
            defender_id=int(defender_type["id"]),
            w_eng=float(defender_type["w_eng"]),
            w_info=float(defender_type["w_info"]),
            w_prot=float(defender_type["w_prot"]),
            w_cost=float(defender_type["w_cost"]),
            res=int(defender_type["res"]),
            riskD=float(defender_type["riskD"]),
        )

        # ===========================
        #   ENVIRONMENT
        # ===========================
        S1 = float(env_init["S1"])
        S2 = float(env_init["S2"])
        Sweetness = float(env_init["Sweetness"])
        C = float(env_init["C"])

        # ==== ROBUST RHO ====
        # If "rho" does not exist, or is None, or is empty, or "None", automatically derive rho
        raw_rho = env_init.get("rho", None)

        if raw_rho is None or raw_rho == "" or str(raw_rho).lower() == "none":
            rho = S1 * Sweetness
        else:
            try:
                rho = float(raw_rho)
            except Exception:
                rho = S1 * Sweetness   # safe fallback

        # ==== ASSET VALUES ====
        asset_value_if_real = float(env_init["asset_value_if_real"])
        asset_value_if_honey = 2.0
        # CHANGE: Always Honeypot to analyze defensive behavior
        asset_real = False

        # ==== CREATE ENVIRONMENT (WAS MISSING) ====
        self.env = Environment(
            S1=S1,
            S2=S2,
            sweetness=Sweetness,
            C=C,
            rho=rho,
            asset_real=asset_real,
            asset_value_if_real=asset_value_if_real,
            asset_value_if_honey=asset_value_if_honey,
        )

        # ===========================
        #   ATTACKER BELIEF
        # ===========================
        self.p_honey = float(env_init.get("initial_p", 0.5))

        # ===========================
        #   HISTORY
        # ===========================
        self.attack_actions = []
        self.defense_actions = []
        self.signal_history = []
        self.belief_history = [self.p_honey]

        self.U_A_step = []
        self.U_A_realized_step = []  # New metric: Real Utility (Objective)
        self.U_D_step = []
        self.T = T

        self.defender.U_D_global = 0.0

    # ============================================================
    # REALIZED UTILITY (OBJECTIVE)
    # ============================================================
    def compute_realized_utility(self, action):
        """
        Calculates the 'true' utility obtained by the attacker.
        Different from the expected (subjective) utility used to decide.
        """
        # Fixed costs are always paid
        costes = self.attacker.c_T + self.attacker.c_action.get(action, 0.0)
        
        payoff = 0.0
        
        if action == "EXPLOIT":
            if self.env.asset_real:
                # If real, attacker gains asset value
                payoff = self.env.compute_asset_value_for_attacker()
            else:
                # It's a honeypot: Gains nothing and suffers compromise/trap penalty
                # We assume a compromise cost of 5.0
                payoff = -5.0
                
        elif action == "EXIT":
            # If exits, gains nor loses anything extra objectively
            # (Unlike subjective utility where they feel missed opportunity)
            payoff = 0.0
            
        # For RECON/TEST/STEALTH direct payoff is 0 (only costs paid)
        # unless considering information gain as real utility,
        # but objectively they only spend time.
        
        return payoff - costes

    # ============================================================
    # DEFENDER UTILITY
    # ============================================================
    def _defender_step_utility(self, atk_action, def_main, def_sub, sig):
        """Calculates defender's utility for a single step."""
        meta = MITRE_META.get(
            (def_main, def_sub),
            {"cost": 2.0, "tag": "general", "risk": "medium"},
        )

        cost = meta["cost"]
        tag = meta["tag"]
        risk = meta["risk"]

        risk_penalty = {"low": 0.1, "medium": 0.25, "high": 0.6}[risk]

        bonus = 0.0

        if atk_action == "EXPLOIT":
            if tag in ("monitoring", "manipulation", "deception"):
                bonus += 1.5
            elif tag in ("analysis", "intel"):
                bonus += 0.7
        elif atk_action in ("RECON", "TEST"):
            if tag in ("deception", "intel", "analysis"):
                bonus += 1.2
            elif tag == "monitoring":
                bonus += 0.4
        elif atk_action == "STEALTH":
            if tag in ("monitoring", "analysis"):
                bonus += 1.0

        deception_gain = self.p_honey * self.env.honey.C

        sweetSig = sig["sweetness_signal"]
        hint = sig["honey_hint"]
        signal_bonus = 0.4 * (sweetSig + hint - 1.0)

        return bonus + deception_gain + signal_bonus - (0.3 * cost + risk_penalty)

    # ============================================================
    # COMPUTE_STEP_PAYOFFS
    # ============================================================
    def compute_step_payoffs(self, atk_action, def_actions, sig, t: int):
        """Computes payoffs for both attributes for the current step."""
        # U_A: recompute expected_utility (consistent with history)
        uA = self.attacker.expected_utility(atk_action, self.env, self.p_honey)

        def_main, def_sub = def_actions
        uD = self._defender_step_utility(atk_action, def_main, def_sub, sig)

        return uA, uD

    # ============================================================
    # A COMPLETE GAME STEP
    # ============================================================
    def step(self) -> bool:
        """Executes a single step of the game."""
        t = len(self.attack_actions)

        # 1) Attacker action
        aA = self.attacker.choose_action(self.env, self.p_honey, t=t)
        self.attack_actions.append(aA)

        if aA == "EXIT":
            # no more steps; game over
            return False

        # 2) Defender action
        main, sub = self.defender.choose_action(
            self.env, self.belief_history, aA, t
        )
        self.defense_actions.append((main, sub))

        # 3) Generated signals
        sig = generate_signals(self.env, (main, sub))
        self.signal_history.append(sig)

        # 4) Utilities
        uA = self.compute_step_payoffs(aA, (main, sub), sig, t)[0] # We only need uA expected here
        uD = self.compute_step_payoffs(aA, (main, sub), sig, t)[1]
        
        # Realized Utility (Objective)
        uA_real = self.compute_realized_utility(aA)
        
        self.U_A_step.append(uA)
        self.U_A_realized_step.append(uA_real)
        self.U_D_step.append(uD)
        
        # ⚠️ Attacker already accumulates U_A_global inside Attacker.choose_action.
        self.defender.U_D_global += (self.defender.delta_D ** t) * uD

        # 5) Update environment (MITRE env effects)
        self.update_environment_mitre(main, sub)

        # 6) Update honeypot belief
        self.p_honey = update_attacker_belief(
            self.p_honey, sig, self.env, self.attacker
        )
        self.belief_history.append(self.p_honey)

        # 7) Advance physical time of environment
        self.env.advance_time()

        return True

    # ============================================================
    #   APPLY MITRE EFFECTS TO ENVIRONMENT
    # ============================================================
    def update_environment_mitre(self, main, sub):
        """Updates environment state based on MITRE effects."""
        group = MITRE_ENV_EFFECTS.get(main)
        if not group:
            return

        baseline = group["baseline"]
        effect = group["sub"].get(sub, baseline)

        h = self.env.honey

        h.S1 = clip01(h.S1 + effect["dS1"])
        h.S2 = clip01(h.S2 + effect["dS2"])
        h.sweetness = max(0.0, h.sweetness + effect["dSw"])
        h.C = clip01(h.C + effect["dC"])
        h.rho = h.S1 * h.sweetness

    # ============================================================
    # EXECUTE FULL MATCH
    # ============================================================
    def run(self):
        """Runs the game for T steps."""
        for _ in range(self.T):
            if not self.step():
                break

        return {
            "attack_actions": self.attack_actions,
            "defense_actions": self.defense_actions,
            "signals": self.signal_history,
            "beliefs": self.belief_history,
            "U_A_step": self.U_A_step,
            "U_A_realized_step": self.U_A_realized_step,
            "U_D_step": self.U_D_step,
            "U_A_global": self.attacker.U_A_global,
            "U_D_global": self.defender.U_D_global,
        }
