# mitre_effects.py
from utils import clip01

# =============================================================
# COMPLETE MITRE ENGAGE CATALOG (grouped by main action)
# =============================================================

MITRE_ACTIONS = {
    "Prepare": [
        "Cyber Threat Intelligence",
        "Engagement Environment",
        "Gating Criteria",
        "Operational Objective",
        "Persona Creation",
        "Storyboarding",
        "Threat Model",
    ],
    "Expose": [
        "API Monitoring",
        "Network Monitoring",
        "Software Manipulation",
        "System Activity Monitoring",
        "Introduced Vulnerabilities",
        "Lures",
        "Malware Detonation",
        "Network Analysis",
        "Application Logs",
        "Behavioral Indicators",
        "Endpoint Monitoring",
        "Network Logs",
        "Sensor Telemetry",
    ],
    "Affect": [
        "Baseline",
        "Hardware Manipulation",
        "Security Controls",
        "Malware Detonation",
        "Network Manipulation",
        "Email Manipulation",
        "Attack Vector Migration",
        "Introduced Vulnerabilities",
        "Lures",
        "Isolation",
        "Peripheral Management",
        "Software Manipulation",
    ],
    "Elicit": [
        "Application Diversity",
        "Artifact Diversity",
        "Burn-In",
        "Email Manipulation",
        "Information Manipulation",
        "Network Diversity",
        "Peripheral Management",
        "Pocket Litter",
        "Introduced Vulnerabilities",
        "Malware Detonation",
        "Personas",
    ],
    "Understand": [
        "After-Action Review",
        "Cyber Threat Intelligence",
        "Threat Model",
    ],
}


SIGNALS = [
    "latency",
    "jitter",
    "fingerprint_vm",
    "banner_consistency",
    "vuln_attractiveness",
    "traffic_pattern",
    "system_errors",
]

# =============================================================
# SIGNAL EFFECTS (Φ) COMPLETE
# =============================================================

