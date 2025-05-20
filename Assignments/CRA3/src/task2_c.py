import numpy as np 
import matplotlib.pyplot as plt
import random
from scipy.ndimage import label
from tqdm import tqdm

# Constants
GRID_SIZE = 50
NUM_OBJECTS = 100
NUM_AGENTS = 50
SENSE_RADIUS = 1
k_pick_vals = [0.05, 0.1, 0.2]
k_drop_vals = [0.2, 0.3, 0.5]
STEPS = 500
ANTI_AGENT_COUNTS = [0, 5, 10, 15, 20]

REPEATS = 10

def local_density(x, y, grid):
    count = 0
    for dx in range(-SENSE_RADIUS, SENSE_RADIUS + 1):
        for dy in range(-SENSE_RADIUS, SENSE_RADIUS + 1):
            nx, ny = (x + dx) % GRID_SIZE, (y + dy) % GRID_SIZE
            if grid[nx, ny] == 1:
                count += 1
    area = (2 * SENSE_RADIUS + 1) ** 2
    return count / area

def largest_cluster_size(grid):
    structure = np.ones((3, 3), dtype=int)
    labeled, num_features = label(grid, structure=structure)
    if num_features == 0:
        return 0
    sizes = np.bincount(labeled.ravel())[1:]
    return sizes.max() if sizes.size > 0 else 0

def run_simulation(num_anti_agents, k_pick=0.05, k_drop=0.2):
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

    # Place objects randomly
    object_positions = random.sample([(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)], NUM_OBJECTS)
    for pos in object_positions:
        grid[pos] = 1

    # Initialize agents (x, y, carrying, is_anti)
    agents = []
    for _ in range(NUM_AGENTS - num_anti_agents):
        x, y = np.random.randint(0, GRID_SIZE, 2)
        agents.append([x, y, False, False])
    for _ in range(num_anti_agents):
        x, y = np.random.randint(0, GRID_SIZE, 2)
        agents.append([x, y, False, True])

    # Run simulation steps
    for step in range(STEPS):
        for agent in agents:
            x, y, carrying, is_anti = agent
            f = local_density(x, y, grid)

            if carrying:
                p_drop = (k_drop**2 / (k_drop**2 + f**2)) if is_anti else (f**2 / (k_drop**2 + f**2))
                if grid[x, y] == 0 and np.random.rand() < p_drop:
                    grid[x, y] = 1
                    agent[2] = False
            else:
                if grid[x, y] == 1:
                    p_pick = (f**2 / (k_pick**2 + f**2)) if is_anti else (k_pick**2 / (k_pick**2 + f**2))
                    if np.random.rand() < p_pick:
                        grid[x, y] = 0
                        agent[2] = True

            # Move agent - avoid no movement
            while True:
                dx, dy = np.random.choice([-1, 0, 1]), np.random.choice([-1, 0, 1])
                if dx != 0 or dy != 0:
                    break
            agent[0] = (x + dx) % GRID_SIZE
            agent[1] = (y + dy) % GRID_SIZE

    return largest_cluster_size(grid)


# Run experiments and collect results
results = {}
avg_clusters_all = {}

for k_pick in k_pick_vals:
    for k_drop in k_drop_vals:
        key = (k_pick, k_drop)
        results[key] = {}
        print(f"Running for k_pick={k_pick}, k_drop={k_drop}")
        for num_anti in tqdm(ANTI_AGENT_COUNTS, desc=f"k_pick={k_pick}, k_drop={k_drop}"):
            clusters = [run_simulation(num_anti_agents=num_anti, k_pick=k_pick, k_drop=k_drop) for _ in range(REPEATS)]
            results[key][num_anti] = clusters

        # Compute averages and std dev
        avg_clusters = [np.mean(results[key][n]) for n in ANTI_AGENT_COUNTS]
        std_clusters = [np.std(results[key][n]) for n in ANTI_AGENT_COUNTS]
        avg_clusters_all[key] = avg_clusters

        # Plot results for this parameter pair
        plt.figure()
        plt.errorbar(ANTI_AGENT_COUNTS, avg_clusters, yerr=std_clusters, fmt='o-', capsize=5)
        plt.title(f"Largest Cluster Size vs. Number of Anti-Agents\n(k_pick={k_pick}, k_drop={k_drop})")
        plt.xlabel("Number of Anti-Agents")
        plt.ylabel("Average Largest Cluster Size")
        plt.grid(True)
        plt.tight_layout()
        filename = f"anti_agent_performance_kpick{k_pick}_kdrop{k_drop}.png"
        plt.savefig(f"./output/{filename}")
        plt.show()

# Now plot all parameter pairs together
plt.figure(figsize=(10, 6))
for key, avg_clusters in avg_clusters_all.items():
    k_pick, k_drop = key
    plt.plot(ANTI_AGENT_COUNTS, avg_clusters, marker='o', label=f'k_pick={k_pick}, k_drop={k_drop}')
plt.title("Comparison of Largest Cluster Size for all (k_pick, k_drop)")
plt.xlabel("Number of Anti-Agents")
plt.ylabel("Average Largest Cluster Size")
plt.legend()
plt.grid(True)
plt.tight_layout()
combined_filename = "anti_agent_performance_all_k.png"
plt.savefig(f"./output/{combined_filename}")
plt.show()

# Find best (k_pick, k_drop) based on max average cluster size across anti-agent counts
best_key = max(avg_clusters_all, key=lambda k: max(avg_clusters_all[k]))
best_avg_clusters = avg_clusters_all[best_key]

print(f"Best parameters: k_pick={best_key[0]}, k_drop={best_key[1]} with max cluster size={max(best_avg_clusters):.2f}")

# Plot the best graph separately with error bars
best_std_clusters = [np.std(results[best_key][n]) for n in ANTI_AGENT_COUNTS]
plt.figure()
plt.errorbar(ANTI_AGENT_COUNTS, best_avg_clusters, yerr=best_std_clusters, fmt='o-', capsize=5, color='red')
plt.title(f"Best Largest Cluster Size vs. Number of Anti-Agents\n(k_pick={best_key[0]}, k_drop={best_key[1]})")
plt.xlabel("Number of Anti-Agents")
plt.ylabel("Average Largest Cluster Size")
plt.grid(True)
plt.tight_layout()
best_filename = f"best_anti_agent_performance_kpick{best_key[0]}_kdrop{best_key[1]}.png"
plt.savefig(f"./output/{best_filename}")
plt.show()
