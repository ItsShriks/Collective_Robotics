import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
# --- PARAMETERS ---
N = 20
C = 1.0
v_abs = 0.001
r = 0.045
P_switch = 0.015
timesteps = 500
runs = 1000  # for better estimation of P matrix

# --- TASK 1: Full Simulation ---
positions = np.random.rand(N)
velocities = np.random.choice([-v_abs, v_abs], size=N)

left_counts = []

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

        if np.random.rand() < P_switch:
            new_velocities[i] *= -1

    velocities = new_velocities
    positions = (positions + velocities) % C
    left_counts.append(np.sum(velocities < 0))

# --- TASK 3: Build P matrix using many runs ---
A = np.zeros((N + 1, N + 1), dtype=int)
M = np.zeros(N + 1, dtype=int)

for run in tqdm(range(runs), desc="Building transition matrix"):
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

            if np.random.rand() < P_switch:
                new_velocities[i] *= -1

        velocities = new_velocities
        positions = (positions + velocities) % C

        new_left_count = np.sum(velocities < 0)

        A[left_count][new_left_count] += 1
        M[left_count] += 1

        left_count = new_left_count

# Normalize to get transition probabilities
P = np.zeros_like(A, dtype=float)
for i in range(N + 1):
    if M[i] > 0:
        P[i] = A[i] / M[i]

# --- Simulate Markov model using P ---
L_trajectory = []
L = np.random.randint(0, N + 1)

for t in range(timesteps):
    L_trajectory.append(L)
    probs = P[L]
    if probs.sum() == 0:
        break
    L = np.random.choice(np.arange(N + 1), p=probs)

output_dir = "../output"
os.makedirs(output_dir, exist_ok=True)

fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Top: Task 1 (Full Simulation)
axs[0].plot(left_counts, color='red')
axs[0].set_title('Task 1: Full Locust Simulation')
axs[0].set_ylabel('Left-Going Locusts')
axs[0].grid(True)

# Bottom: Task 3 (Markov Model)
axs[1].plot(L_trajectory, color='blue', linestyle='--')
axs[1].set_title('Task 3: Markov Model Simulation')
axs[1].set_xlabel('Time Step')
axs[1].set_ylabel('Left-Going Locusts')
axs[1].grid(True)

# plt.tight_layout()
# plt.show()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'task1_task3_individual_plots.png'))
plt.close()

# --- COMPARISON PLOT ---
plt.figure(figsize=(12, 5))
plt.plot(left_counts, label='Full Simulation (Task 1)', color='red', linewidth=2)
plt.plot(L_trajectory, label='Markov Model Simulation (Task 3)', color='blue', linestyle='--', linewidth=2)
plt.xlabel('Time Step')
plt.ylabel('Number of Left-Going Locusts')
plt.title('Comparison: Full Simulation vs. Markov Model')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'task1_task3_comparison.png'))
#plt.show()
