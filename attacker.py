from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List
import math
import random

ATTACKER_ACTIONS: List[str] = ["RECON", "TEST", "EXPLOIT", "STEALTH", "EXIT"]


@dataclass
class Attacker:
    attacker_id: int
    mot: str
    skill: str
    knowl: str
    auto: str
    att: str
    risk: str
    affil: str
    obj: str

    lambda_dec: float = 0.0
    lambda_sweet: float = 0.0
    c_T: float = 0.0
    c_action: Dict[str, float] = None
    C_det: float = 0.0
    delta: float = 0.9

    aggression: float = 0.0
    exploration_rate: float = 0.0
    risk_aversion: float = 0.0

    U_A_global: float = 0.0
    utility_history: List[float] = None

    def __post_init__(self):
        self._compute_derived_parameters()
        self.utility_history = []
        if self.c_action is None:
            self.c_action = {}

    # ============================
    #   BASE TABLES
    # ============================

    @staticmethod
    def _skill_table(skill):
        """Returns skill-based parameters."""
        if skill == "low":
            return {"bonus": 1.0, "Pr_comp_base": 0.25}
        if skill == "medium":
            return {"bonus": 2.0, "Pr_comp_base": 0.55}
        if skill == "high":
            return {"bonus": 3.0, "Pr_comp_base": 0.85}
        return {"bonus": 2.0, "Pr_comp_base": 0.55}

    @staticmethod
    def _mot_table(mot):
        """Returns motivation-based parameters."""
        if mot == "economic":
            return {"lambda_sweet": 0.6, "lambda_dec_extra": 0.3, "agg": 0.5}
        if mot == "espionage":
            return {"lambda_sweet": 1.2, "lambda_dec_extra": 1.5, "agg": 0.7}
        if mot == "ideological":
            return {"lambda_sweet": 0.7, "lambda_dec_extra": 0.5, "agg": 0.4}
        if mot == "sabotage":
            return {"lambda_sweet": 0.9, "lambda_dec_extra": 1.0, "agg": 0.9}
        return {"lambda_sweet": 0.7, "lambda_dec_extra": 0.5, "agg": 0.6}

    @staticmethod
    def _knowl_table(knowl):
        """Returns knowledge-based parameters."""
        if knowl == "low":
            return {"lambda_dec": 0.2, "c_T": 1.4, "explore": 0.3}
        if knowl == "medium":
            return {"lambda_dec": 0.7, "c_T": 1.0, "explore": 0.6}
        if knowl == "high":
            return {"lambda_dec": 1.2, "c_T": 0.7, "explore": 0.9}
        return {"lambda_dec": 0.7, "c_T": 1.0, "explore": 0.6}

    @staticmethod
    def _auto_table(auto):
        """Returns automation-based parameters."""
        if auto == "manual":
            return {"c_T_add": 1.0, "c_RECON_bonus": 1.0}
        if auto == "hybrid":
            return {"c_T_add": 0.0, "c_RECON_bonus": 0.0}
        if auto == "auto":
            return {"c_T_add": -0.4, "c_RECON_bonus": -0.5}
        return {"c_T_add": 0.0, "c_RECON_bonus": 0.0}

    @staticmethod
    def _risk_table(risk):
        """Returns risk-based parameters."""
        if risk == "low":
            return {
                "C_det": 10.0,
                "delta": 0.95,
                "lambda_dec_extra": 2.0,
                "risk_av": 0.3,
            }
        if risk == "medium":
            return {
                "C_det": 5.0,
                "delta": 0.75,
                "lambda_dec_extra": 1.0,
                "risk_av": 0.6,
            }
        if risk == "high":
            return {
                "C_det": 2.0,
                "delta": 0.55,
                "lambda_dec_extra": 0.2,
                "risk_av": 1.0,
            }
        return {"C_det": 5.0, "delta": 0.75, "lambda_dec_extra": 1.0, "risk_av": 0.6}

    @staticmethod
    def _affil_table(a):
        """Returns affiliation-based parameters."""
        if a == "individual":
            return {"C_det_extra": 0.0, "delta_extra": -0.05}
        if a == "crime":
            return {"C_det_extra": 2.0, "delta_extra": 0.05}
        if a == "insider":
            return {"C_det_extra": 1.0, "delta_extra": 0.10}
        if a == "state":
            return {"C_det_extra": 10.0, "delta_extra": 0.20}
        return {"C_det_extra": 0.0, "delta_extra": 0.0}

    @staticmethod
    def _att_table(att):
        """Returns attack type parameters."""
        if att == "opportunistic":
            return {
                "lambda_sweet": 0.4,
                "delta": 0.4,
                "stealth_cost": -0.1,
                "agg": 0.4,
            }
        if att == "persistent":
            return {
                "lambda_sweet": 0.7,
                "delta": 0.7,
                "stealth_cost": 0.0,
                "agg": 0.6,
            }
        if att == "targeted":
            return {
                "lambda_sweet": 1.0,
                "delta": 0.9,
                "stealth_cost": 0.2,
                "agg": 0.8,
            }
        if att == "destructive":
            return {
                "lambda_sweet": 1.3,
                "delta": 0.6,
                "stealth_cost": -0.4,
                "agg": 1.0,
            }
        return {"lambda_sweet": 0.7, "delta": 0.7, "stealth_cost": 0.0, "agg": 0.6}

    # ============================
    #   DERIVED PARAMETERS
    # ============================
    def _compute_derived_parameters(self):
        """Computes derived parameters based on attacker attributes."""
        mot_t = self._mot_table(self.mot)
        skill_t = self._skill_table(self.skill)
        knowl_t = self._knowl_table(self.knowl)
        auto_t = self._auto_table(self.auto)
        risk_t = self._risk_table(self.risk)
        affil_t = self._affil_table(self.affil)
        att_t = self._att_table(self.att)

        self.lambda_dec = (
            knowl_t["lambda_dec"]
            + mot_t["lambda_dec_extra"]
            + risk_t["lambda_dec_extra"]
        )
        self.lambda_sweet = mot_t["lambda_sweet"] + att_t["lambda_sweet"]

        self.c_T = knowl_t["c_T"] + auto_t["c_T_add"]

        # base costs
        base_RECON = 0.4
        base_TEST = 0.9
        base_EXPLOIT = 2.4
        base_STEALTH = 0.8

        skill_bonus = skill_t["bonus"]
        recon_bonus = auto_t["c_RECON_bonus"]
        stealth_extra = att_t["stealth_cost"]

        # lower costs so EXPLOIT/TEST are used
        self.c_action = {
            "RECON": max(0.02, base_RECON - recon_bonus - 0.25 * skill_bonus),
            "TEST": max(0.05, base_TEST - 0.35 * skill_bonus),
            "EXPLOIT": max(0.25, base_EXPLOIT - 0.5 * skill_bonus),
            "STEALTH": max(0.05, base_STEALTH + stealth_extra),
            "EXIT": 0.0,
        }

        self.C_det = risk_t["C_det"] + affil_t["C_det_extra"]

        raw_delta = risk_t["delta"] + affil_t["delta_extra"] + att_t["delta"]
        self.delta = max(0.4, min(0.99, raw_delta / 3.0))

        self.aggression = max(0.0, min(1.0, (mot_t["agg"] + att_t["agg"]) / 2.0))
        self.exploration_rate = max(0.0, min(1.0, knowl_t["explore"]))
        self.risk_aversion = max(0.0, min(1.0, risk_t["risk_av"]))

    # ============================
    #   INSTANT UTILITY
    # ============================

    def _compute_Pr_comp_real(self, action, env):
        """Computes probability of compromising the real asset."""
        if action != "EXPLOIT":
            return 0.0

        base = self._skill_table(self.skill)["Pr_comp_base"]
        factor = 0.5 + 0.04 * env.honey.sweetness
        Pr = base * factor
        return max(0.0, min(0.95, Pr))

    def _compute_detection_prob(self, action, env, p_honey):
        """Computes probability of detection."""
        base = {
            "RECON": 0.08,
            "TEST": 0.15,
            "EXPLOIT": 0.55,  # before 0.75
            "STEALTH": 0.03,
            "EXIT": 0.0,
        }.get(action, 0.25)

        env_factor = 0.5 + 0.5 * env.honey.C

        if action == "EXPLOIT":
            env_factor *= 1.0 + 0.5 * p_honey

        return min(1.0, max(0.0, base * env_factor))

    def expected_utility(self, action, env, p_honey):
        """Calculates the expected utility of an action."""
        V_real = env.compute_asset_value_for_attacker()
        V_honeyinfo = env.compute_honey_info_value_for_attacker()
        pi_trap = env.compute_pi_trap()
        rho = env.honey.rho

        V_real_eff = min(V_real, 8.0)
        Pr_real = self._compute_Pr_comp_real(action, env)
        P_det = self._compute_detection_prob(action, env, p_honey)
        cA = self.c_action.get(action, 0.0)

        term_real = (1 - p_honey) * V_real_eff * Pr_real

        if action in ("RECON", "TEST"):
            info_gain = 0.6 if action == "RECON" else 0.9
            term_honey = p_honey * (info_gain * V_honeyinfo * (1 - pi_trap))

        elif action == "STEALTH":
            term_honey = -0.15 * p_honey * self.lambda_dec * rho * pi_trap

        elif action == "EXPLOIT":
            term_honey = p_honey * (
                V_honeyinfo * (0.5 - pi_trap) - self.lambda_dec * rho * pi_trap
            )

        elif action == "EXIT":
            # strong penalty for exiting the game: forces trying things
            exit_penalty = 3.0 + 0.5 * self.C_det
            return -exit_penalty

        else:
            # fallback
            return -1.0

        term_time = self.c_T
        term_action = cA

        # softer detection penalty
        term_det = self.C_det * P_det * (0.3 + 0.3 * self.risk_aversion)

        return term_real + term_honey - term_time - term_action - term_det

    # ============================
    #   FUTURE FORECAST
    # ============================

    def _forecast_future(self, env, p_honey, action):
        """Forecasts future utility based on current action."""
        V_real = env.compute_asset_value_for_attacker()
        V_real_eff = min(V_real, 8.0)

        if action == "RECON":
            p_next = 0.65 * p_honey + 0.35 * 0.4
            bonus_Pr = 0.18
        elif action == "TEST":
            p_next = 0.55 * p_honey + 0.45 * 0.35
            bonus_Pr = 0.28
        elif action == "STEALTH":
            p_next = 0.9 * p_honey
            bonus_Pr = -0.05
        elif action == "EXPLOIT":
            p_next = min(1.0, 0.7 * p_honey + 0.2)
            bonus_Pr = 0.0
        else:
            return 0.0

        Pr_base = self._skill_table(self.skill)["Pr_comp_base"] + bonus_Pr
        Pr_future = max(0.0, min(0.95, Pr_base))

        return (1 - p_next) * V_real_eff * Pr_future - p_next * 1.5

    # ============================
    #   EXPLORATION BONUS
    # ============================

    def _exploration_bonus(self, action, t, p_honey):
        """Calculates exploration bonus."""
        bonus = 0.0

        if t <= 2:
            if action in ("RECON", "TEST"):
                bonus += 1.5 * self.exploration_rate
            elif action == "EXPLOIT":
                bonus -= 1.0 * (1.0 - self.exploration_rate)

        elif 3 <= t <= 5:
            if action in ("RECON", "TEST", "STEALTH"):
                bonus += 0.8 * self.exploration_rate

        if p_honey >= 0.5:
            if action == "EXPLOIT":
                bonus -= 1.5 * (0.5 + self.risk_aversion)
            elif action in ("RECON", "STEALTH"):
                bonus += 0.8 * (0.5 + self.exploration_rate)

        if action == "EXIT" and t < 6:
            bonus -= 5.0

        return bonus

    # ============================
    #   CHOOSE ACTION (with epsilon-greedy)
    # ============================

    def choose_action(self, env, p_honey, t):
        """Chooses the best action using epsilon-greedy strategy."""
        best_action = None
        best_total = -1e9

        totals = {}

        for a in ATTACKER_ACTIONS:
            u_now = self.expected_utility(a, env, p_honey)
            u_future = self._forecast_future(env, p_honey, a)
            bonus = self._exploration_bonus(a, t, p_honey)

            total = u_now + self.delta * u_future + bonus
            totals[a] = total

            if total > best_total:
                best_total = total
                best_action = a

        # epsilon-greedy: explore some of the time
        epsilon = max(0.02, min(0.10, 0.05 + 0.05 * self.exploration_rate))
        if random.random() < epsilon:
            best_action = random.choice(ATTACKER_ACTIONS)

        # immediate utility of chosen action
        u_t = self.expected_utility(best_action, env, p_honey)
        self.U_A_global += (self.delta ** t) * u_t
        self.utility_history.append(u_t)

        return best_action
