import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
def buffons_needle_std_dev(b=0.7, s=1.0, repetitions=10000):
    trial_counts = np.arange(10, 1001, 10)  # n in {10, 20, ..., 1000}
    std_devs = []

    for n in trial_counts:
        intersection_probs = []
        for _ in range(repetitions):
            d = np.random.uniform(0, s / 2, n)
            theta = np.random.uniform(0, np.pi / 2, n)
            intersects = (b / 2) * np.sin(theta) >= d
            P = np.mean(intersects)
            intersection_probs.append(P)

        std_dev = np.std(intersection_probs)
        std_devs.append(std_dev)

    return trial_counts, std_devs


trial_counts, std_devs = buffons_needle_std_dev()

plt.figure(figsize=(10, 6))
plt.plot(trial_counts, std_devs, color='blue', marker='o', linestyle='-')
plt.xlabel("Number of Trials (n)")
plt.ylabel("Standard Deviation of Intersection Probability")
plt.title("Standard Deviation vs Number of Trials in Buffon's Needle Simulation")
plt.grid(True)
plt.tight_layout()
plt.savefig('../output/task1_b.png')
plt.show()
