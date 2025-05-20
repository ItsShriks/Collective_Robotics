import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from tqdm import tqdm
from matplotlib.colors import ListedColormap
import matplotlib.patches as patches
from matplotlib import gridspec

# Constants
GRID_SIZE = 50
NUM_OBJECTS = 200
NUM_AGENTS = 30
SENSE_RADIUS = 1
k_pick = 0.1
k_drop = 0.3
STEPS = 1000
ANTI_AGENT_COUNTS = [0, 5, 10, 15, 20]

# Define discrete color map
cmap = ListedColormap([
    'white',    # 0: empty
    'black',    # 1: object
    'red',      # 2: agent
    'blue',     # 3: anti-agent
    'orange',   # 4: agent carrying
    'cyan'      # 5: anti-agent carrying
])

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
    num_regular = NUM_AGENTS - num_anti_agents
    for _ in range(num_regular):
        x, y = np.random.randint(0, GRID_SIZE, 2)
        agents.append([x, y, False, False])  # x, y, carrying, is_anti
    for _ in range(num_anti_agents):
        x, y = np.random.randint(0, GRID_SIZE, 2)
        agents.append([x, y, False, True])

    frames = []

    for step in range(STEPS):
        display = np.copy(grid)

        for agent in agents:
            x, y, carrying, is_anti = agent
            f = local_density(x, y, grid)

            # Drop
            if carrying:
                p_drop = (k_drop**2 / (k_drop**2 + f**2)) if is_anti else (f**2 / (k_drop**2 + f**2))
                if grid[x, y] == 0 and np.random.rand() < p_drop:
                    grid[x, y] = 1
                    agent[2] = False
            else:
                # Pick
                if grid[x, y] == 1:
                    p_pick = (f**2 / (k_pick**2 + f**2)) if is_anti else (k_pick**2 / (k_pick**2 + f**2))
                    if np.random.rand() < p_pick:
                        grid[x, y] = 0
                        agent[2] = True

            # Move
            dx, dy = np.random.choice([-1, 0, 1]), np.random.choice([-1, 0, 1])
            agent[0] = (x + dx) % GRID_SIZE
            agent[1] = (y + dy) % GRID_SIZE

            # Color for visualization
            ax, ay = agent[0], agent[1]
            if carrying:
                display[ax, ay] = 4 if not is_anti else 5
            else:
                display[ax, ay] = 2 if not is_anti else 3

        if return_animation:
            frames.append(display.copy())

    return frames if return_animation else (compute_average_density(grid), grid)

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

# Run sweep
average_densities = []
final_grids = []
for num_anti in tqdm(ANTI_AGENT_COUNTS, desc="Sweeping Anti-Agent Counts"):
    density, final_grid = run_simulation(num_anti_agents=num_anti)
    average_densities.append(density)
    final_grids.append(final_grid)

# Plot average local densities
plt.figure()
plt.plot(ANTI_AGENT_COUNTS, average_densities, marker='o', color='purple')
plt.title("Average Local Density vs Anti-Agent Count")
plt.xlabel("Number of Anti-Agents")
plt.ylabel("Average Local Density")
plt.grid(True)
plt.savefig("./output/task_a.png")
plt.show()

# Save final grid image of best result
best_index = np.argmax(average_densities)
best_grid = final_grids[best_index]

plt.figure(figsize=(6, 6))
plt.imshow(best_grid, cmap=cmap, origin='lower', vmin=0, vmax=5)
plt.title(f"Final Clustering State (Anti-Agents = {ANTI_AGENT_COUNTS[best_index]})")
plt.axis('off')
plt.savefig("./output/task2_a_final.png")
plt.show()

# Plot final clustering states for all anti-agent counts with boxes
plt.figure(figsize=(15, 6))
cols = len(ANTI_AGENT_COUNTS)

for i, (count, grid) in enumerate(zip(ANTI_AGENT_COUNTS, final_grids)):
    ax = plt.subplot(1, cols, i + 1)
    ax.imshow(grid, cmap=cmap, origin='lower', vmin=0, vmax=5)
    ax.set_title(f"Anti-Agents = {count}")
    ax.axis('off')

    # Add rectangle (box) around each subplot
    rect = patches.Rectangle(
        (0, 0), 1, 1, transform=ax.transAxes,
        linewidth=2, edgecolor='gray', facecolor='none'
    )
    ax.add_patch(rect)

plt.suptitle("Final Clustering States for Different Anti-Agent Counts")
plt.tight_layout()
plt.subplots_adjust(top=0.85)
plt.savefig("./output/task2_a_all_final_states_boxed.png")
plt.show()


# Indices for best and worst cases
best_index = np.argmax(average_densities)
worst_index = np.argmin(average_densities)

# Get corresponding frames
frames_best = run_simulation(num_anti_agents=ANTI_AGENT_COUNTS[best_index], return_animation=True)
frames_worst = run_simulation(num_anti_agents=ANTI_AGENT_COUNTS[worst_index], return_animation=True)

# Determine the number of frames to sync both animations
num_frames = min(len(frames_best), len(frames_worst))

# Setup figure and subplots
fig = plt.figure(figsize=(12, 6))
gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

img1 = ax1.imshow(frames_best[0], cmap=cmap, origin='lower', vmin=0, vmax=5)
ax1.set_title(f"Best Clustering (Anti-Agents = {ANTI_AGENT_COUNTS[best_index]})")
ax1.axis('off')

img2 = ax2.imshow(frames_worst[0], cmap=cmap, origin='lower', vmin=0, vmax=5)
ax2.set_title(f"Worst Clustering (Anti-Agents = {ANTI_AGENT_COUNTS[worst_index]})")
ax2.axis('off')

def animate(i):
    img1.set_data(frames_best[i])
    img2.set_data(frames_worst[i])
    return [img1, img2]

ani = animation.FuncAnimation(fig, animate, frames=num_frames, interval=300, blit=True)

plt.tight_layout()
plt.show()