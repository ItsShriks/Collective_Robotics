import numpy as np
import matplotlib.pyplot as plt

C = 0.5        # Length of the circular track
v = 0.01       # Velocity of agents per timestep
r = 0.045      # Interaction radius
N = 50         # Number of agents
P = 0.15       # Probability of random direction flip
T_warmup = 100 # Timesteps to reach steady state before measurement
T_measure = 20 # Number of timesteps to measure ΔL after warmup
runs = 50000   # Number of simulation runs to average over

# -----------------------------
# Preallocate result accumulators
# -----------------------------
delta_sum = np.zeros(N + 1)  # Sum of ΔL values for each possible L (number of left-goers)
count = np.zeros(N + 1)      # Count of observations for each L

# -----------------------------
# Main Simulation Loop
# -----------------------------
for run in range(runs):
    # Initialize agents with random positions on the ring [0, C)
    positions = np.random.uniform(0, C, N)

    # Random initial directions: -1 (left) or 1 (right)
    directions = np.random.choice([-1, 1], N)

    # Initial number of agents going left
    L_prev = np.count_nonzero(directions == -1)

    for t in range(T_warmup + T_measure):
        # Compute pairwise circular distances between all agents
        pos_diff = positions[:, None] - positions
        distances = np.abs(pos_diff)
        distances = np.minimum(distances, C - distances)  # Handle circular boundary

        # -----------------------------
        # Update directions based on neighbor influence
        # -----------------------------
        influence = np.zeros(N)
        for i in range(N):
            neighbors = distances[i] <= r  # Neighbors within interaction radius
            local_sum = np.sum(directions[neighbors])  # Net direction of neighbors

            # Update direction with probabilistic rule
            if np.random.rand() < P:
                influence[i] = -directions[i]  # Random flip
            elif local_sum != 0:
                influence[i] = np.sign(local_sum)  # Follow majority direction
            else:
                influence[i] = directions[i]  # Keep same direction

        # Update directions and positions
        directions = influence.astype(int)
        positions = (positions + v * directions) % C  # Move and wrap around circle

        # -----------------------------
        # Measurement Phase
        # -----------------------------
        L_curr = np.count_nonzero(directions == -1)  # Current number of left-goers

        if t >= T_warmup:
            delta = L_curr - L_prev  # Change in number of left-goers
            delta_sum[L_prev] += delta  # Accumulate ΔL
            count[L_prev] += 1          # Count how many times L_prev occurred

        L_prev = L_curr  # Update for next timestep

# Avoid division by zero
nonzero_mask = count > 0
L_vals = np.arange(N + 1)[nonzero_mask]          # L values with nonzero measurements
avg_deltaL = delta_sum[nonzero_mask] / count[nonzero_mask]  # Compute average ΔL


# Save Results to File

with open("L_of_L.txt", "w") as f:
    for L, dL in zip(L_vals, avg_deltaL):
        f.write(f"{L} {dL}\n")

plt.figure(figsize=(8, 5))
plt.plot(L_vals, avg_deltaL, marker='o')
plt.axhline(0, color='black', linestyle='--')  # Reference line at ΔL = 0
plt.xlabel("L (Number of Left-Goers)")
plt.ylabel("ΔL(L) (Average Change in L)")
plt.title("Average Change ΔL(L) vs L")
plt.grid(True)
plt.savefig("../output/task1_1_plot.png", dpi=300)
plt.close()  # Close the figure to free memory
