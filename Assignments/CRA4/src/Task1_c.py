import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
# Parameters
N = 20
C = 1.0
v_abs = 0.001
r = 0.045
P = 0.015
timesteps = 500
runs = 100

# Initialize matrices
A = np.zeros((N + 1, N + 1), dtype=int)  # transition counts
M = np.zeros(N + 1, dtype=int)          # occurrence counts

# Run simulations
for run in tqdm(range(runs), desc="Running simulations"):
    positions = np.random.rand(N)
    velocities = np.random.choice([-v_abs, v_abs], size=N)
    left_count = np.sum(velocities < 0)

    for t in range(timesteps):
        new_velocities = velocities.copy()
        for i in range(N):
            distances = np.abs(positions - positions[i])
            distances = np.minimum(distances, C - distances)
            in_range = (distances <= r) & (np.arange(N) != i)
            left = np.sum(velocities[in_range] < 0)
            right = np.sum(velocities[in_range] > 0)

            if velocities[i] < 0 and right > left:
                new_velocities[i] = v_abs
            elif velocities[i] > 0 and left > right:
                new_velocities[i] = -v_abs

            if np.random.rand() < P:
                new_velocities[i] *= -1

        velocities = new_velocities
        positions = (positions + velocities) % C

        new_left_count = np.sum(velocities < 0)

        # Record transition and state count
        A[left_count][new_left_count] += 1
        M[left_count] += 1

        left_count = new_left_count

# Compute transition probabilities P[i][j] = A[i][j] / M[i]

transition_matrix = np.zeros_like(A, dtype=float)

# Replace further references:
for i in range(N + 1):
    if M[i] > 0:
        transition_matrix[i, :] = A[i, :] / M[i]

# --- Simulate Markov chain using transition_matrix ---
L_trajectory = []
L = np.random.randint(0, N + 1)  # initial state

for t in range(timesteps):
    L_trajectory.append(L)
    probs = transition_matrix[L]
    if probs.sum() == 0:  # no transition data; stay in place
        break
    L = np.random.choice(np.arange(N + 1), p=probs)


output_dir = "../output"
os.makedirs(output_dir, exist_ok=True)

# --- Plot L_trajectory (dimension-reduced model) ---
plt.figure(figsize=(10, 4))
plt.plot(L_trajectory, label='Simulated L(t) from Markov model', color='blue')
plt.xlabel('Time step')
plt.ylabel('Number of left-going locusts')
plt.title('Trajectory of L(t) using dimension-reduced Markov model')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "task1_c.png"))
plt.show()
