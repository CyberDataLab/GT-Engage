# ============================================================
# environment.py — Game Environment (Honey + Asset)
# ============================================================

from dataclasses import dataclass
from utils import clip01


@dataclass
class HoneyState:
    S1: float
    S2: float
    sweetness: float
    C: float
    rho: float = 0.0

    def recompute_rho(self):
        self.rho = self.S1 * self.sweetness


class Environment:
    """
    Simplified but realistic environment:
      - honey: parameters S1, S2, sweetness, C, rho
      - asset_real: whether the asset is real or a honeypot
      - asset_value_if_real / asset_value_if_honey: base value
    """

    def __init__(
        self,
        S1: float,
        S2: float,
        sweetness: float,
        C: float,
        rho: float,
        asset_real: bool,
        asset_value_if_real: float,
        asset_value_if_honey: float,
    ):
        self.honey = HoneyState(
            S1=float(S1),
            S2=float(S2),
            sweetness=float(sweetness),
            C=float(C),
            rho=float(rho),
        )
        self.asset_real = bool(asset_real)
        self.asset_value_if_real = float(asset_value_if_real)
        self.asset_value_if_honey = float(asset_value_if_honey)
        self.t = 0

    # ========================================================
    #   ASSET VALUE FOR ATTACKER
    # ========================================================
    def compute_asset_value_for_attacker(self) -> float:
        """
        Effective value of the asset (capped for numerical stability).
        Scales with S1 and S2.
        """
        base = self.asset_value_if_real if self.asset_real else self.asset_value_if_honey
        # S1 and S2 between 0–1, base typically 1–10
        factor = 0.5 + 0.3 * self.honey.S1 + 0.2 * self.honey.S2
        value = base * factor
        return max(0.0, min(10.0, value))

    def compute_honey_info_value_for_attacker(self) -> float:
        """
        Value of information the attacker gains by interacting
        with honeypots / decoys (for expected_utility).
        """
        # Higher value if C (deception quality) and sweetness are high
        base = self.asset_value_if_honey
        value = base * (0.4 + 0.8 * self.honey.C) + 1.5 * (self.honey.sweetness / 10.0)
        return max(0.0, min(8.0, value))

    @property
    def asset_value_if_honey(self) -> float:
        return self._asset_value_if_honey

    @asset_value_if_honey.setter
    def asset_value_if_honey(self, v: float):
        self._asset_value_if_honey = float(v)

    # ========================================================
    #   TRAP PROBABILITY
    # ========================================================
    def compute_pi_trap(self) -> float:
        """
        Approximates the probability that the attacker falls into a trap.
        Depends on C and rho (honeypot coupling).
        """
        # rho can be >1, we normalize it
        rho_norm = min(1.0, self.honey.rho / 5.0)
        p = 0.15 + 0.5 * self.honey.C + 0.3 * rho_norm
        return clip01(p)

    # ========================================================
    #   ENVIRONMENT EVOLUTION
    # ========================================================
    def advance_time(self):
        """
        Smooth evolution of the environment between steps (slight decay).
        """
        self.t += 1

        # Slight relaxation towards mean values
        self.honey.S2 = clip01(self.honey.S2 * 0.98 + 0.02 * 0.5)
        self.honey.sweetness = max(0.0, self.honey.sweetness * 0.99)
        # C is maintained; rho is recomputed outside by Game.update_environment_mitre,
        # but we can ensure consistency:
        self.honey.recompute_rho()
