import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def buffons_needle_ci_coverage(b=0.7, s=1.0, max_n=100, repetitions=1000, confidence=0.95):
    z = norm.ppf(0.5 + confidence / 2)
    true_P = (2 * b) / (s * np.pi)  # Theoretical intersection probability

    ns = np.arange(1, max_n + 1)
    error_rates = []

    for n in ns:
        outside_count = 0

        for _ in range(repetitions):
            d = np.random.uniform(0, s / 2, n)
            theta = np.random.uniform(0, np.pi / 2, n)
            intersects = (b / 2) * np.sin(theta) >= d
            P_hat = np.mean(intersects)
            std_hat = np.std(intersects) / np.sqrt(n)
            margin = z * std_hat

            lower = P_hat - margin
            upper = P_hat + margin

            if true_P < lower or true_P > upper:
                outside_count += 1

        error_rate = outside_count / repetitions
        error_rates.append(error_rate)

    return ns, error_rates

# Run the simulation
ns, error_rates = buffons_needle_ci_coverage()

# Plot the ratio of experiments where the true probability is outside the 95% CI
plt.figure(figsize=(10, 6))
plt.plot(ns, error_rates, label="Out-of-CI Rate", color="crimson")
plt.axhline(y=0.05, color='gray', linestyle='--', label="Expected (5%)")
plt.xlabel("Number of Trials (n)")
plt.ylabel("Error Rate (True P Outside CI)")
plt.title("Empirical Error Rate of 95% CI vs Number of Trials")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('../output/task1_d.png')
plt.show()