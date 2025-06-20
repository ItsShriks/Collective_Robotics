import pybullet as p
import pybullet_data
import time
from robot import Robot
from environment import load_plane, load_boxes, create_home_zone, create_light_above
from math import sqrt

def distance(a, b):
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def main():
    # Initialize simulation
    p.connect(p.GUI)
    p.setGravity(0, 0, -9.81)
    p.setRealTimeSimulation(0)

    load_plane()
    boxes = load_boxes(10, "../objects/box.urdf")
    home_id, home_pos = create_home_zone()
    create_light_above(home_pos)

    # Create robots
    robot1 = Robot("../robots/simple_robot.urdf", [0, 0, 0.05], p.getQuaternionFromEuler([0, 0, 0]), name="robot1")
    robot2 = Robot("../robots/simple_robot.urdf", [1, 0, 0.05], p.getQuaternionFromEuler([0, 0, 0]), name="robot2")
    robots = [robot1, robot2]

    # Offset home zone for each robot
    home_positions = {
        robot1: [home_pos[0] - 0.1, home_pos[1], home_pos[2]],
        robot2: [home_pos[0] + 0.1, home_pos[1], home_pos[2]],
    }

    assigned_boxes = set()

    while True:
        for robot in robots:
            # Controller outputs sensor values + actuator commands
            controller_output = robot.step_controller(home_pos)

            print(f"[{robot.name}] Status:")
            for key, val in controller_output.items():
                print(f"  {key}: {val}")
            print("-" * 40)

            # Basic behavior: pick and place
            if robot.holding is None:
                available_boxes = [b for b in boxes if b not in assigned_boxes]
                if not available_boxes:
                    continue
                pos = robot.get_position()
                nearest_box = min(available_boxes, key=lambda b: distance(pos, p.getBasePositionAndOrientation(b)[0]))
                target_pos = p.getBasePositionAndOrientation(nearest_box)[0]

                # Use strict avoidance for robot1
                halt = robot == robot1
                reached = robot.move_to(target_pos, other_robots=robots, halt_if_blocked=halt)

                if reached:
                    robot.pick(nearest_box)
                    assigned_boxes.add(nearest_box)
            else:
                # Go to home zone (slightly offset)
                target = home_positions[robot]
                halt = robot == robot1
                reached = robot.move_to(target, other_robots=robots, halt_if_blocked=halt)

                if reached:
                    robot.drop()

        p.stepSimulation()
        time.sleep(1. / 240.)

if __name__ == "__main__":
    main()
