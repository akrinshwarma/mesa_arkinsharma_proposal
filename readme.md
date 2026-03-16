# Mesa GSoC 2026 Proposal: Agent-Based Physics Simulations
**Candidate:** Arkin Sharma  
**University:** MIT Bengaluru  

## 🚀 Project Overview
This repository contains a suite of Agent-Based Models (ABM) developed using the **Mesa** framework. These simulations demonstrate the application of ABM in physical and engineering systems, focusing on thermodynamics, stochastic processes, and reactive UI architecture.

## 🛠️ Simulations Included

### 1. Thermal Equilibrium (`base.py`)
- **Physics Engine:** Explores the Second Law of Thermodynamics through local kinetic energy exchange.
- **Stochastic Initial States:** Replaced standard uniform distributions with a **Beta Distribution** ($\alpha=0.5, \beta=0.5$) to simulate extreme initial entropy.
- **High-Performance Rendering:** Implements **vectorized Matplotlib scatter plots** to maintain high frame rates during complex particle interactions.
- **Reactivity Fix:** Resolved a critical Solara "Step 0" refresh bug by implementing a `version` state-tracking system and using `ipyvuetify` (`v.Div`) to force component re-mounting.

### 2. Brownian Motion
- **Stochastic Dynamics:** Simulates random particle jitter in a fluid medium using Mesa's continuous space.

### 3. Diode Router
- **Network Logic:** Applies agent-based logic to directional flow and routing within a node-based graph using **NetworkX**.

---

## 🔧 Engineering & Architectural Fixes (MetaAgent Logic)

To prepare this framework for a GSoC-level contribution, I performed a significant refactor of the core agent logic to ensure it meets the strict stability requirements of the Mesa ecosystem.

### 1. Deprecated Dynamic Class Generation (The "God Factory")
- **The Problem:** The legacy code used `type()` to dynamically invent Python classes at runtime and forcefully copied `__dict__` attributes between objects. This bypassed Python’s inheritance model and made the code impossible to debug.
- **The Fix:** Shifted to an explicit subclassing model. Users now subclass `MetaAgent`, making the framework vastly more predictable and compatible with IDE autocompletion.

### 2. Resolved Type Erasure in Sorting
- **The Problem:** The `remove_constituting_agents` function used a sorting lambda (`lambda x: x.uniqueid or 0`) that would crash with a `TypeError` if `unique_id` was a string instead of an integer.
- **The Fix:** Implemented a deterministic set extraction (`next(iter(...))`) that handles any `unique_id` data type without risk of comparison crashes.

### 3. State Encapsulation & Monkey-Patching Safety
- **The Fix:** Introduced private methods (`_register_child` and `_unregister_child`) to manage how `.meta_agents` attributes are injected into child agents. This encapsulates the "monkey-patching" logic, protecting the global state.

### 4. Modern Type Hinting (Mypy Compliance)
- **The Fix:** Upgraded all type hints to use `typing.Type` and `collections.abc.Iterable`. This ensures the codebase passes rigorous **mypy** checks, a prerequisite for core Mesa contributions.

---

## 💻 Tech Stack
- **Engine:** Mesa (Python)
- **Frontend:** Solara, Reacton, ipyvuetify
- **Math/Viz:** NumPy, Matplotlib, NetworkX

## 🔧 Installation & Usage
1. Clone the repository and navigate to the branch:
   `git checkout proposal-draft`
2. Install dependencies:
   `pip install -r requirements.txt`
3. Run the primary simulation:
   `solara run thermalequilibrium.py`