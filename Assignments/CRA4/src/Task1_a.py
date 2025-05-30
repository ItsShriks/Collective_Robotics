import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# Parameters
N = 20
C = 1.0
v_abs = 0.001
r = 0.045
P = 0.015
timesteps = 500

# Initialization
positions = np.random.rand(N)
velocities = np.random.choice([-v_abs, v_abs], size=N)

# Store data for animation and plotting
positions_over_time = []
velocities_over_time = []
left_counts = []

for t in range(timesteps):
    new_velocities = velocities.copy()

    for i in range(N):
        # Compute ring distances
        distances = np.abs(positions - positions[i])
        distances = np.minimum(distances, C - distances)

        # Find neighbors
        in_range = (distances <= r) & (np.arange(N) != i)
        left = np.sum(velocities[in_range] < 0)
        right = np.sum(velocities[in_range] > 0)

        # Majority rule
        if velocities[i] < 0 and right > left:
            new_velocities[i] = v_abs
        elif velocities[i] > 0 and left > right:
            new_velocities[i] = -v_abs

        # Spontaneous switch
        if np.random.rand() < P:
            new_velocities[i] *= -1

    velocities = new_velocities
    positions = (positions + velocities) % C

    # Store data
    positions_over_time.append(positions.copy())
    velocities_over_time.append(velocities.copy())
    left_counts.append(np.sum(velocities < 0))

# --- Animation ---
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')
circle = plt.Circle((0, 0), 1.0, color='gray', fill=False)
ax.add_artist(circle)
scat = ax.scatter([], [], s=80)

def init():
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    return scat,

def update(frame):
    pos = positions_over_time[frame]
    vel = velocities_over_time[frame]
    angles = 2 * np.pi * pos
    x = np.cos(angles)
    y = np.sin(angles)
    colors = ['red' if v < 0 else 'blue' for v in vel]
    scat.set_offsets(np.c_[x, y])
    scat.set_color(colors)
    ax.set_title(f'Time: {frame} | Left-going: {np.sum(vel < 0)}')
    return scat,

ani = animation.FuncAnimation(fig, update, frames=timesteps,
                              init_func=init, blit=True, interval=30, repeat=False)

# Show animation
#plt.show()

# --- Plot at the end ---
output_dir = "../output"
os.makedirs(output_dir, exist_ok=True)

# --- Save Animation ---
ani.save(os.path.join(output_dir, "task1_a.mp4"), fps=30, dpi=200)

# --- Save Final Plot ---
plt.figure(figsize=(10, 4))
plt.plot(left_counts, color='red')
plt.title('Number of left-going locusts over time')
plt.xlabel('Time step')
plt.ylabel('Count of left-going locusts')
plt.grid(True)
plt.tight_layout()
#plt.show()
plt.savefig(os.path.join(output_dir, "task1_a_plot.png"))
plt.close()
