import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
# For n from 1 to 100, simulate many experiments and track the probability over trials
def buffons_needle_probability_with_ci(b=0.7, s=1.0, max_trials=100, repetitions=10000, confidence=0.95):
    from scipy.stats import norm

    z = norm.ppf(0.5 + confidence / 2)  # z-value for 95% CI
    trial_range = np.arange(1, max_trials + 1)
    
    # Store mean probabilities and confidence intervals
    mean_probs = []
    lower_bounds = []
    upper_bounds = []

    for n in trial_range:
        probs = []
        for _ in range(repetitions):
            d = np.random.uniform(0, s / 2, n)
            theta = np.random.uniform(0, np.pi / 2, n)
            intersects = (b / 2) * np.sin(theta) >= d
            P = np.mean(intersects)
            probs.append(P)

        mean_P = np.mean(probs)
        std_P = np.std(probs)
        margin = z * std_P

        mean_probs.append(mean_P)
        lower_bounds.append(mean_P - margin)
        upper_bounds.append(mean_P + margin)

    return trial_range, mean_probs, lower_bounds, upper_bounds

# Run the function
trial_range, mean_probs, lower_bounds, upper_bounds = buffons_needle_probability_with_ci()

# Plotting the probabilities with confidence intervals
plt.figure(figsize=(10, 6))
plt.plot(trial_range, mean_probs, label="Mean Intersection Probability", color="blue")
plt.fill_between(trial_range, lower_bounds, upper_bounds, color='blue', alpha=0.2, label="95% Confidence Interval")
plt.xlabel("Number of Trials (n)")
plt.ylabel("Estimated Probability")
plt.title("Estimated Probability with 95% CI (Buffon's Needle, n ≤ 100)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('../output/task1_c.png')
plt.show()
