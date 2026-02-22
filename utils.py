# utils.py
import numpy as np
from math import log2

def clip01(x: float) -> float:
    """Clips a value to the range [0, 1]."""
    x = float(x)
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def safe_mean(x):
    """Calculates a safe mean for empty lists/arrays."""
    if x is None:
        return 0.0
    if len(x) == 0:
        return 0.0
    return float(np.mean(x))


def entropy(probs) -> float:
    """
    Calculates the entropy in bits of a discrete distribution.
    Accepts unnormalized list/array of weights.
    """
    arr = np.asarray(probs, dtype=float)
    s = arr.sum()
    if s <= 0:
        return 0.0
    arr = arr / s
    return float(-np.sum([p * log2(p) for p in arr if p > 0]))
