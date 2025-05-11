import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def buffons_needle_simulation(b=0.7, s=1.0, N=100000):
    d = np.random.uniform(0, s / 2, N)
    theta = np.random.uniform(0, np.pi / 2, N)
    intersects = (b / 2) * np.sin(theta) >= d
    P = np.mean(intersects)
    pi_estimate = (2 * b) / (s * P)
    
    return P, pi_estimate
P, pi_estimate = buffons_needle_simulation()
print(f"Estimated Probability P: {P}")
print(f"Estimated π: {pi_estimate}")
