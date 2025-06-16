import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# -----------------------------
# Load and preprocess data
# -----------------------------
data = np.loadtxt("L_of_L.txt")
L_vals = data[:, 0]
deltaL_vals = data[:, 1]

N = 50
s_vals = L_vals / N
delta_s_vals = deltaL_vals / N  # Convert ΔL to Δs = ΔL / N

# -----------------------------
# Define the model function
# -----------------------------
def delta_s_model(s, phi, c):
    PFB = phi * np.sin(np.pi * s)
    return 4 * c * (PFB - 0.5) * (s - 0.5)

# -----------------------------
# Fit the model to data
# -----------------------------
# Initial guess for phi and c
initial_guess = [0.5, 1.0]
# Bounds: phi in [0, 1], c unbounded
bounds = ([0.0, -np.inf], [1.0, np.inf])

# Fit the function
params, _ = curve_fit(delta_s_model, s_vals, delta_s_vals, p0=initial_guess, bounds=bounds)
phi_fit, c_fit = params

print(f"Fitted φ (phi): {phi_fit:.4f}")
print(f"Fitted c: {c_fit:.4f}")

# -----------------------------
# Generate smooth curves for plotting
# -----------------------------
s_fit = np.linspace(0, 1, 300)
delta_s_fit = delta_s_model(s_fit, phi_fit, c_fit)
PFB_fit = phi_fit * np.sin(np.pi * s_fit)

# -----------------------------
# Plot: Δs(s) with fitted function
# -----------------------------
plt.figure(figsize=(10, 5))
plt.plot(s_vals, delta_s_vals, 'o', label='Simulation Data (Δs)')
plt.plot(s_fit, delta_s_fit, '-', label=f'Fitted Model\nφ = {phi_fit:.2f}, c = {c_fit:.2f}', color='red')
plt.axhline(0, color='black', linestyle='--')
plt.axvline(0.5, color='gray', linestyle=':')
plt.xlabel("s (Fraction of Left-Goers)")
plt.ylabel("Δs(s)")
plt.title("Δs(s) vs s with Fitted Urn Model")
plt.legend()
plt.grid(True)
#plt.show()
plt.savefig("../output/task1_2_plot.png", dpi=300)
plt.close()  # Close the figure to free memory