MITRE_SIGNAL_EFFECTS = {
    "Prepare": {
        "baseline": {s: 0.0 for s in SIGNALS},
        "sub": {
            "Cyber Threat Intelligence": {
                "latency": 0.00, "jitter": 0.00,
                "fingerprint_vm": -0.05, "banner_consistency": 0.10,
                "vuln_attractiveness": 0.00, "traffic_pattern": 0.00,
                "system_errors": -0.02,
            },
            "Engagement Environment": {
                "latency": 0.02, "jitter": 0.00,
                "fingerprint_vm": -0.08, "banner_consistency": 0.12,
                "vuln_attractiveness": 0.05, "traffic_pattern": 0.02,
                "system_errors": -0.03,
            },
            "Gating Criteria": {
                "latency": 0.01, "jitter": 0.01,
                "fingerprint_vm": -0.03, "banner_consistency": 0.05,
                "vuln_attractiveness": -0.05, "traffic_pattern": -0.03,
                "system_errors": -0.03,
            },
            "Operational Objective": {
                "latency": 0.00, "jitter": 0.00,
                "fingerprint_vm": 0.00, "banner_consistency": 0.03,
                "vuln_attractiveness": 0.00, "traffic_pattern": 0.00,
                "system_errors": 0.00,
            },
            "Persona Creation": {
                "latency": -0.01, "jitter": -0.01,
                "fingerprint_vm": -0.07, "banner_consistency": 0.15,
                "vuln_attractiveness": 0.05, "traffic_pattern": -0.02,
                "system_errors": -0.02,
            },
            "Storyboarding": {
                "latency": -0.01, "jitter": -0.02,
                "fingerprint_vm": -0.05, "banner_consistency": 0.10,
                "vuln_attractiveness": 0.00, "traffic_pattern": -0.02,
                "system_errors": -0.03,
            },
            "Threat Model": {
                "latency": 0.00, "jitter": 0.00,
                "fingerprint_vm": -0.04, "banner_consistency": 0.07,
                "vuln_attractiveness": -0.02, "traffic_pattern": -0.01,
                "system_errors": -0.02,
            },
        },
    },

    "Expose": {
        "baseline": {s: 0.0 for s in SIGNALS},
        "sub": {
            "API Monitoring": {
                "latency": 0.10, "jitter": 0.05,
                "fingerprint_vm": 0.00, "banner_consistency": -0.02,
                "vuln_attractiveness": 0.00, "traffic_pattern": 0.25,
                "system_errors": 0.05,
            },
            "Network Monitoring": {
                "latency": 0.08, "jitter": 0.05,
                "fingerprint_vm": 0.00, "banner_consistency": 0.00,
                "vuln_attractiveness": 0.00, "traffic_pattern": 0.30,
                "system_errors": 0.05,
            },
            "Software Manipulation": {
                "latency": 0.05, "jitter": 0.10,
                "fingerprint_vm": 0.08, "banner_consistency": -0.10,
                "vuln_attractiveness": 0.05, "traffic_pattern": 0.10,
                "system_errors": 0.20,
            },
            "System Activity Monitoring": {
                "latency": 0.07, "jitter": 0.04,
                "fingerprint_vm": 0.02, "banner_consistency": 0.00,
                "vuln_attractiveness": 0.00, "traffic_pattern": 0.20,
                "system_errors": 0.10,
            },
            "Introduced Vulnerabilities": {
                "latency": 0.03, "jitter": 0.03,
                "fingerprint_vm": -0.05, "banner_consistency": 0.05,
                "vuln_attractiveness": 0.35, "traffic_pattern": 0.10,
                "system_errors": 0.10,
            },
            "Lures": {
                "latency": 0.02, "jitter": 0.02,
                "fingerprint_vm": -0.08, "banner_consistency": 0.18,
                "vuln_attractiveness": 0.40, "traffic_pattern": 0.08,
                "system_errors": 0.08,
            },
            "Malware Detonation": {
                "latency": 0.15, "jitter": 0.12,
                "fingerprint_vm": 0.05, "banner_consistency": -0.05,
                "vuln_attractiveness": 0.25, "traffic_pattern": 0.25,
                "system_errors": 0.30,
            },
            "Network Analysis": {
                "latency": 0.06, "jitter": 0.03,
                "fingerprint_vm": 0.00, "banner_consistency": 0.00,
                "vuln_attractiveness": 0.00, "traffic_pattern": 0.20,
                "system_errors": 0.05,
            },
            "Application Logs": {
                "latency": 0.04, "jitter": 0.02,
                "fingerprint_vm": 0.00, "banner_consistency": -0.02,
                "vuln_attractiveness": 0.00, "traffic_pattern": 0.15,
                "system_errors": 0.05,
            },
            "Behavioral Indicators": {
                "latency": 0.05, "jitter": 0.03,
                "fingerprint_vm": 0.02, "banner_consistency": 0.00,
                "vuln_attractiveness": 0.00, "traffic_pattern": 0.18,
                "system_errors": 0.10,
            },
            "Endpoint Monitoring": {
                "latency": 0.06, "jitter": 0.03,
                "fingerprint_vm": 0.02, "banner_consistency": 0.00,
                "vuln_attractiveness": 0.00, "traffic_pattern": 0.22,
                "system_errors": 0.08,
            },
            "Network Logs": {
                "latency": 0.04, "jitter": 0.02,
                "fingerprint_vm": 0.00, "banner_consistency": 0.00,
                "vuln_attractiveness": 0.00, "traffic_pattern": 0.20,
                "system_errors": 0.04,
            },
            "Sensor Telemetry": {
                "latency": 0.05, "jitter": 0.03,
                "fingerprint_vm": 0.00, "banner_consistency": 0.00,
                "vuln_attractiveness": 0.00, "traffic_pattern": 0.22,
                "system_errors": 0.06,
            },
        },
    },

    "Affect": {
        "baseline": {s: 0.0 for s in SIGNALS},
        "sub": {
            "Baseline": {
                "latency": 0.03, "jitter": 0.02,
                "fingerprint_vm": 0.05, "banner_consistency": -0.03,
                "vuln_attractiveness": -0.05, "traffic_pattern": 0.08,
                "system_errors": 0.05,
            },
            "Hardware Manipulation": {
                "latency": 0.20, "jitter": 0.20,
                "fingerprint_vm": 0.15, "banner_consistency": -0.15,
                "vuln_attractiveness": -0.10, "traffic_pattern": 0.25,
                "system_errors": 0.30,
            },
            "Security Controls": {
                "latency": 0.10, "jitter": 0.08,
                "fingerprint_vm": 0.05, "banner_consistency": -0.05,
                "vuln_attractiveness": -0.20, "traffic_pattern": 0.15,
                "system_errors": 0.10,
            },
            "Malware Detonation": {
                "latency": 0.18, "jitter": 0.15,
                "fingerprint_vm": 0.10, "banner_consistency": -0.10,
                "vuln_attractiveness": 0.25, "traffic_pattern": 0.30,
                "system_errors": 0.35,
            },
            "Network Manipulation": {
                "latency": 0.22, "jitter": 0.25,
                "fingerprint_vm": 0.08, "banner_consistency": -0.12,
                "vuln_attractiveness": 0.00, "traffic_pattern": 0.35,
                "system_errors": 0.25,
            },
            "Email Manipulation": {
                "latency": 0.12, "jitter": 0.10,
                "fingerprint_vm": 0.05, "banner_consistency": -0.10,
                "vuln_attractiveness": 0.10, "traffic_pattern": 0.20,
                "system_errors": 0.15,
            },
            "Attack Vector Migration": {
                "latency": 0.15, "jitter": 0.12,
                "fingerprint_vm": 0.05, "banner_consistency": -0.08,
                "vuln_attractiveness": 0.05, "traffic_pattern": 0.28,
                "system_errors": 0.18,
            },
            "Introduced Vulnerabilities": {
                "latency": 0.08, "jitter": 0.05,
                "fingerprint_vm": -0.03, "banner_consistency": 0.02,
                "vuln_attractiveness": 0.40, "traffic_pattern": 0.15,
                "system_errors": 0.12,
            },
            "Lures": {
                "latency": 0.06, "jitter": 0.06,
                "fingerprint_vm": -0.06, "banner_consistency": 0.20,
                "vuln_attractiveness": 0.45, "traffic_pattern": 0.12,
                "system_errors": 0.10,
            },
            "Isolation": {
                "latency": 0.30, "jitter": 0.25,
                "fingerprint_vm": 0.10, "banner_consistency": -0.20,
                "vuln_attractiveness": -0.20, "traffic_pattern": 0.40,
                "system_errors": 0.30,
            },
            "Peripheral Management": {
                "latency": 0.10, "jitter": 0.08,
                "fingerprint_vm": 0.05, "banner_consistency": -0.05,
                "vuln_attractiveness": -0.05, "traffic_pattern": 0.18,
                "system_errors": 0.15,
            },
            "Software Manipulation": {
                "latency": 0.16, "jitter": 0.18,
                "fingerprint_vm": 0.10, "banner_consistency": -0.12,
                "vuln_attractiveness": 0.00, "traffic_pattern": 0.22,
                "system_errors": 0.25,
            },
        },
    },

    "Elicit": {
        "baseline": {s: 0.0 for s in SIGNALS},
        "sub": {
            "Application Diversity": {
                "latency": -0.05, "jitter": -0.10,
                "fingerprint_vm": -0.18, "banner_consistency": 0.25,
                "vuln_attractiveness": 0.05, "traffic_pattern": -0.05,
                "system_errors": -0.05,
            },
            "Artifact Diversity": {
                "latency": -0.03, "jitter": -0.08,
                "fingerprint_vm": -0.15, "banner_consistency": 0.18,
                "vuln_attractiveness": 0.10, "traffic_pattern": -0.03,
                "system_errors": -0.03,
            },
            "Burn-In": {
                "latency": -0.02, "jitter": -0.05,
                "fingerprint_vm": -0.12, "banner_consistency": 0.20,
                "vuln_attractiveness": 0.05, "traffic_pattern": -0.05,
                "system_errors": -0.05,
            },
            "Email Manipulation": {
                "latency": 0.08, "jitter": 0.06,
                "fingerprint_vm": 0.03, "banner_consistency": -0.08,
                "vuln_attractiveness": 0.10, "traffic_pattern": 0.18,
                "system_errors": 0.12,
            },
            "Information Manipulation": {
                "latency": 0.02, "jitter": 0.02,
                "fingerprint_vm": -0.05, "banner_consistency": 0.10,
                "vuln_attractiveness": 0.15, "traffic_pattern": 0.05,
                "system_errors": 0.08,
            },
            "Network Diversity": {
                "latency": -0.03, "jitter": -0.08,
                "fingerprint_vm": -0.18, "banner_consistency": 0.18,
                "vuln_attractiveness": 0.05, "traffic_pattern": -0.05,
                "system_errors": -0.05,
            },
            "Peripheral Management": {
                "latency": 0.04, "jitter": 0.02,
                "fingerprint_vm": -0.05, "banner_consistency": 0.05,
                "vuln_attractiveness": 0.00, "traffic_pattern": 0.10,
                "system_errors": 0.05,
            },
            "Pocket Litter": {
                "latency": 0.00, "jitter": 0.00,
                "fingerprint_vm": -0.08, "banner_consistency": 0.15,
                "vuln_attractiveness": 0.20, "traffic_pattern": 0.05,
                "system_errors": 0.05,
            },
            "Introduced Vulnerabilities": {
                "latency": 0.04, "jitter": 0.04,
                "fingerprint_vm": -0.05, "banner_consistency": 0.10,
                "vuln_attractiveness": 0.40, "traffic_pattern": 0.12,
                "system_errors": 0.10,
            },
            "Malware Detonation": {
                "latency": 0.15, "jitter": 0.12,
                "fingerprint_vm": 0.05, "banner_consistency": -0.05,
                "vuln_attractiveness": 0.25, "traffic_pattern": 0.25,
                "system_errors": 0.30,
            },
            "Personas": {
                "latency": -0.02, "jitter": -0.04,
                "fingerprint_vm": -0.15, "banner_consistency": 0.25,
                "vuln_attractiveness": 0.05, "traffic_pattern": -0.03,
                "system_errors": -0.03,
            },
        },
    },

    "Understand": {
        "baseline": {s: 0.0 for s in SIGNALS},
        "sub": {
            "After-Action Review": {
                "latency": -0.01, "jitter": -0.01,
                "fingerprint_vm": -0.02, "banner_consistency": 0.05,
                "vuln_attractiveness": 0.00, "traffic_pattern": -0.02,
                "system_errors": -0.02,
            },
            "Cyber Threat Intelligence": {
                "latency": -0.01, "jitter": -0.01,
                "fingerprint_vm": -0.05, "banner_consistency": 0.05,
                "vuln_attractiveness": -0.02, "traffic_pattern": -0.01,
                "system_errors": -0.02,
            },
            "Threat Model": {
                "latency": -0.01, "jitter": -0.01,
                "fingerprint_vm": -0.03, "banner_consistency": 0.05,
                "vuln_attractiveness": 0.00, "traffic_pattern": -0.02,
                "system_errors": -0.01,
            },
        },
    },
}

