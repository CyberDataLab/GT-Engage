# GT-Engage: Cyber Deception Simulator based on Game Theory and the MITRE Engage Framework

**GT-Engage** is a cybersecurity simulation framework designed to model and analyze the strategic interaction between a defender and an attacker in a dynamic network environment. The project integrates the mathematical rigor of **Incomplete Information Game Theory** (Hypergames) with the tactical applicability of the **MITRE Engage** framework.

The simulator transforms a static network into a hostile environment for an intruder by strategically deploying deception signals, thereby increasing adversary uncertainty and exhausting their cognitive and temporal resources.

## 🧠 Scientific Foundations

The model is based on the principles detailed in the original research:

* **Hypergame Modeling:** Captures scenarios where the attacker and the defender operate with different subjective perceptions of the available strategies and outcomes.
* **Bayesian Inference:** The attacker uses an inference engine to update their belief ($b_t$) regarding whether an asset is real or a decoy, based on noisy technical signals.
* **Technical Signaling:** Implements deep technical mimicry by manipulating physical variables such as latency, jitter, and service banner consistency to degrade adversary confidence.

## 📂 Project Structure

The implementation is written in Python 3.9+ following an Object-Oriented Programming (OOP) paradigm.

### Source Code Files (.py)

* **`main.py`**: The orchestration engine. It handles data loading from CSVs, manages the simulation loop (Monte Carlo sampling), and exports the detailed results.
* **`game.py`**: The core game engine (CPD-GAME v3). It governs turn-based logic, agent interactions, and the calculation of expected and realized utilities (payoffs).
* **`attacker.py`**: Defines the `Attacker` agent. It includes profiles (from Script Kiddies to APTs), epsilon-greedy decision-making logic, and risk aversion parameters.
* **`defender.py`**: Defines the `Defender` agent. It implements action selection based on MITRE Engage tactics, managing action fatigue and lightweight learning about attacker behavior.
* **`environment.py`**: Models the physical state of the network and assets. It calculates asset values and the probability of an attacker falling into a trap.
* **`signals.py`**: Responsible for generating noisy signals (latency, jitter, VM fingerprints) and implementing the Bayesian belief update logic for the attacker.
* **`mitre_effects.py`**: Contains the full MITRE Engage action catalog and defines how each action numerically perturbs signals and the environment state.
* **`utils.py`**: Provides auxiliary mathematical functions such as value clipping, entropy calculation, and safe means for data analysis.

### Data Configuration Files (.csv)

* **`attacker_types.csv`**: Input file defining attacker profiles, including motivation, skill level, technical knowledge, and risk aversion.
* **`defender_types.csv`**: Input file for defender configurations, specifying strategic weights for engagement, information gathering, and protection.
* **`environment_initial_states.csv`**: Defines initial asset conditions and the baseline noise level of the network infrastructure.
* **`test_results.csv`**: Output file where simulation steps, actions taken, belief evolution, and obtained utilities are recorded for analysis.

## 🛠️ Requirements and Installation

### Technical Requirements
* **Python**: 3.9 or higher.
* **Libraries**: `numpy` (for stochastic operations) and `pandas` (recommended for data analysis).

### Installation
1.  Clone the repository:
    ```bash
    git clone [https://github.com/your-user/GT-Engage.git](https://github.com/your-user/GT-Engage.git)
    cd GT-Engage
    ```
2.  Install dependencies:
    ```bash
    pip install numpy pandas
    ```

## ▶️ Execution and Configuration

Run the simulator using the main script:

```bash
python main.py
