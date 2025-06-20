from robot import Robot
from environment import load_plane, load_boxes, create_home_zone, create_light_above
import pybullet as p
import time

def distance(pos1, pos2):
    return ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2) ** 0.5

def main():
    p.connect(p.GUI)
    p.setRealTimeSimulation(0)
    p.setGravity(0, 0, -9.81)

    load_plane()
    boxes = load_boxes(10, "../objects/box.urdf")
    home_id, home_pos = create_home_zone()
    create_light_above(home_pos)
    robot1 = Robot("../robots/simple_robot.urdf", [0, 0, 0.05], p.getQuaternionFromEuler([0, 0, 0]))
    robot2 = Robot("../robots/simple_robot.urdf", [1, 0, 0.05], p.getQuaternionFromEuler([0, 0, 0]))
    home_positions = {
        robot1: [home_pos[0] - 0.1, home_pos[1], home_pos[2]],
        robot2: [home_pos[0] + 0.1, home_pos[1], home_pos[2]],
    }

    robots = [robot1, robot2]
    assigned_boxes = set()

    while True:
        for robot in robots:

            if robot.holding is None:
                pos = robot.get_position()
                available_boxes = [b for b in boxes if b not in assigned_boxes]
                if not available_boxes:
                    continue
                nearest = min(available_boxes, key=lambda b: distance(pos, p.getBasePositionAndOrientation(b)[0]))

                if robot == robot1:
                    moved = robot.move_to(p.getBasePositionAndOrientation(nearest)[0], other_robots=robots, halt_if_blocked=True)
                else:
                    moved = robot.move_to(p.getBasePositionAndOrientation(nearest)[0], other_robots=robots)

                if moved:
                    robot.pick(nearest)
                    assigned_boxes.add(nearest)

            else:
                if robot == robot1:
                    moved = robot.move_to(home_positions[robot], other_robots=robots, halt_if_blocked=True)
                else:
                    moved = robot.move_to(home_positions[robot], other_robots=robots)

                if moved:
                    robot.drop()

        p.stepSimulation()
        time.sleep(1. / 240.)
        distances = robot1.get_proximity_readings()
        print(f"Proximity sensor distances: {distances}")

        force = robot1.get_bumper_force()
        print(f"Bumper force: {force}")

        num_pushed = robot1.estimate_objects_pushed(single_object_force=10.0)
        print(f"Estimated objects pushed: {num_pushed}")

if __name__ == "__main__":
    main()
