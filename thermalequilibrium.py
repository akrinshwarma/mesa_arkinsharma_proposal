import mesa
import solara
import reacton.ipyvuetify as v
from matplotlib.figure import Figure
import matplotlib.colors as mcolors
import numpy as np

# --- Core Model Logic ---

class Molecule(mesa.Agent):
    def __init__(self, model, temperature):
        super().__init__(model)
        self.temperature = temperature

    def step(self):
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
        if neighbors:
            neighbor_avg = sum(n.temperature for n in neighbors) / len(neighbors)
            # Low conductivity: 10% thermal flux per step
            self.temperature += (neighbor_avg - self.temperature) * 0.1

class ConductionModel(mesa.Model):
    def __init__(self, width=12, height=12):
        super().__init__()
        self.grid = mesa.space.SingleGrid(width, height, torus=False)
        for x in range(width):
            for y in range(height):
                # Beta distribution creates "Extreme" initial states
                raw_val = self.random.betavariate(0.5, 0.5)
                temp = raw_val * 100.0
                agent = Molecule(self, temp)
                self.grid.place_agent(agent, (x, y))

    def step(self):
        self.agents.shuffle_do("step")

# --- Global Model Instance ---
model_internal = ConductionModel(12, 12)

# --- Custom Scientific Colormap ---
colors = ["#ADD8E6", "green", "red"]
thermal_cmap = mcolors.LinearSegmentedColormap.from_list("thermal_ice", colors)

@solara.component
def Page():
    step_count, set_step_count = solara.use_state(0)
    version, set_version = solara.use_state(0)

    def run_step():
        model_internal.step()
        set_step_count(step_count + 1)

    def generate_new_config():
        global model_internal
        model_internal = ConductionModel(12, 12)
        set_step_count(0)
        # Forcing a re-render even at step 0
        set_version(version + 1)

    with solara.Column(style={"padding": "20px", "max-width": "800px"}):
        solara.Title("Thermal Equilibrium: Extreme Initial Conditions")
        
        with solara.Row():
            solara.Button("Step Simulation", on_click=run_step, color="primary")
            solara.Button("New Configuration", on_click=generate_new_config, color="secondary")
        
        solara.Markdown(f"### Current Step: {step_count}")

        # --- RENDER BLOCK ---
        fig = Figure(figsize=(7, 6))
        ax = fig.subplots()
        
        agents = model_internal.agents
        x = np.array([a.pos[0] for a in agents])
        y = np.array([a.pos[1] for a in agents])
        temps = np.array([a.temperature for a in agents])
        
        sc = ax.scatter(x, y, c=temps, s=500, cmap=thermal_cmap, 
                        vmin=0, vmax=100, edgecolors='black', linewidth=0.8)
        
        cbar = fig.colorbar(sc, ax=ax)
        cbar.set_label('Temperature (°C)', rotation=270, labelpad=15)
        
        ax.set_xticks(range(12))
        ax.set_yticks(range(12))
        ax.set_title("Beta-Distributed Stochastic States")
        fig.tight_layout()

        # FIXED SYNTAX: We use solara.Div (or a plain solara.Column without extra args)
        # Using a standard solara container with a key works if we don't pass 'key' to FigureMatplotlib
        with solara.Div(key=f"plot-v{version}-s{step_count}"):
            with solara.Card():
                solara.FigureMatplotlib(fig)

page = Page()