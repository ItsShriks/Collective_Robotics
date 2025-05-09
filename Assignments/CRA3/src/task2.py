import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Parameters
GRID_SIZE = 50
NUM_OBJECTS = 200
NUM_AGENTS = 30
NUM_ANTI_AGENTS = 10
SENSE_RADIUS = 1
k_pick = 0.1
k_drop = 0.3

# Local density function
def local_density(x, y):
    count = 0
    for dx in range(-SENSE_RADIUS, SENSE_RADIUS + 1):
        for dy in range(-SENSE_RADIUS, SENSE_RADIUS + 1):
            nx, ny = (x + dx) % GRID_SIZE, (y + dy) % GRID_SIZE
            if grid[nx, ny] == 1:
                count += 1
    area = (2 * SENSE_RADIUS + 1) ** 2
    return count / area

# Initialize grid and agents
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
object_positions = random.sample([(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)], NUM_OBJECTS)
for pos in object_positions:
    grid[pos] = 1

agents = []
for _ in range(NUM_AGENTS):
    x, y = np.random.randint(0, GRID_SIZE, 2)
    agents.append([x, y, False, False])  # [x, y, carrying, is_anti]
for _ in range(NUM_ANTI_AGENTS):
    x, y = np.random.randint(0, GRID_SIZE, 2)
    agents.append([x, y, False, True])  # Anti-agent

# Animation setup
fig, ax = plt.subplots(figsize=(6, 6))
img = ax.imshow(grid, cmap='Blues', origin='lower')
ax.set_title("Object Clustering with Anti-Agents")
plt.axis('off')

def update(frame):
    global grid, agents
    for agent in agents:
        x, y, carrying, is_anti = agent
        f = local_density(x, y)

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

        # Random movement
        dx, dy = np.random.choice([-1, 0, 1]), np.random.choice([-1, 0, 1])
        agent[0] = (x + dx) % GRID_SIZE
        agent[1] = (y + dy) % GRID_SIZE

    img.set_data(grid)
    return [img]

# Run animation
ani = animation.FuncAnimation(fig, update, frames=200, interval=100, blit=True)
plt.show()
