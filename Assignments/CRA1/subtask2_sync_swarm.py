import random
import numpy as np
import matplotlib.pyplot as plt

def synchronize_swarm(num_agents, max_iter=100):
    states = [random.randint(0, 10) for _ in range(num_agents)]
    history = [states.copy()]

    for _ in range(max_iter):
        avg_state = sum(states) / num_agents
        states = [state + (avg_state - state) * 0.1 for state in states]
        history.append(states.copy())
        if all(abs(state - avg_state) < 0.01 for state in states):
            break

    return history

history = synchronize_swarm(10)
history = np.array(history)

for i in range(history.shape[1]):
    plt.plot(history[:, i], label=f'Agent {i+1}')
plt.title("Synchronization of Asynchronous Swarm")
plt.xlabel("Iterations")
plt.ylabel("State Value")
plt.legend()
plt.grid(True)
plt.savefig("Plots/swarm_synchronization.png")
plt.show()