# =============================================================
# ENVIRONMENT EFFECTS (S1, S2, Sweetness, C)
# =============================================================

MITRE_ENV_EFFECTS = {
    "Prepare": {
        "baseline": {"dS1": 0.0, "dS2": 0.0, "dSw": 0.0, "dC": 0.0},
        "sub": {
            "Cyber Threat Intelligence": {"dS1": 0.05, "dS2": 0.05, "dSw": 0.00, "dC": 0.08},
            "Engagement Environment": {"dS1": 0.12, "dS2": 0.10, "dSw": 0.05, "dC": 0.10},
            "Gating Criteria": {"dS1": 0.03, "dS2": 0.05, "dSw": -0.10, "dC": 0.12},
            "Operational Objective": {"dS1": 0.02, "dS2": 0.02, "dSw": 0.00, "dC": 0.05},
            "Persona Creation": {"dS1": 0.10, "dS2": 0.08, "dSw": 0.05, "dC": 0.08},
            "Storyboarding": {"dS1": 0.08, "dS2": 0.05, "dSw": 0.00, "dC": 0.06},
            "Threat Model": {"dS1": 0.06, "dS2": 0.06, "dSw": -0.02, "dC": 0.08},
        },
    },

    "Expose": {
        "baseline": {"dS1": 0.0, "dS2": 0.0, "dSw": 0.0, "dC": 0.0},
        "sub": {
            "API Monitoring": {"dS1": 0.02, "dS2": 0.08, "dSw": 0.00, "dC": -0.08},
            "Network Monitoring": {"dS1": 0.02, "dS2": 0.10, "dSw": 0.00, "dC": -0.10},
            "Software Manipulation": {"dS1": -0.05, "dS2": -0.05, "dSw": 0.05, "dC": -0.15},
            "System Activity Monitoring": {"dS1": 0.03, "dS2": 0.06, "dSw": 0.00, "dC": -0.06},
            "Introduced Vulnerabilities": {"dS1": 0.05, "dS2": 0.00, "dSw": 0.45, "dC": -0.08},
            "Lures": {"dS1": 0.08, "dS2": 0.00, "dSw": 0.50, "dC": -0.05},
            "Malware Detonation": {"dS1": -0.05, "dS2": -0.05, "dSw": 0.30, "dC": -0.20},
            "Network Analysis": {"dS1": 0.03, "dS2": 0.07, "dSw": 0.00, "dC": -0.05},
            "Application Logs": {"dS1": 0.01, "dS2": 0.04, "dSw": 0.00, "dC": -0.05},
            "Behavioral Indicators": {"dS1": 0.02, "dS2": 0.05, "dSw": 0.00, "dC": -0.06},
            "Endpoint Monitoring": {"dS1": 0.03, "dS2": 0.06, "dSw": 0.00, "dC": -0.07},
            "Network Logs": {"dS1": 0.02, "dS2": 0.05, "dSw": 0.00, "dC": -0.05},
            "Sensor Telemetry": {"dS1": 0.02, "dS2": 0.06, "dSw": 0.00, "dC": -0.06},
        },
    },

    "Affect": {
        "baseline": {"dS1": 0.0, "dS2": 0.0, "dSw": 0.0, "dC": 0.0},
        "sub": {
            "Baseline": {"dS1": -0.02, "dS2": -0.02, "dSw": -0.05, "dC": -0.05},
            "Hardware Manipulation": {"dS1": -0.10, "dS2": -0.15, "dSw": -0.05, "dC": -0.25},
            "Security Controls": {"dS1": -0.05, "dS2": -0.08, "dSw": -0.10, "dC": -0.20},
            "Malware Detonation": {"dS1": -0.08, "dS2": -0.08, "dSw": 0.20, "dC": -0.25},
            "Network Manipulation": {"dS1": -0.12, "dS2": -0.12, "dSw": -0.05, "dC": -0.30},
            "Email Manipulation": {"dS1": -0.05, "dS2": -0.05, "dSw": 0.05, "dC": -0.15},
            "Attack Vector Migration": {"dS1": -0.05, "dS2": -0.05, "dSw": 0.10, "dC": -0.18},
            "Introduced Vulnerabilities": {"dS1": 0.05, "dS2": 0.00, "dSw": 0.50, "dC": -0.10},
            "Lures": {"dS1": 0.10, "dS2": 0.00, "dSw": 0.55, "dC": -0.08},
            "Isolation": {"dS1": -0.15, "dS2": -0.20, "dSw": -0.10, "dC": -0.40},
            "Peripheral Management": {"dS1": -0.03, "dS2": -0.03, "dSw": -0.05, "dC": -0.12},
            "Software Manipulation": {"dS1": -0.08, "dS2": -0.10, "dSw": 0.00, "dC": -0.22},
        },
    },

    "Elicit": {
        "baseline": {"dS1": 0.0, "dS2": 0.0, "dSw": 0.0, "dC": 0.0},
        "sub": {
            "Application Diversity": {"dS1": 0.20, "dS2": 0.20, "dSw": 0.00, "dC": 0.25},
            "Artifact Diversity": {"dS1": 0.15, "dS2": 0.15, "dSw": 0.10, "dC": 0.20},
            "Burn-In": {"dS1": 0.18, "dS2": 0.18, "dSw": 0.05, "dC": 0.22},
            "Email Manipulation": {"dS1": 0.05, "dS2": 0.00, "dSw": 0.10, "dC": -0.05},
            "Information Manipulation": {"dS1": 0.10, "dS2": 0.05, "dSw": 0.15, "dC": -0.02},
            "Network Diversity": {"dS1": 0.18, "dS2": 0.22, "dSw": 0.00, "dC": 0.20},
            "Peripheral Management": {"dS1": 0.08, "dS2": 0.08, "dSw": 0.00, "dC": 0.10},
            "Pocket Litter": {"dS1": 0.12, "dS2": 0.08, "dSw": 0.20, "dC": 0.05},
            "Introduced Vulnerabilities": {"dS1": 0.08, "dS2": 0.00, "dSw": 0.55, "dC": -0.10},
            "Malware Detonation": {"dS1": -0.05, "dS2": -0.05, "dSw": 0.25, "dC": -0.20},
            "Personas": {"dS1": 0.20, "dS2": 0.18, "dSw": 0.00, "dC": 0.22},
        },
    },
}

