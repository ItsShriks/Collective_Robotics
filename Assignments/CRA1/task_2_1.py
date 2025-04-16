import numpy as np
import matplotlib.pyplot as plt

# --------------------------
# Parameters
# --------------------------
N = 250                      # Number of fireflies
L = 50                       # Flashing cycle length
T = 5000                     # Number of simulation time steps
r_values = [0.05, 0.1, 0.5, 1.4]  # Vicinity distances

# --------------------------
# Initialize firefly positions (randomly in 1x1 square)
# --------------------------
positions = np.random.rand(N, 2)  # Each row = (x, y)

# --------------------------
# Get neighbors within distance r
# --------------------------
def compute_neighbors(r):
    neighbors = [[] for _ in range(N)]
    for i in range(N):
        for j in range(i + 1, N):
            dist = np.linalg.norm(positions[i] - positions[j])
            if dist < r:
                neighbors[i].append(j)
                neighbors[j].append(i)
    avg_neighbors = np.mean([len(nlist) for nlist in neighbors])
    return neighbors, avg_neighbors

# --------------------------
# Simulate firefly behavior for a given r
# --------------------------
def run_simulation(r):
    neighbors, avg_neighbors = compute_neighbors(r)
    clocks = np.random.randint(0, L, size=N)  # Random initial phases
    flash_counts = []

    for t in range(T):
        is_flashing = clocks < (L // 2)
        flash_counts.append(np.sum(is_flashing))

        new_clocks = (clocks + 1) % L  # Default clock advance

        for i in range(N):
            if not is_flashing[i] and neighbors[i]:
                flashing_neighbors = np.sum(is_flashing[neighbors[i]])
                if flashing_neighbors > len(neighbors[i]) / 2:
                    # Advance clock by 1 (i.e., flash 1 step earlier next cycle)
                    new_clocks[i] = (clocks[i] + 1) % L

        clocks = new_clocks  # Update clocks

    return flash_counts, avg_neighbors

# --------------------------
# Run simulation for all r values and plot
# --------------------------
plt.figure(figsize=(14, 8))

for r in r_values:
    print(f"Running simulation for r = {r}")
    flash_counts, avg_neighbors = run_simulation(r)
    plt.plot(flash_counts, linewidth=2, label=f"r = {r}, avg_neighbors ≈ {avg_neighbors:.2f}")

# Add vertical dashed lines every L steps
for cycle_start in range(0, T, L):
    plt.axvline(x=cycle_start, color='gray', linestyle='--', linewidth=0.5)

# Optional: Highlight region where synchronization is visible
# You can change 1000 to another time where you notice stable peaks
plt.axvspan(1000, 5000, color='yellow', alpha=0.1, label='Synchronized region (example)')

# --------------------------
# Plot settings
# --------------------------
plt.title("Firefly Synchronization Over Time")
plt.xlabel("Time Step")
plt.ylabel("Number of Flashing Fireflies")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
