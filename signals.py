# signals.py
import numpy as np
from utils import clip01
from mitre_effects import MITRE_ACTIONS, MITRE_SIGNAL_EFFECTS

# ============================================================
# Signaling Parameters
# ============================================================

SIGMA_LAT = 0.20
SIGMA_JIT = 0.25
SIGMA_FP = 0.15
SIGMA_NOISE = 0.20

# Strength with which the attacker adjusts belief at each step
BAYES_ALPHA = 0.10   # before 0.15 -> now responds much more
ANCHOR = 0.10        # kept in case it's needed later


# ============================================================
# REALISTIC SIGNAL GENERATION (MITRE Engage style)
# ============================================================

def generate_signals(env, defender_actions):
    """
    Returns signals: latency, jitter, fingerprint_vm, banner_noise,
    vuln_attractiveness, traffic_pattern, system_errors, sweetSig, hint.
    """
    act_main, act_sub = defender_actions

    eff = MITRE_SIGNAL_EFFECTS.get(act_main, {})
    base = eff.get("baseline", {})
    delta = eff.get("sub", {}).get(act_sub, {})

    def noisy(base_v, d, sigma):
        return clip01(base_v + d + np.random.normal(0, sigma))

    latency = noisy(base.get("latency", 0), delta.get("latency", 0), SIGMA_LAT)
    jitter = noisy(base.get("jitter", 0), delta.get("jitter", 0), SIGMA_JIT)
    fp_vm = noisy(
        base.get("fingerprint_vm", 0),
        delta.get("fingerprint_vm", 0),
        SIGMA_FP,
    )
    banner = noisy(
        base.get("banner_consistency", 0),
        delta.get("banner_consistency", 0),
        SIGMA_FP,
    )
    attractor = noisy(
        base.get("vuln_attractiveness", 0),
        delta.get("vuln_attractiveness", 0),
        0.10,
    )
    traffic = noisy(
        base.get("traffic_pattern", 0),
        delta.get("traffic_pattern", 0),
        0.10,
    )
    errors = noisy(
        base.get("system_errors", 0),
        delta.get("system_errors", 0),
        SIGMA_NOISE,
    )

    sweetSig = clip01(env.honey.sweetness / 10.0 + np.random.normal(0, 0.03))
    hint = clip01(env.honey.rho / 10.0 + np.random.normal(0, 0.03))

    return {
        "latency": latency,
        "jitter": jitter,
        "fingerprint_vm": fp_vm,
        "banner_noise": 1 - banner,
        "vuln_attractiveness": attractor,
        "traffic_pattern": traffic,
        "system_errors": errors,
        "sweetness_signal": sweetSig,
        "honey_hint": hint,
    }


# ============================================================
#      BAYES: Attacker Belief about Honeypot
# ============================================================

def gaussian_likelihood(x, mu, sigma):
    """Calculates the likelihood of x given a Gaussian distribution (mu, sigma)."""
    if sigma <= 0: sigma = 0.001
    term1 = 1.0 / (sigma * np.sqrt(2 * np.pi))
    term2 = np.exp(-0.5 * ((x - mu) / sigma) ** 2)
    return term1 * term2

def update_attacker_belief(p_old, sig, env, attacker):
    """
    Updates belief p(H=1) using Gaussian Bayesian inference.
    Replaces the previous heuristic with a more robust likelihood model.
    """
    
    # 1. LATENCY - VERY TOLERANT
    # Real: Can be slow (up to 1s with low prob)
    mu_lat_real = 0.10
    sig_lat_real = 0.50 # Giant Sigma to tolerate real lags
    
    # Honey: Depends on quality C. If C is high, low latency (mimics well).
    # If C is low, high latency.
    mu_lat_honey = 0.10 + (1.0 - env.honey.C) * 0.5 
    sig_lat_honey = 0.50
    
    l_lat_real = gaussian_likelihood(sig['latency'], mu_lat_real, sig_lat_real)
    l_lat_honey = gaussian_likelihood(sig['latency'], mu_lat_honey, sig_lat_honey)

    # 2. JITTER
    l_jit_real = gaussian_likelihood(sig['jitter'], 0.02, 0.10)
    l_jit_honey = gaussian_likelihood(sig['jitter'], 0.15, 0.20)

    # 3. BANNERS (TIMEOUT = NEUTRAL)
    # High banner_noise means inconsistency
    if sig['banner_noise'] > 0.5: 
        l_ban_real = 0.5 # Internet fails
        l_ban_honey = 0.5 # Honeypots fail
    else: 
        l_ban_real = 0.8 
        l_ban_honey = 0.6 

    # 4. SWEETNESS (ADMIN PANEL)
    # If we see Admin, probability of honey rises, but not to 100%
    if sig['sweetness_signal'] > 0.8: 
        l_sweet_real = 0.3 
        l_sweet_honey = 0.8
    else:
        l_sweet_real = 0.7
        l_sweet_honey = 0.5

    # CALCULATION
    lik_real = max(l_lat_real * l_jit_real * l_ban_real * l_sweet_real, 1e-9)
    lik_honey = max(l_lat_honey * l_jit_honey * l_ban_honey * l_sweet_honey, 1e-9)

    num = lik_honey * p_old
    den = num + (lik_real * (1.0 - p_old))
    
    if den == 0: 
        return p_old
    
    raw_post = num / den
    
    # STRONG DAMPING (Belief inertia)
    damping = 0.4 
    p_new = (raw_post * (1.0 - damping)) + (p_old * damping)
    
    return clip01(p_new)