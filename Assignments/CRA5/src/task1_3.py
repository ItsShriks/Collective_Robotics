import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# -----------------------------
# Plot: PFB(s) from fitted φ
# -----------------------------
plt.figure(figsize=(10, 4))
plt.plot(s_fit, PFB_fit, label=f"PFB(s) = φ·sin(πs), φ = {phi_fit:.2f}", color='green')
plt.axhline(0.5, color='black', linestyle='--')
plt.xlabel("s (Fraction of Left-Goers)")
plt.ylabel("PFB(s)")
plt.title("Probability of Positive Feedback (PFB) vs s")
plt.grid(True)
plt.legend()
#plt.show()
plt.savefig("../output/task1_3_plot.png", dpi=300)
plt.close()  # Close the figure to free memory