# =============================================================
# META-INFO
# =============================================================

def _estimate_cost(main: str, sub: str) -> float:
    """Estimates the cost of an action based on its type."""
    name = sub.lower()
    high = ["detonation", "diversity", "manipulation", "migration", "hardware", "software"]
    medium = ["monitor", "analysis", "intelligence", "logs", "criteria", "telemetry"]
    low = ["story", "persona", "baseline", "review"]

    if any(t in name for t in high):
        return 3.0
    if any(t in name for t in medium):
        return 2.0
    if any(t in name for t in low):
        return 1.0
    return 2.0


def _derive_tag(main: str, sub: str) -> str:
    """Derives a tag for the action based on the main category."""
    if main == "Expose":
        return "monitoring"
    if main == "Prepare":
        return "intel"
    if main == "Understand":
        return "analysis"
    if main == "Elicit":
        return "deception"
    if main == "Affect":
        return "manipulation"
    return "general"


def _estimate_risk(main: str, sub: str) -> str:
    """Estimates the risk level associated with an action."""
    name = sub.lower()
    if any(k in name for k in ["introduced vulnerabilities", "lures", "malware detonation"]):
        return "high"
    if main in ("Affect", "Expose"):
        return "medium"
    if main in ("Prepare", "Understand", "Elicit"):
        return "low"
    return "medium"


# =============================================================
# FINAL META
# =============================================================

MITRE_META = {}
for main, subs in MITRE_ACTIONS.items():
    for sub in subs:
        MITRE_META[(main, sub)] = {
            "cost": _estimate_cost(main, sub),
            "tag": _derive_tag(main, sub),
            "risk": _estimate_risk(main, sub),
        }
