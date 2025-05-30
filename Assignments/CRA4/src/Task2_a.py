import numpy as np
import matplotlib.pyplot as plt
import os
# Parameters
alpha_r = 0.6
alpha_p = 0.2
tau_a = 2.0
t_max = 50.0
dt = 0.01
n_steps = int(t_max / dt)

# Time array
t = np.linspace(0, t_max, n_steps)
ns = np.zeros(n_steps)
m = np.zeros(n_steps)

# Initial conditions
ns[0] = 1.0
m[0] = 1.0

# Delay steps
delay_steps = int(tau_a / dt)

for i in range(1, n_steps):
    # Current and delayed ns values
    ns_current = ns[i - 1]
    if i - delay_steps >= 0:
        ns_delayed = ns[i - delay_steps]
    else:
        ns_delayed = ns[0]  # Use initial value before delay time

    # Derivatives
    d_ns = -alpha_r * ns_current * (ns_current + 1) + alpha_r * ns_delayed * (ns_delayed + 1)
    d_m = -alpha_p * ns_current * m[i - 1]

    # Euler integration
    ns[i] = ns[i - 1] + dt * d_ns
    m[i] = m[i - 1] + dt * d_m

output_dir = "../output"
os.makedirs(output_dir, exist_ok=True)

# --- Plot results ---
plt.figure(figsize=(10, 5))
plt.plot(t, ns, label='n_s(t) (searching)', color='blue')
plt.plot(t, m, label='m(t) (avoiding)', color='red')
plt.xlabel('Time (t)')
plt.ylabel('Values')
plt.title('Temporal Evolution of n_s(t) and m(t) with Delay')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Task2_a.png'))
#plt.show()
