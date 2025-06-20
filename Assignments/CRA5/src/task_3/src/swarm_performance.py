import pybullet as p
import pybullet_data
import time
import matplotlib.pyplot as plt
from robot import Robot
from environment import load_plane, load_boxes, create_home_zone, create_light_above
from math import sqrt

def distance(a, b):
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def run_simulation(num_robots, sim_duration=30):
    p.connect(p.DIRECT)  # Use DIRECT for headless fast runs
    p.setGravity(0, 0, -9.81)
    p.setRealTimeSimulation(0)

    load_plane()
    boxes = load_boxes(100, "../objects/box.urdf")  # Use N Boxes
    home_id, home_pos = create_home_zone()
    create_light_above(home_pos)

    robots = []
    for i in range(num_robots):
        x = i * 0.5
        robot = Robot("../robots/simple_robot.urdf", [x, 0, 0.05], p.getQuaternionFromEuler([0, 0, 0]), name=f"robot{i}")
        robots.append(robot)

    home_positions = {
        robot: [home_pos[0] + 0.1 * i, home_pos[1], home_pos[2]]
        for i, robot in enumerate(robots)
    }

    assigned_boxes = set()
    collected_count = 0
    start_time = time.time()

    while time.time() - start_time < sim_duration:
        for robot in robots:
            if robot.holding is None:
                available_boxes = [b for b in boxes if b not in assigned_boxes]
                if not available_boxes:
                    continue
                pos = robot.get_position()
                nearest = min(available_boxes, key=lambda b: distance(pos, p.getBasePositionAndOrientation(b)[0]))
                target_pos = p.getBasePositionAndOrientation(nearest)[0]
                reached = robot.move_to(target_pos, other_robots=robots, halt_if_blocked=(robot == robots[0]))
                if reached:
                    robot.pick(nearest)
                    assigned_boxes.add(nearest)
            else:
                target = home_positions[robot]
                reached = robot.move_to(target, other_robots=robots, halt_if_blocked=(robot == robots[0]))
                if reached:
                    robot.drop()
                    collected_count += 1

        p.stepSimulation()

    p.disconnect()
    return collected_count
def main():
    swarm_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    results = []

    for size in swarm_sizes:
        print(f"Running simulation with {size} robots...")
        collected = run_simulation(size, sim_duration=30)  # Run 30 seconds per trial
        results.append(collected)
        print(f"Collected: {collected}")

    # Plot
    plt.figure(figsize=(8, 5))
    plt.plot(swarm_sizes, results, marker='o')
    plt.xlabel("Swarm Size (Number of Robots)")
    plt.ylabel("Objects Collected in 30s")
    plt.title("Swarm Performance vs Swarm Size")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    plt.savefig("task3_plot.png", dpi=300)  # PNG with high resolution
    print("Plot saved as 'task3_plot.png'")
    plt.show()
if __name__ == "__main__":
    main()
