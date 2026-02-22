# ============================================================
# defender.py — MITRE Model + Fatigue + Learning + Hypergame
# ============================================================

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple, List
import numpy as np

from mitre_effects import MITRE_ACTIONS, MITRE_SIGNAL_EFFECTS, MITRE_META


# ============================================================
# LAYER 1: BASE MITRE SCORING
# ============================================================

def compute_mitre_score(main: str, sub: str, weights: Dict[str, float]) -> float:
    """
    Technical score based on MITRE_SIGNAL_EFFECTS + defender weights.
    """
    effects = MITRE_SIGNAL_EFFECTS[main]["sub"].get(sub, {})
    meta = MITRE_META.get((main, sub), {"cost": 2.0})

    # Signals related to info / deception / monitoring
    delta_info = (
        abs(effects.get("banner_consistency", 0))
        + abs(effects.get("fingerprint_vm", 0))
        + abs(effects.get("system_errors", 0))
    )

    delta_eng = (
        abs(effects.get("traffic_pattern", 0))
        + abs(effects.get("latency", 0))
    )

    delta_prot = -effects.get("vuln_attractiveness", 0)

    cost = meta["cost"]

    score = (
        weights["eng"] * delta_eng
        + weights["info"] * delta_info
        + weights["prot"] * delta_prot
        - weights["cost"] * cost
    )

    return score


# ============================================================
# LAYER 2: FATIGUE AND INERTIA
# ============================================================

def compute_fatigue_score(
    last_action: Tuple[str, str] | None,
    main: str,
    sub: str,
    fatigue_state: Dict[Tuple[str, str], float],
) -> float:
    """Computes score adjustment based on fatigue and inertia."""
    pair = (main, sub)

    fatigue = fatigue_state.get(pair, 0.0)

    inertia_bonus = 0.7 if last_action == pair else 0.0
    fatigue_penalty = -0.25 * fatigue

    return inertia_bonus + fatigue_penalty


# ============================================================
# LAYER 3: LIGHTWEIGHT LEARNING
# ============================================================

def compute_learning_score(tag: str, last_attacker: str | None) -> float:
    """Computes score adjustment based on past attacker actions."""
    if last_attacker is None:
        return 0.0

    if last_attacker == "EXPLOIT":
        if tag in ("monitoring", "analysis", "manipulation"):
            return 1.4

    if last_attacker in ("RECON", "TEST"):
        if tag in ("deception", "intel"):
            return 1.2

    if last_attacker == "STEALTH":
        if tag in ("monitoring", "analysis"):
            return 1.0

    return 0.0


# ============================================================
# COMPLETE DEFENDER
# ============================================================

@dataclass
class Defender:
    defender_id: int
    w_eng: float
    w_info: float
    w_prot: float
    w_cost: float
    res: int
    riskD: float

    fatigue_state: Dict[Tuple[str, str], float] | None = None
    last_action: Tuple[str, str] | None = None
    U_D_global: float = 0.0
    delta_D: float = 0.95

    def __post_init__(self):
        # discount based on risk (more risk -> more impatience)
        self.delta_D = max(0.5, 1 - self.riskD)
        if self.fatigue_state is None:
            self.fatigue_state = {}

    # ========================================================
    # MAIN FUNCTION: ACTION SELECTION
    # ========================================================
    def choose_action(self, env, beliefs: List[float], last_attacker: str | None, t: int):
        """
        Hypergame: the defender adapts weights according to the attacker's belief.
        beliefs: history of pHoney that the attacker has (or that the defender estimates).
        """
        weights = {
            "eng": float(self.w_eng),
            "info": float(self.w_info),
            "prot": float(self.w_prot),
            "cost": float(self.w_cost),
        }

        # ======================
        # Simple Hypergame Layer
        # ======================
        if beliefs:
            window = beliefs[-5:] if len(beliefs) >= 5 else beliefs
            mean_p = float(np.mean(window))  # mean pHoney
        else:
            mean_p = 0.5

        # Attacker believes almost everything is real -> hardening / monitoring
        if mean_p < 0.3:
            weights["prot"] *= 1.15
            weights["eng"] *= 1.05

        # Attacker believes it's a honeypot -> more deception / intel
        elif mean_p > 0.7:
            weights["info"] *= 1.15
            weights["eng"] *= 0.95

        # ====================================================
        # Score for each (main, sub) in MITRE Engage
        # ====================================================
        scores: Dict[Tuple[str, str], float] = {}

        for main, subs in MITRE_ACTIONS.items():
            for sub in subs:
                meta = MITRE_META.get((main, sub), {"tag": "general", "cost": 2.0})
                tag = meta["tag"]

                score_mitre = compute_mitre_score(main, sub, weights)
                score_fatigue = compute_fatigue_score(
                    self.last_action, main, sub, self.fatigue_state
                )
                score_learning = compute_learning_score(tag, last_attacker)

                total = score_mitre + score_fatigue + score_learning

                scores[(main, sub)] = total

        # ---------------------------
        # Probabilistic Softmax
        # ---------------------------
        keys = list(scores.keys())
        vals = np.array([scores[k] for k in keys], dtype=float)

        temperature = max(0.3, 1.5 - self.riskD)  # more risk -> more exploration
        logits = np.exp(vals / temperature)
        probs = logits / logits.sum()

        idx = np.random.choice(len(keys), p=probs)
        choice = keys[idx]

        # ---------------------------
        # Update fatigue
        # ---------------------------
        for k in list(self.fatigue_state.keys()):
            self.fatigue_state[k] *= 0.9

        self.fatigue_state[choice] = self.fatigue_state.get(choice, 0.0) + 0.4 * (
            1 + self.res
        )
        self.last_action = choice

        return choice
