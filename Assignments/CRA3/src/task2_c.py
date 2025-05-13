from collections import deque
import matplotlib.pyplot as plt
import numpy as np
import random
from tqdm import tqdm

# PARAMETERS
GRID_SIZE = 50
NUM_OBJECTS = 200
NUM_AGENTS = 30
SENSE_RADIUS = 1
k_pick = 0.1
k_drop = 0.3
STEPS = 300
ANTI_AGENT_COUNTS = [0, 5, 10, 15, 20]
N_REPEATS = 5

def local_density(x, y, grid):
    count = 0
    for dx in range(-SENSE_RADIUS, SENSE_RADIUS + 1):
        for dy in range(-SENSE_RADIUS, SENSE_RADIUS + 1):
            nx, ny = (x + dx) % GRID_SIZE, (y + dy) % GRID_SIZE
            if grid[nx, ny] == 1:
                count += 1
    area = (2 * SENSE_RADIUS + 1) ** 2
    return count / area

def run_simulation(num_anti_agents):
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    object_positions = random.sample([(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)], NUM_OBJECTS)
    for pos in object_positions:
        grid[pos] = 1

    agents = []
    for _ in range(NUM_AGENTS):
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

    return grid

# Cluster analysis using BFS
def get_largest_cluster_size(grid):
    visited = np.zeros_like(grid, dtype=bool)
    max_size = 0

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i, j] == 1 and not visited[i, j]:
                queue = deque([(i, j)])
                size = 0
                while queue:
                    x, y = queue.popleft()
                    if visited[x, y]:
                        continue
                    visited[x, y] = True
                    size += 1
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = (x + dx) % GRID_SIZE, (y + dy) % GRID_SIZE
                            if grid[nx, ny] == 1 and not visited[nx, ny]:
                                queue.append((nx, ny))
                max_size = max(max_size, size)
    return max_size

# Sweep and measure
avg_sizes = []
std_sizes = []

for num_anti in tqdm(ANTI_AGENT_COUNTS, desc="Testing Anti-Agent Impact"):
    sizes = []
    for _ in range(N_REPEATS):
        final_grid = run_simulation(num_anti)
        max_cluster = get_largest_cluster_size(final_grid)
        sizes.append(max_cluster)
    avg_sizes.append(np.mean(sizes))
    std_sizes.append(np.std(sizes))

# Plot results
plt.figure(figsize=(8, 5))
plt.errorbar(ANTI_AGENT_COUNTS, avg_sizes, yerr=std_sizes, fmt='-o', capsize=5)
plt.title("Impact of Anti-Agent Percentage on Largest Cluster Size")
plt.xlabel("Number of Anti-Agents")
plt.ylabel("Largest Cluster Size")
plt.grid(True)
plt.savefig("../output/task2_c_cluster_size.png")
print("Graph saved to output/")
plt.show()
