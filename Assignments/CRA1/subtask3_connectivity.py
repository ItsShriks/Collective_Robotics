import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def simulate_connectivity_effect(num_agents, connection_prob):
    G = nx.erdos_renyi_graph(num_agents, connection_prob)
    is_connected = nx.is_connected(G)
    return is_connected

probs = np.linspace(0.05, 1.0, 20)
connectivity = [simulate_connectivity_effect(20, p) for p in probs]

plt.plot(probs, connectivity, marker='o')
plt.title("Effect of Connection Probability on Swarm Connectivity")
plt.xlabel("Connection Probability")
plt.ylabel("Is Connected (1=True, 0=False)")
plt.grid(True)
plt.savefig("Plots/swarm_connectivity.png")
plt.show()
