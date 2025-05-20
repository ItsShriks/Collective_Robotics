import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Parameters
GRID_SIZE = 50
NUM_AGENTS = 40
NUM_ANTI_AGENTS = 5
SENSE_RADIUS = 1
CLUSTER_THRESHOLD = 4  # If local robot density exceeds this, agent is in a "cluster"
TOTAL_STEPS = 200

# Initialize grid and agents
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
agents = []

# Create normal agents
for _ in range(NUM_AGENTS):
    x, y = np.random.randint(0, GRID_SIZE, 2)
    agents.append({'x': x, 'y': y, 'is_anti': False, 'ordered_to_leave': False})

# Create anti-agents
for _ in range(NUM_ANTI_AGENTS):
    x, y = np.random.randint(0, GRID_SIZE, 2)
    agents.append({'x': x, 'y': y, 'is_anti': True})

def local_density(x, y, agents):
    count = 0
    for other in agents:
        if other['is_anti']:
            continue
        dx = min(abs(x - other['x']), GRID_SIZE - abs(x - other['x']))
        dy = min(abs(y - other['y']), GRID_SIZE - abs(y - other['y']))
        if dx <= SENSE_RADIUS and dy <= SENSE_RADIUS:
            count += 1
    return count

def move_randomly(agent):
    dx, dy = np.random.choice([-1, 0, 1]), np.random.choice([-1, 0, 1])
    agent['x'] = (agent['x'] + dx) % GRID_SIZE
    agent['y'] = (agent['y'] + dy) % GRID_SIZE

# Visualization setup
fig, ax = plt.subplots(figsize=(6, 6))
img = ax.imshow(grid, cmap='gray', origin='lower', vmin=0, vmax=2)
ax.set_title("Swarm Aggregation with Anti-Agents")
plt.axis('off')

def update(frame):
    global agents, grid

    grid[:] = 0  # Clear grid

    # Step 1: Anti-agents broadcast "leave" command
    for agent in agents:
        if agent['is_anti']:
            # Sense surrounding area and find agents in dense clusters
            for other in agents:
                if not other['is_anti']:
                    dx = min(abs(agent['x'] - other['x']), GRID_SIZE - abs(agent['x'] - other['x']))
                    dy = min(abs(agent['y'] - other['y']), GRID_SIZE - abs(agent['y'] - other['y']))
                    if dx <= SENSE_RADIUS and dy <= SENSE_RADIUS:
                        density = local_density(other['x'], other['y'], agents)
                        if density >= CLUSTER_THRESHOLD:
                            other['ordered_to_leave'] = True

    # Step 2: Move agents
    for agent in agents:
        if agent['is_anti']:
            move_randomly(agent)
        else:
            density = local_density(agent['x'], agent['y'], agents)

            if agent.get('ordered_to_leave', False):
                move_randomly(agent)
                agent['ordered_to_leave'] = False
            elif density < CLUSTER_THRESHOLD:
                # In sparse area: move randomly to seek clusters
                move_randomly(agent)
            else:
                # In cluster: stay put
                pass

        # Mark agent's position on grid
        if agent['is_anti']:
            grid[agent['x'], agent['y']] = 2  # Anti-agent
        else:
            grid[agent['x'], agent['y']] = 1  # Normal agent

    img.set_data(grid)
    return [img]

# Animate
ani = animation.FuncAnimation(fig, update, frames=TOTAL_STEPS, interval=100, blit=True)
ani.save("./output/task2_b.gif", writer='pillow', fps=10)
print("Animation video saved to output")
plt.show()
