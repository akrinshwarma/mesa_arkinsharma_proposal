# Mesa GSoC 2026 Proposal: Agent-Based Physics Simulations
**Candidate:** Arkin Sharma  
**University:** MIT Bengaluru  

## 🚀 Project Overview
This repository contains a suite of Agent-Based Models (ABM) developed using the **Mesa** framework. These simulations are designed to demonstrate the application of ABM in physical and engineering systems, specifically focusing on thermodynamics and stochastic processes.

## 🛠️ Simulations Included
1. **Thermal Equilibrium:** - Explores the Second Law of Thermodynamics.
   - Uses a **Beta Distribution** for extreme initial entropy states.
   - Implements local kinetic energy exchange to simulate heat conduction.
2. **Brownian Motion:**
   - Simulates stochastic particle movement in a fluid medium.
3. **Diode Router:**
   - Agent-based logic applied to network routing and directional flow.

### What I Changed and Why

### . 	Deleted the "God Factory” mypyate_meta_agent):
The Problem:
 The old code used type() to invent new Python classes while the simulation was running and then forcefully copied variables (__dict__) from children to parents. This creates invisible bugs and makes type checking impossible.

The Fix:
 By requiring the user to explicitly subclass MetaAgent, your framework becomes vastly easier to test and maintain.

### . 	Fixed the Type Crash Bug in remove_constituting_agents:
The Problem:
 The old code tried to sort remaining meta-agents using lambda x: x.uniqueid or 0. If a user defined uniqueid as a string (e.g., "Agent_A"), Python would throw a TypeError trying to compare strings to integers.

The Fix:
 I replaced this with a deterministic set extraction (next(iter(...))) that won't crash regardless of what data type the unique_id is.

### . 	Encapsulated State Modification:

I created private methods (_register_child and _unregister_child) to handle the injection of the .meta_agents attribute onto the child agents. This keeps the messy "monkey-patching" logic contained in one place rather than scattered across the file.
Strict Type Hinting:

I upgraded all the type hints to use the modern typing. Type and collections.abc.Iterable. This will ensure the code passes mypy checks, which is a hard requirement for contributing to the core Mesa repository.

## 💻 Tech Stack
- **Engine:** Mesa (Python)
- **Frontend:** Solara, Reacton, ipyvuetify
- **Math/Viz:** NumPy, Matplotlib, NetworkX

## 🔧 Installation & Usage
To run these simulations locally:
1. Clone the repository and navigate to the branch:
   `git checkout proposal-draft`
2. Install dependencies:
   `pip install -r requirements.txt`
3. Run a simulation (e.g., Thermal Equilibrium):
   `solara run thermalequilibrium.py`