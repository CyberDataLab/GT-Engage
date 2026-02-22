# main.py

import csv
import random
from collections import Counter

from game import Game


ATTACKER_FILE = "attacker_types.csv"
DEFENDER_FILE = "defender_types.csv"
ENVIRONMENT_FILE = "environment_initial_states.csv"
RESULTS_FILE = "results_games.csv"


# ============================================================
# 1. DATA LOADING
# ============================================================

def load_attackers(path=ATTACKER_FILE):
    """Loads attacker configurations from a CSV file."""
    attackers = []
    with open(path, newline="") as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            attackers.append({
                "id": int(r["id"]),
                "mot": r["mot"],
                "skill": r["skill"],
                "knowl": r["knowl"],
                "auto": r["auto"],
                "att": r["att"],
                "risk": r["risk"],
                "affil": r["affil"],
                "obj": r["obj"],
            })
    return attackers


def load_defenders(path=DEFENDER_FILE):
    """Loads defender configurations from a CSV file."""
    defenders = []
    with open(path, newline="") as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            defenders.append({
                "id": int(r["id"]),
                "w_eng": float(r["w_eng"]),
                "w_info": float(r["w_info"]),
                "w_prot": float(r["w_prot"]),
                "w_cost": float(r["w_cost"]),
                "res": int(r["res"]),
                "riskD": float(r["riskD"]),
            })
    return defenders


def load_environments(path=ENVIRONMENT_FILE):
    """Loads environment initial states from a CSV file."""
    envs = []
    with open(path, newline="") as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            envs.append({
                "id": int(r["id"]),
                "S1": float(r["S1"]),
                "S2": float(r["S2"]),
                "Sweetness": float(r["Sweetness"]),
                "C": float(r["C"]),
                "initial_p": float(r["initial_p"]),
                "asset_value_if_real": float(r["asset_value_if_real"]),
            })
    return envs


# ============================================================
# 2. GAME SUMMARY CALCULATION
# ============================================================

def summarize_game(game, attacker_type, defender_type, env_init):
    """
    Returns a list with the summary of a game:
    - Attacker, defender, and environment parameters
    - Game behavior
    - Useful labels to search for patterns and equilibrium
    """
    steps = len(game.attack_actions)
    first_action = game.attack_actions[0] if steps > 0 else None
    last_action = game.attack_actions[-1] if steps > 0 else None
    exit_early = int(first_action == "EXIT")

    # beliefs
    if game.belief_history:
        mean_p = sum(game.belief_history) / len(game.belief_history)
        final_p = game.belief_history[-1]
    else:
        mean_p = 0.0
        final_p = env_init["initial_p"]

    # attacker action counts
    counts = Counter(game.attack_actions)
    count_RECON = counts.get("RECON", 0)
    count_TEST = counts.get("TEST", 0)
    count_EXPLOIT = counts.get("EXPLOIT", 0)
    count_STEALTH = counts.get("STEALTH", 0)

    # most used MITRE main action by defender
    main_counts = Counter(m for (m, s) in game.defense_actions)
    top_mitre_main = main_counts.most_common(1)[0][0] if main_counts else None

    # "reasonable equilibrium" label (criteria can be adjusted)
    is_equilibrium_like = int(
        (steps >= 3) and
        (first_action != "EXIT") and
        (0.2 <= final_p <= 0.8)
    )

    row = [
        # IDs
        attacker_type["id"],
        defender_type["id"],
        env_init["id"],

        # Attacker type (summarized)
        attacker_type["mot"],
        attacker_type["skill"],
        attacker_type["risk"],
        attacker_type["att"],
        attacker_type["affil"],
        attacker_type["obj"],

        # Defender type (weights + resources)
        defender_type["w_eng"],
        defender_type["w_info"],
        defender_type["w_prot"],
        defender_type["w_cost"],
        defender_type["res"],
        defender_type["riskD"],

        # Environment (initial)
        env_init["S1"],
        env_init["S2"],
        env_init["Sweetness"],
        env_init["C"],
        env_init["initial_p"],
        env_init["asset_value_if_real"],

        # Game results
        steps,
        first_action,
        last_action,
        exit_early,
        mean_p,
        final_p,
        count_RECON,
        count_TEST,
        count_EXPLOIT,
        count_STEALTH,
        top_mitre_main,
        is_equilibrium_like,
    ]
    return row


# ============================================================
# 3. EXPERIMENT EXECUTION (MONTE CARLO SAMPLING)
# ============================================================

def run_experiments(
    n_games: int = 100000,
    max_steps_per_game: int = 5,
    results_path: str = RESULTS_FILE,
):
    """
    Launches n_games games, in each one randomly choosing:
    - an attacker
    - a defender
    - an environment

    No component is fixed: all participate in variability.
    A summary per game is saved in results_path.
    """

    print("=== Loading types ===")
    attackers = load_attackers()
    defenders = load_defenders()
    envs = load_environments()

    print(f"Attackers loaded: {len(attackers)}")
    print(f"Defenders loaded: {len(defenders)}")
    print(f"Environments loaded:  {len(envs)}")

    random.seed(42)

    # Header of results CSV
    header = [
        "attacker_id",
        "defender_id",
        "env_id",

        "mot",
        "skill",
        "risk",
        "att",
        "affil",
        "obj",

        "w_eng",
        "w_info",
        "w_prot",
        "w_cost",
        "res",
        "riskD",

        "S1",
        "S2",
        "Sweetness",
        "C",
        "initial_p",
        "asset_value_if_real",

        "steps",
        "first_action_A",
        "last_action_A",
        "exit_early",
        "mean_p_honey",
        "final_p_honey",
        "count_RECON",
        "count_TEST",
        "count_EXPLOIT",
        "count_STEALTH",
        "top_mitre_main",
        "is_equilibrium_like",
    ]

    with open(results_path, mode="w", newline="") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(header)

        for i in range(n_games):
            # Random sampling of the three components
            atk = random.choice(attackers)
            dfn = random.choice(defenders)
            env_init = random.choice(envs)

            # Create and run game
            game = Game(
                attacker_type=atk,
                defender_type=dfn,
                env_init=env_init,
                T=max_steps_per_game,
            )
            game.run()

            # Summarize the game and write to CSV
            row = summarize_game(game, atk, dfn, env_init)
            writer.writerow(row)

            if (i + 1) % 1000 == 0:
                print(f"  > Simulations completed: {i+1}/{n_games}")

    print(f"\n[OK] Simulations complete. Results in {results_path}")


# ============================================================
# 4. MAIN
# ============================================================

if __name__ == "__main__":
    # Adjust these values as you want more or less load
    run_experiments(
        n_games=100000,       # total number of games you want to simulate
        max_steps_per_game=5, # max T of your Game
        results_path=RESULTS_FILE,
    )
