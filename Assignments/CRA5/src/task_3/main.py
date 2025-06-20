# main.py

import pybullet as p
import pybullet_data
import numpy as np
import matplotlib.pyplot as plt
from robot import Robot
import time

def run_simulation(n_robots=5, max_steps=3000, gui=False):
    if gui:
        p.connect(p.GUI)
    else:
        p.connect(p.DIRECT)

    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.loadURDF("plane.urdf")
    p.setGravity(0, 0, -9.8)

    # Simulated home zone light source
    home_zone_pos = [0, 0, 1.5]

    # Spawn robots
    robots = []
    for i in range(n_robots):
        start_pos = [np.random.uniform(-4, 4), np.random.uniform(-4, 4), 0.1]
        robot_id = i  # placeholder ID
        robots.append(Robot(start_pos=start_pos, robot_id=robot_id))

    delivered_objects = 0

    for t in range(max_steps):
        for robot in robots:
            delivered = robot.step(objects=[], home_zone=home_zone_pos)
            delivered_objects += delivered

        p.stepSimulation()
        if gui:
            time.sleep(1. / 240.)

    p.disconnect()
    return delivered_objects


if __name__ == "__main__":
    swarm_sizes = [1, 3, 5, 7, 10]
    performances = []

    for size in swarm_sizes:
        print(f"Running simulation for swarm size = {size}")
        delivered = run_simulation(n_robots=size, gui=False)
        performances.append(delivered)

    # Plot results
    plt.figure(figsize=(8, 5))
    plt.plot(swarm_sizes, performances, marker='o', linestyle='-', color='blue')
    plt.xlabel("Swarm Size")
    plt.ylabel("Objects Delivered")
    plt.title("Swarm Foraging Performance vs Swarm Size")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("swarm_performance.png")
    plt.show()
