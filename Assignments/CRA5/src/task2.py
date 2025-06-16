import numpy as np
import matplotlib.pyplot as plt

# Base Parameters (except N)
C = 0.5
v = 0.01
r = 0.045
P = 0.15
T_total = 10000  # Should be enough for multiple switches
runs_per_N = 30  # Repeat for averaging

# Swarm sizes to test
N_vals = np.arange(20, 155, 10)
avg_switch_times = []
num_switches_list = []

for N in N_vals:
    switch_durations = []

    for run in range(runs_per_N):
        positions = np.random.uniform(0, C, N)
        directions = np.random.choice([-1, 1], N)

        prev_zone = None
        zone_entry = None
        counter = 0

        for t in range(T_total):
            # Movement
            pos_diff = positions[:, None] - positions
            distances = np.abs(pos_diff)
            distances = np.minimum(distances, C - distances)

            influence = np.zeros(N)
            for i in range(N):
                neighbors = distances[i] <= r
                local_sum = np.sum(directions[neighbors])
                if np.random.rand() < P:
                    influence[i] = -directions[i]
                elif local_sum != 0:
                    influence[i] = np.sign(local_sum)
                else:
                    influence[i] = directions[i]

            directions = influence.astype(int)
            positions = (positions + v * directions) % C

            # Count left-goers
            L = np.count_nonzero(directions == -1)

            # Determine current zone
            if L > 0.7 * N:
                zone = "A"
            elif L < 0.3 * N:
                zone = "C"
            else:
                zone = "B"

            # Switch detection logic
            if zone in ["A", "C"]:
                if prev_zone == "B":
                    if zone != zone_entry:  # A → B → C or C → B → A
                        switch_durations.append(counter)
                    counter = 0
                prev_zone = zone
            elif zone == "B":
                if prev_zone in ["A", "C"]:
                    zone_entry = prev_zone  # Remember where we came from
                    counter = 1
                    prev_zone = "B"
                elif prev_zone == "B":
                    counter += 1

    # Stats for this N
    num_switches = len(switch_durations)
    avg_time = np.mean(switch_durations) if num_switches > 0 else np.nan

    avg_switch_times.append(avg_time)
    num_switches_list.append(num_switches)

# ---------------------------
# Plotting results
# ---------------------------

# Plot 1: Average switch time vs swarm size
plt.figure(figsize=(10, 5))
plt.plot(N_vals, avg_switch_times, marker='o', label="Avg. Switch Time")
plt.xlabel("Swarm Size N")
plt.ylabel("Average Switch Time")
plt.title("Switch Time vs Swarm Size")
plt.grid(True)
plt.legend()
plt.tight_layout()
#plt.show()
plt.savefig("../output/task2_1_plot.png", dpi=300)
plt.close()  # Close the figure to free memory


# Plot 2: Number of switches vs swarm size
plt.figure(figsize=(10, 5))
plt.plot(N_vals, num_switches_list, marker='s', color='orange', label="Switch Count")
plt.xlabel("Swarm Size N")
plt.ylabel("Number of Switches")
plt.title("Number of Switches vs Swarm Size")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("../output/task2_2_plot.png", dpi=300)
plt.close()  # Close the figure to free memory
