import os
import numpy as np
import matplotlib.pyplot as plt
import time
import platform
import psutil
from scipy.stats import poisson
from scipy.spatial import KDTree

# -------------------------
# Start timer
# -------------------------
start_time = time.time()

# -------------------------
# Output path
# -------------------------
output_dir = "Assignments/CRA1/output"
output_path = os.path.join(output_dir, "firefly_synchronization.png")
os.makedirs(output_dir, exist_ok=True)

# -------------------------
# Parameters
# -------------------------
N = 250
L = 50
T = 1000
r_values = np.arange(0.000, 1.5, 0.25)
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
plt.savefig(output_path, dpi=300)
plt.show()

# -------------------------
# End timer and print system info
# -------------------------
end_time = time.time()
exec_time = end_time - start_time

print("\n--- Execution Summary ---")
print(f"Execution Time: {exec_time:.2f} seconds")
print(f"System Architecture: {platform.machine()}")
print(f"CPU: {platform.processor() or platform.uname().processor}")
print(f"Total RAM: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB")
