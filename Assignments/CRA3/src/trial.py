import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from tqdm import tqdm

# Constants
GRID_SIZE = 50
NUM_OBJECTS = 200
NUM_AGENTS = 30
SENSE_RADIUS = 1
k_pick = 0.1
k_drop = 0.3
STEPS = 200
ANTI_AGENT_COUNTS = [0, 5, 10, 15, 20]

# Local density function
def local_density(x, y, grid):
    count = 0
    for dx in range(-SENSE_RADIUS, SENSE_RADIUS + 1):
        for dy in range(-SENSE_RADIUS, SENSE_RADIUS + 1):
            nx, ny = (x + dx) % GRID_SIZE, (y + dy) % GRID_SIZE
            if grid[nx, ny] == 1:
                count += 1
    area = (2 * SENSE_RADIUS + 1) ** 2
    return count / area

# Simulation function
def run_simulation(num_anti_agents, return_animation=False):
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

    frames = []

    for step in range(STEPS):
        display = np.copy(grid).astype(float)

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

            # Overlay agent colors
            if carrying:
                display[agent[0], agent[1]] = 0.7 if not is_anti else 0.9  # Regular: gray, Anti: light violet
            else:
                display[agent[0], agent[1]] = 0.3 if not is_anti else 0.6  # Regular: greenish, Anti: violet

        if return_animation:
            frames.append(display.copy())

    return frames if return_animation else compute_average_density(grid)

# Evaluation: average local density
def compute_average_density(grid):
    total_density = 0
    count = 0
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x, y] == 1:
                total_density += local_density(x, y, grid)
                count += 1
    return total_density / count if count > 0 else 0

# Main simulation loop with parameter sweep
average_densities = []
for num_anti in tqdm(ANTI_AGENT_COUNTS, desc="Sweeping Anti-Agent Counts"):
    density = run_simulation(num_anti_agents=num_anti)
    average_densities.append(density)

# Plot comparison
plt.figure()
plt.plot(ANTI_AGENT_COUNTS, average_densities, marker='o')
plt.title("Average Local Density vs Anti-Agent Count")
plt.xlabel("Number of Anti-Agents")
plt.ylabel("Average Local Density")
plt.grid(True)
plt.savefig("../output/task2_a.png")
plt.show()

# Run one animation for the best anti-agent setting (optional)
best_index = np.argmax(average_densities)
best_anti_agents = ANTI_AGENT_COUNTS[best_index]
frames = run_simulation(num_anti_agents=best_anti_agents, return_animation=True)

# Create animation
fig, ax = plt.subplots(figsize=(6, 6))
img = ax.imshow(frames[0], cmap='Blues', origin='lower')
ax.set_title(f"Object Clustering (Anti-Agents = {best_anti_agents})")
plt.axis('off')

def animate(i):
    img.set_data(frames[i])
    return [img]

ani = animation.FuncAnimation(fig, animate, frames=len(frames), interval=100, blit=True)
ani.save("../output/task2_a.mp4", writer='ffmpeg', fps=10)
plt.show()
