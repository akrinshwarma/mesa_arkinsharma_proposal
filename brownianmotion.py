"""
Project: Brownian Motion (Gas Particle Simulation)

The Phenomenon: Brownian motion is the random, uncontrolled movement of microscopic particles suspended in a fluid (a liquid or a gas).

The Physics: Because atoms and molecules are constantly vibrating and moving (kinetic energy), they endlessly crash into each other. 
When a larger particle is suspended in this environment, it gets bombarded asymmetrically by these invisible molecules from all sides, causing it to jitter and zig-zag 
unpredictably. It was first observed by botanist Robert Brown looking at pollen in water, and later mathematically proven by Albert Einstein, confirming the existence of atoms.

Description: 
This model simulates the erratic, random movement of gas particles in a closed 
environment, demonstrating classical Brownian motion. Particles are placed on a 
2D grid and perform a random walk by moving to an adjacent cell during each time step.

Key Mesa Mechanics Demonstrated:
- MultiGrid functionality (allowing multiple agents to occupy the same cell).
- Toroidal space (the grid wraps around the edges like a sphere to prevent boundary effects).
- Stochastic agent movement using Mesa's built-in random number generator.
- DataCollector integration with NumPy to track the system's center of mass over time.
"""

import mesa
import numpy as np
import matplotlib.pyplot as plt

def compute_center_of_mass(model):
    # Use NumPy to efficiently calculate the mean X and Y coordinates
    positions = np.array([agent.pos for agent in model.agents])
    if len(positions) == 0:
        return (0, 0)
    return np.mean(positions, axis=0)

class GasParticle(mesa.Agent):
    def __init__(self, model):
        super().__init__(model)

    def step(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        if possible_steps:
            new_position = self.random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)

class GasChamberModel(mesa.Model):
    def __init__(self, N, width, height):
        super().__init__()
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, torus=True) 

        # Storage: DataCollector hooks into the model to save data every step
        self.datacollector = mesa.DataCollector(
            model_reporters={"Center_of_Mass": compute_center_of_mass}
        )

        for _ in range(self.num_agents):
            a = GasParticle(self)
            self.grid.place_agent(a, (self.random.randrange(width), self.random.randrange(height)))

    def step(self):
        self.datacollector.collect(self) # Save data BEFORE agents move
        self.agents.shuffle_do("step")

# --- Run & Visualize ---
if __name__ == "__main__":
    model = GasChamberModel(N=50, width=20, height=20)
    for _ in range(100):
        model.step()

    # Extract stored data as a Pandas DataFrame
    data = model.datacollector.get_model_vars_dataframe()
    
    # Visualization using Matplotlib
    x_coords = [pos[0] for pos in data["Center_of_Mass"]]
    y_coords = [pos[1] for pos in data["Center_of_Mass"]]
    
    plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='b')
    plt.title("Center of Mass Trajectory (100 Steps)")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.show()