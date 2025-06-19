import pybullet as p
import pybullet_data
import time
import numpy as np
import matplotlib.pyplot as plt
from robot_controller import Robot
from utils import spawn_objects, spawn_home_zone

def run_simulation(num_robots, sim_time=30):
    p.connect(p.DIRECT)  # Use GUI for debugging
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.8)
    p.loadURDF("plane.urdf")

    home_zone = spawn_home_zone()
    robots = [Robot(start_pos=(i * 0.5, 0, 0.1), robot_id=i) for i in range(num_robots)]
    objects = spawn_objects(num_objects=20)

    collected = 0
    start_time = time.time()

    while time.time() - start_time < sim_time:
        for robot in robots:
            collected += robot.step(objects, home_zone)
        p.stepSimulation()
        time.sleep(1/240.0)

    p.disconnect()
    return collected

# Run for different swarm sizes
results = []
for N in range(1, 11):
    performance = run_simulation(num_robots=N)
    results.append(performance)
    print(f"N={N}, Collected: {performance}")

# Plotting
plt.plot(range(1, 11), results, marker='o')
plt.title("Swarm Performance over Swarm Size")
plt.xlabel("Number of Robots")
plt.ylabel("Collected Objects")
plt.grid(True)
plt.show()
