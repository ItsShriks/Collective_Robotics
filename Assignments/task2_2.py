import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# Parameters
# -------------------------
N = 250
L = 50
T = 5000
r_values = np.arange(0.025, 1.425, 0.025)
num_runs = 50

# -------------------------
# Generate firefly positions once for each run
# -------------------------
def generate_positions():
    return np.random.rand(N, 2)

# -------------------------
# Compute neighbors
# -------------------------
def compute_neighbors(positions, r):
    neighbors = [[] for _ in range(N)]
    for i in range(N):
        for j in range(i + 1, N):
            dist = np.linalg.norm(positions[i] - positions[j])
            if dist < r:
                neighbors[i].append(j)
                neighbors[j].append(i)
    return neighbors

# -------------------------
# Run one simulation, return last cycle flash counts
# -------------------------
def run_simulation(positions, r):
    neighbors = compute_neighbors(positions, r)
    clocks = np.random.randint(0, L, size=N)
    flash_counts = []

    for t in range(T):
        is_flashing = clocks < (L // 2)
        flash_counts.append(np.sum(is_flashing))
        new_clocks = (clocks + 1) % L
        for i in range(N):
            if not is_flashing[i] and neighbors[i]:
                flashing_neighbors = np.sum(is_flashing[neighbors[i]])
                if flashing_neighbors > len(neighbors[i]) / 2:
                    new_clocks[i] = (clocks[i] + 1) % L
        clocks = new_clocks

    # Return only the last cycle's flash count
    return flash_counts[-L:]

# -------------------------
# Main experiment: compute avg amplitude per r
# -------------------------
avg_amplitudes = []

print("Running amplitude analysis...")

for r in r_values:
    amplitudes = []
    for _ in range(num_runs):
        positions = generate_positions()
        last_cycle = run_simulation(positions, r)
        amp = (max(last_cycle) - min(last_cycle)) / 2
        amplitudes.append(amp)
    avg_amp = np.mean(amplitudes)
    avg_amplitudes.append(avg_amp)
    print(f"r = {r:.3f}, Avg amplitude = {avg_amp:.2f}")

# -------------------------
# Plot average amplitudes vs r
# -------------------------
plt.figure(figsize=(10, 6))
plt.plot(r_values, avg_amplitudes, marker='o', linewidth=2)
plt.title("Average Synchronization Amplitude vs Vicinity Radius")
plt.xlabel("Vicinity Radius r")
plt.ylabel("Average Amplitude (ΔFlashers / 2)")
plt.grid(True)
plt.tight_layout()
plt.show()