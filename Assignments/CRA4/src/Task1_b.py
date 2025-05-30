import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm  # For progress bar
import os

# Parameters
N = 20
C = 1.0
v_abs = 0.001
r = 0.045
P = 0.015
timesteps = 500
runs = 1000

# Initialize 2D histogram A[Lt][Lt+1]
A = np.zeros((N + 1, N + 1), dtype=int)

# Simulation loop
for run in tqdm(range(runs), desc="Running simulations"):
    positions = np.random.rand(N)
    velocities = np.random.choice([-v_abs, v_abs], size=N)

    left_count = np.sum(velocities < 0)

    for t in range(timesteps):
        new_velocities = velocities.copy()
        for i in range(N):
            # Compute ring distances
            distances = np.abs(positions - positions[i])
            distances = np.minimum(distances, C - distances)
            in_range = (distances <= r) & (np.arange(N) != i)
            left = np.sum(velocities[in_range] < 0)
            right = np.sum(velocities[in_range] > 0)

            # Majority switch
            if velocities[i] < 0 and right > left:
                new_velocities[i] = v_abs
            elif velocities[i] > 0 and left > right:
                new_velocities[i] = -v_abs

            # Spontaneous switch
            if np.random.rand() < P:
                new_velocities[i] *= -1

        velocities = new_velocities
        positions = (positions + velocities) % C

        # Next left count
        new_left_count = np.sum(velocities < 0)

        # Record transition
        A[left_count][new_left_count] += 1
        left_count = new_left_count

# Plot heatmap
output_dir = "../output"
os.makedirs(output_dir, exist_ok=True)

plt.figure(figsize=(8, 6))
plt.imshow(A, origin='lower', cmap='viridis', interpolation='nearest')
plt.colorbar(label='Frequency of transitions')
plt.xlabel('Lt+1 (Next # of left-goers)')
plt.ylabel('Lt (Current # of left-goers)')
plt.title('Histogram of Lt → Lt+1 transitions over 1000 runs')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "task1_b.png"))
#plt.show()
