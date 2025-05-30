import numpy as np
import matplotlib.pyplot as plt
import os
# Parameters
alpha_r = 0.6
alpha_p = 0.2
tau_a = 2
tau_h = 15

# Initial values
ns0 = 1.0
m0 = 1.0
nh0 = 0.0

# Simulation settings
t_max = 160
dt = 0.1
n_steps = int(t_max / dt)
time = np.linspace(0, t_max, n_steps)

# Delay steps
delay_a = int(tau_a / dt)
delay_h = int(tau_h / dt)

# Initialize arrays
ns = np.full(n_steps, ns0)
m = np.full(n_steps, m0)
nh = np.full(n_steps, nh0)

# Cap values to avoid overflow
CAP = 1e3

# Simulation loop
for i in range(1, n_steps):
    ns_curr = ns[i - 1]
    m_curr = m[i - 1]
    nh_curr = nh[i - 1]

    # Handle delays
    if i >= delay_a:
        ns_a = ns[i - delay_a]
    else:
        ns_a = ns0

    if i >= delay_h:
        nh_h = nh[i - delay_h]
    else:
        nh_h = 0.0

    # Rate equations
    d_ns = -alpha_r * ns_curr * (ns_curr + 1) + alpha_r * ns_a * (ns_a + 1) + nh_h
    d_m = -alpha_p * ns_curr * m_curr
    d_nh = alpha_r * ns_curr * (ns_curr + 1) - nh_h

    # Euler integration with clipping
    ns[i] = np.clip(ns[i - 1] + dt * d_ns, 0, CAP)
    m[i] = np.clip(m[i - 1] + dt * d_m, 0, CAP)
    nh[i] = np.clip(nh[i - 1] + dt * d_nh, 0, CAP)

# ---- Plot original result ----
plt.figure(figsize=(10, 5))
plt.plot(time, ns, label='Searching robots (ns)')
plt.plot(time, m, label='Pucks (m)')
plt.plot(time, nh, label='Homing robots (nh)')
plt.title("Temporal evolution of ns, m, and nh")
plt.xlabel("Time")
plt.ylabel("Value")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# ---- Reset m(80) = 0.5 and rerun ----
m_reset = m.copy()
ns2 = ns.copy()
nh2 = nh.copy()

for i in range(int(80 / dt), n_steps):
    ns_curr = ns2[i - 1]
    m_curr = m_reset[i - 1]
    nh_curr = nh2[i - 1]

    if i >= delay_a:
        ns_a = ns2[i - delay_a]
    else:
        ns_a = ns0

    if i >= delay_h:
        nh_h = nh2[i - delay_h]
    else:
        nh_h = 0.0

    d_ns = -alpha_r * ns_curr * (ns_curr + 1) + alpha_r * ns_a * (ns_a + 1) + nh_h
    d_m = -alpha_p * ns_curr * m_curr
    d_nh = alpha_r * ns_curr * (ns_curr + 1) - nh_h

    ns2[i] = np.clip(ns2[i - 1] + dt * d_ns, 0, CAP)
    m_reset[i] = np.clip(m_reset[i - 1] + dt * d_m, 0, CAP)
    nh2[i] = np.clip(nh2[i - 1] + dt * d_nh, 0, CAP)

    # Reset m(80) = 0.5
    if i == int(80 / dt):
        m_reset[i] = 0.5
output_dir = "../output"
os.makedirs(output_dir, exist_ok=True)
# ---- Plot after m(80)=0.5 reset ----
plt.figure(figsize=(10, 5))
plt.plot(time, ns2, label='Searching robots (ns)')
plt.plot(time, m_reset, label='Pucks (m) after reset at t=80')
plt.plot(time, nh2, label='Homing robots (nh)')
plt.title("After reset: m(80) = 0.5")
plt.xlabel("Time")
plt.ylabel("Value")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig(os.path.join(output_dir, 'Task2_b.png'))
#plt.show()

