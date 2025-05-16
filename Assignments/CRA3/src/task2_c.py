import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.ndimage import label
from tqdm import tqdm

# Constants
GRID_SIZE = 50
NUM_OBJECTS = 200
NUM_AGENTS = 50
SENSE_RADIUS = 1
k_pick = 0.1
k_drop = 0.3
STEPS = 300  # Reduced for speed
ANTI_AGENT_COUNTS = [0, 2, 5, 8, 10]
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

def run_simulation(num_anti_agents):
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    object_positions = random.sample([(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)], NUM_OBJECTS)
    for pos in object_positions:
        grid[pos] = 1

    agents = []
    for _ in range(NUM_AGENTS - num_anti_agents):
        x, y = np.random.randint(0, GRID_SIZE, 2)
        agents.append([x, y, False, False])
    for _ in range(num_anti_agents):
        x, y = np.random.randint(0, GRID_SIZE, 2)
        agents.append([x, y, False, True])

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
            dx, dy = np.random.choice([-1, 0, 1]), np.random.choice([-1, 0, 1])
            agent[0] = (x + dx) % GRID_SIZE
            agent[1] = (y + dy) % GRID_SIZE

    return largest_cluster_size(grid)

# Run and collect results
results = {}
for num_anti in tqdm(ANTI_AGENT_COUNTS, desc="Testing Anti-Agent Percentages"):
    clusters = [run_simulation(num_anti_agents=num_anti) for _ in range(REPEATS)]
    results[num_anti] = clusters

# Plot average cluster size
avg_clusters = [np.mean(results[n]) for n in ANTI_AGENT_COUNTS]
std_clusters = [np.std(results[n]) for n in ANTI_AGENT_COUNTS]

plt.figure()
plt.errorbar(ANTI_AGENT_COUNTS, avg_clusters, yerr=std_clusters, fmt='o-', capsize=5)
plt.title("Largest Cluster Size vs. Number of Anti-Agents")
plt.xlabel("Number of Anti-Agents")
plt.ylabel("Average Largest Cluster Size")
plt.grid(True)
plt.savefig("anti_agent_performance.png")
plt.show()
