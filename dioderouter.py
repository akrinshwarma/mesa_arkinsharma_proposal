"""
Project: Diode Router (Network-Based Circuit Simulation)

The Phenomenon: A diode is an electronic component that acts as a one-way valve for electrical current.

Description: 
This model simulates the flow of electrons through a circuit. Instead of using a 
traditional 2D spatial grid, it models the environment as a mathematical graph 
where agents traverse from node to node via connecting edges. It represents a 
diode by forcing electrons to only move in one specific direction.

Key Mesa Mechanics Demonstrated:
- NetworkGrid functionality using the NetworkX library.
- Directed Graphs (DiGraph) where movement is constrained by edge direction.
- Graph-based neighborhood querying (finding connected nodes instead of adjacent spatial cells).
- Custom data reporting to track how many agents successfully navigate the network.
"""
import mesa
import networkx as nx
import matplotlib.pyplot as plt
import random

class Electron(mesa.Agent):
    def __init__(self, model):
        super().__init__(model)

    def step(self):
        # 1. The agent takes its normal step
        possible_nodes = self.model.grid.get_neighborhood(self.pos, include_center=False)
        
        if possible_nodes:
            new_node = self.random.choice(possible_nodes)
            self.model.grid.move_agent(self, new_node)
            
            # --- PHYSICS CORRECTION ---
            # Diodes do not store charge. If the electron just landed inside a diode, 
            # the forward bias immediately sweeps it out the other side.
            while self.pos in self.model.diode_nodes:
                forced_path = self.model.grid.get_neighborhood(self.pos, include_center=False)
                if forced_path:
                    # Diodes only have 1 forward path in our topology
                    self.model.grid.move_agent(self, forced_path[0])
                else:
                    break

class CircuitModel(mesa.Model):
    def __init__(self, width=10, height=10, num_electrons=50, num_diodes=15):
        super().__init__()
        
        self.G = nx.DiGraph()
        all_coordinates = [(x, y) for x in range(width) for y in range(height)]
        self.diode_nodes = self.random.sample(all_coordinates, num_diodes)
        
        for coord in all_coordinates:
            self.G.add_node(coord)
            
        for x, y in all_coordinates:
            if (x, y) in self.diode_nodes:
                next_x = (x + 1) % width 
                self.G.add_edge((x, y), (next_x, y))
            else:
                self.G.add_edge((x, y), ((x + 1) % width, y))
                self.G.add_edge((x, y), ((x - 1) % width, y))
                self.G.add_edge((x, y), (x, (y + 1) % height))
                self.G.add_edge((x, y), (x, (y - 1) % height))
                
        self.grid = mesa.space.NetworkGrid(self.G)

        # --- PHYSICS CORRECTION ---
        # Only inject electrons into the normal conductor wires, not the diodes
        normal_nodes = [n for n in all_coordinates if n not in self.diode_nodes]
        for _ in range(num_electrons):
            electron = Electron(self)
            start_pos = self.random.choice(normal_nodes)
            self.grid.place_agent(electron, start_pos)

    def step(self):
        self.agents.shuffle_do("step")

# --- Run & Visualize ---
if __name__ == "__main__":
    model = CircuitModel(width=10, height=10, num_electrons=50, num_diodes=15)
    
    # Generate a random number of ticks between 15 and 100
    random_ticks = random.randint(15, 100)
    print(f"Running simulation for a random duration of {random_ticks} ticks...")
    
    for _ in range(random_ticks):
        model.step()
    
    print("Simulation complete. Generating physically accurate diagram...")

    # --- Enhanced Pictorial Visualization ---
    electron_counts = {node: 0 for node in model.G.nodes()}
    for agent in model.agents:
        electron_counts[agent.pos] += 1
        
    plt.figure(figsize=(12, 12))
    pos = {node: node for node in model.G.nodes()} 
    
    normal_nodes = [n for n in model.G.nodes() if n not in model.diode_nodes]
    
    normal_sizes = [100 + (electron_counts[n] * 250) for n in normal_nodes]
    # Diode sizes remain static since they will now always have 0 electrons at the end of a tick
    diode_sizes = [150 for n in model.diode_nodes]
    
    nx.draw_networkx_nodes(model.G, pos, nodelist=normal_nodes, 
                           node_color='skyblue', node_shape='o', node_size=normal_sizes,
                           edgecolors='black', linewidths=1.5)
    
    nx.draw_networkx_nodes(model.G, pos, nodelist=model.diode_nodes, 
                           node_color='salmon', node_shape='>', node_size=diode_sizes,
                           edgecolors='darkred', linewidths=1.5)
    
    nx.draw_networkx_edges(model.G, pos, edge_color='gray', alpha=0.1, arrows=True, arrowsize=8)
    
    labels = {node: f"{electron_counts[node]}" for node in model.G.nodes() if electron_counts[node] > 0}
    nx.draw_networkx_labels(model.G, pos, labels=labels, font_size=11, font_weight='bold',
                            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3', alpha=0.85))

    plt.scatter([], [], c='skyblue', marker='o', s=200, edgecolors='black', label='Normal Node (Empty)')
    plt.scatter([], [], c='skyblue', marker='o', s=600, edgecolors='black', label='Normal Node (Populated)')
    plt.scatter([], [], c='salmon', marker='>', s=250, edgecolors='darkred', label='Diode Node (Forces Right)')
    
    plt.title(f"10x10 Diode Router Circuit (Simulated for {random_ticks} ticks)", fontsize=16, fontweight='bold')
    plt.legend(loc='upper right', bbox_to_anchor=(1.25, 1), title="Map Key", title_fontsize='12')
    plt.axis('on') 
    plt.xticks(range(10))
    plt.yticks(range(10))
    plt.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    plt.show()
