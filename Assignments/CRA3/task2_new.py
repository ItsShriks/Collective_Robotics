import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Parameters
GRID_SIZE = 30
NUM_OBJECTS = 100
NUM_ANTI_AGENTS = 20
SENSE_RADIUS = 1
k_pick = 0.1
k_drop = 0.3

# Color definitions
COLORS = {
    0: (1, 1, 1),        # Empty - white
    1: (0.2, 0.4, 0.9),  # Object - blue
    3: (1.0, 0.2, 0.2),  # Anti-agent - red
    4: (1.0, 0.8, 0.0)   # Anti-agent carrying object - yellow
}

# Local density calculation
def local_density(x, y, grid):
    count = 0
    for dx in range(-SENSE_RADIUS, SENSE_RADIUS + 1):
        for dy in range(-SENSE_RADIUS, SENSE_RADIUS + 1):
            nx, ny = (x + dx) % GRID_SIZE, (y + dy) % GRID_SIZE
            if grid[nx, ny] == 1:
                count += 1
    area = (2 * SENSE_RADIUS + 1) ** 2
    return count / area

# Initialize grid
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
object_positions = random.sample([(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)], NUM_OBJECTS)
for pos in object_positions:
    grid[pos] = 1

# Anti-Agents only: [x, y, carrying, is_anti=True]
agents = []
for _ in range(NUM_ANTI_AGENTS):
    x, y = np.random.randint(0, GRID_SIZE, 2)
    agents.append([x, y, False, True])

# Fancy color grid
def get_color_grid(grid, agents):
    color_grid = np.zeros((GRID_SIZE, GRID_SIZE, 3))
    color_grid[:, :] = COLORS[0]  # background
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i, j] == 1:
                color_grid[i, j] = COLORS[1]  # object
    for agent in agents:
        x, y, carrying, _ = agent
        color_grid[x, y] = COLORS[4] if carrying else COLORS[3]
    return color_grid

# Plot setup
fig, ax = plt.subplots(figsize=(7, 7))
img = ax.imshow(get_color_grid(grid, agents), origin='lower')
ax.set_title("Object Clustering with Only Anti-Agents", fontsize=16, fontweight='bold')
plt.axis('off')

# Update function
def update(frame):
    global grid, agents
    for agent in agents:
        x, y, carrying, is_anti = agent
        f = local_density(x, y, grid)

        if carrying:
            p_drop = k_drop**2 / (k_drop**2 + f**2)
            if grid[x, y] == 0 and np.random.rand() < p_drop:
                grid[x, y] = 1
                agent[2] = False
        else:
            if grid[x, y] == 1:
                p_pick = f**2 / (k_pick**2 + f**2)
                if np.random.rand() < p_pick:
                    grid[x, y] = 0
                    agent[2] = True

        dx, dy = np.random.choice([-1, 0, 1]), np.random.choice([-1, 0, 1])
        agent[0] = (x + dx) % GRID_SIZE
        agent[1] = (y + dy) % GRID_SIZE

    img.set_data(get_color_grid(grid, agents))
    return [img]

# Faster Animation
ani = animation.FuncAnimation(fig, update, frames=300, interval=100, blit=True)
plt.tight_layout()
plt.show()
