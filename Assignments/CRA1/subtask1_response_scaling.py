import matplotlib.pyplot as plt
import numpy as np
import time

def simulate_response_time(n_agents):
    start = time.time()
    for _ in range(n_agents):
        time.sleep(0.001)  # Simulate computation/communication delay
    end = time.time()
    return end - start

agents = list(range(10, 310, 10))
times = [simulate_response_time(n) for n in agents]

plt.plot(agents, times, marker='o')
plt.title("Scaling of Response Time with Number of Agents")
plt.xlabel("Number of Agents")
plt.ylabel("Response Time (s)")
plt.grid(True)
plt.savefig("Plots/response_time_scaling.png")
plt.show()
