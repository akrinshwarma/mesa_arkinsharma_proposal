# Mesa GSoC 2026: Agent-Based Physics & Engineering Simulations
**Candidate:** Arkin Sharma  
**University:** MIT Bengaluru  
**Project Status:** GSoC 2026 Proposal Implementation

## 🚀 Project Overview
This repository contains a suite of high-performance Agent-Based Models (ABM) developed using the **Mesa** framework. The project demonstrates the application of ABM in simulating stochastic physical processes and solving engineering-specific architectural challenges in reactive web environments.

---

## 🧱 Mesa Implementation Architecture

For those unfamiliar with Agent-Based Modeling (ABM), this project utilizes the three core pillars of the **Mesa** ecosystem to simulate complex physical systems:

### 1. The Agent Logic (`Mesa.Agent`)
Each particle or network packet is an independent actor.
* **Autonomous Behavior:** Instead of a global loop, I defined a `step()` method inside the agent. Each agent "decides" how to transfer energy or move based on local conditions.
* **State Management:** Agents carry properties like `energy`, `velocity`, and `mass` which update dynamically.

### 2. The Model Environment (`Mesa.Model`)
The model acts as the "Universe" managing the agents.
* **Space & Grids:** Uses `ContinuousSpace` for fluid dynamics and `MultiGrid` for thermal models, allowing multiple agents to occupy specific coordinates.
* **The Scheduler:** Implements `RandomActivation`. This ensures that in every "tick," every agent acts in a randomized order to prevent computational bias.
* **DataCollection:** Utilizes the `DataCollector` to poll the simulation state, exporting data into NumPy arrays for real-time graphing.

### 3. The Execution Flow (How it runs)
1.  **Instantiation:** The `Model` class creates $N$ agents.
2.  **The Step Loop:** The UI calls `model.step()`, triggering the scheduler.
3.  **Interaction:** Agents execute their `step()` logic (e.g., colliding or exchanging heat).
4.  **UI Sync:** **Solara** detects the state change and re-renders the visualization.

---

## 🛠️ Simulations Included

### 1. Thermal Equilibrium (`thermalequilibrium.py`)
* **Phenomenon:** The Second Law of Thermodynamics and the progression toward maximum entropy.
* **Physics:** Simulates local kinetic energy exchange. Uses a **Beta Distribution** ($\alpha=0.5, \beta=0.5$) for initialization to simulate extreme energy gradients.
* **Mesa Mechanics:** Custom energy-transfer step logic integrated with vectorized Matplotlib rendering.

### 2. Brownian Motion (`brownian_motion.py`)
* **Phenomenon:** Random, uncontrolled movement of microscopic particles in a fluid.
* **Physics:** Classical random walks where particles move to adjacent cells in a 2D grid based on stochastic vectors.
* **Mesa Mechanics:** `MultiGrid` and **Toroidal space** (spherical wrapping) to prevent boundary effects.

### 3. Diode Router
* **Phenomenon:** One-way directional flow in a network.
* **Logic:** Simulates routing constraints akin to a semiconductor diode.
* **Mesa Mechanics:** Integrated with **NetworkX** for graph-based navigation.

---

## 🧬 Evolution of `base.py`: Framework Refactoring

The core `base.py` was refactored from a proof-of-concept into a production-grade framework:

* **Deprecated the "God Factory":** Removed legacy `type()` dynamic class generation. Introduced the `MetaAgent` base class to restore Python’s Method Resolution Order (MRO), enabling IDE autocompletion and `mypy` type-checking.
* **Sorting Stability:** Replaced unstable lambda sorting with **deterministic set extraction**, allowing the framework to handle any `unique_id` type (Int, String, or UUID) without crashes.
* **UI Reactivity:** Solved Solara "Step 0" refresh stalls by implementing a `version` state-tracking toggle and `ipyvuetify` (`v.Div`) wrappers to force DOM re-mounting.

---

## 💻 Technical Stack
* **Language:** Python 3.11+
* **Engine:** Mesa
* **Frontend:** Solara, Reacton, ipyvuetify
* **Mathematics:** NumPy, NetworkX
* **Visualization:** Matplotlib

## 🔧 Installation & Usage
1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/akrinshwarma/mesa_arkinsharma_proposal.git](https://github.com/akrinshwarma/mesa_arkinsharma_proposal.git)
    cd mesa_arkinsharma_proposal
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run Simulation:**
    ```bash
    solara run thermalequilibrium.py
    ```

---

## 📖 Beginner's Guide: How to Experiment
* **Change Density:** Adjust the `N` slider in the Solara sidebar.
* **Modify Physics:** Open `thermalequilibrium.py` and edit the `exchange_energy` method in the `ThermalAgent` class.
* **Track New Data:** Add a new entry to the `model_reporters` in the `DataCollector`.
