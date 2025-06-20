import pybullet as p
import pybullet_data
import time
import math

class Robot:
    def __init__(self, urdf_path, start_pos, start_orientation):
        self.robot_id = p.loadURDF(urdf_path, start_pos, start_orientation, useFixedBase=False)
        self.left_wheel = 0
        self.right_wheel = 1
        self.left_finger = 2
        self.right_finger = 3
        self.max_speed = 10.0
        self.holding = None
        self.constraint_id = None

    def get_position(self):
        return p.getBasePositionAndOrientation(self.robot_id)[0]

    def stop(self):
        p.setJointMotorControl2(self.robot_id, self.left_wheel, p.VELOCITY_CONTROL, targetVelocity=0)
        p.setJointMotorControl2(self.robot_id, self.right_wheel, p.VELOCITY_CONTROL, targetVelocity=0)

    def drive(self, v_l, v_r):
        p.setJointMotorControl2(self.robot_id, self.left_wheel, p.VELOCITY_CONTROL, targetVelocity=v_l, force=10)
        p.setJointMotorControl2(self.robot_id, self.right_wheel, p.VELOCITY_CONTROL, targetVelocity=v_r, force=10)

    def move_towards(self, target, other_robots=[], safe_dist=0.3):
        my_pos = self.get_position()
        dx = target[0] - my_pos[0]
        dy = target[1] - my_pos[1]
        dist = math.hypot(dx, dy)

        if dist < 0.05:
            self.stop()
            return True

        heading = math.atan2(dy, dx)
        yaw = p.getEulerFromQuaternion(p.getBasePositionAndOrientation(self.robot_id)[1])[2]
        error = heading - yaw
        error = (error + math.pi) % (2 * math.pi) - math.pi

        linear_vel = min(6.0 * dist, self.max_speed)
        angular_vel = 6.0 * error

        v_l = linear_vel - angular_vel
        v_r = linear_vel + angular_vel

        for other in other_robots:
            if other is self:
                continue
            other_pos = other.get_position()
            if math.dist(my_pos, other_pos) < safe_dist:
                self.stop()
                return False

        self.drive(v_l, v_r)
        return False

    def open_gripper(self):
        p.setJointMotorControl2(self.robot_id, self.left_finger, p.POSITION_CONTROL, targetPosition=0.04, force=10)
        p.setJointMotorControl2(self.robot_id, self.right_finger, p.POSITION_CONTROL, targetPosition=0.04, force=10)

    def close_gripper(self):
        p.setJointMotorControl2(self.robot_id, self.left_finger, p.POSITION_CONTROL, targetPosition=0.0, force=10)
        p.setJointMotorControl2(self.robot_id, self.right_finger, p.POSITION_CONTROL, targetPosition=0.0, force=10)

    def pick(self, object_id):
        if self.holding is None:
            self.close_gripper()
            time.sleep(0.5)
            cid = p.createConstraint(self.robot_id, -1, object_id, -1, p.JOINT_FIXED, [0, 0, 0], [0, 0.1, 0.15], [0, 0, 0])
            self.holding = object_id
            self.constraint_id = cid

    def drop(self):
        if self.holding is not None:
            p.removeConstraint(self.constraint_id)
            self.holding = None
            self.open_gripper()
            time.sleep(0.5)

def create_environment():
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.loadURDF("plane.urdf")
    box_ids = []
    for i in range(4):
        box_id = p.loadURDF("../objects/box.urdf", [i * 0.4 - 0.6, 0.8, 0.025])
        box_ids.append(box_id)
    home_id = p.loadURDF("../objects/box.urdf", [1.5, 1.5, 0.05], globalScaling=0.2, useFixedBase=True)
    return box_ids, [1.5, 1.5, 0.05]

def main():
    p.connect(p.GUI)
    p.setGravity(0, 0, -9.81)

    boxes, home_pos = create_environment()

    robot1 = Robot("../robots/wheeled_robot.urdf", [0, 0, 0.1], p.getQuaternionFromEuler([0, 0, 0]))
    robot2 = Robot("../robots/wheeled_robot.urdf", [1, 0, 0.1], p.getQuaternionFromEuler([0, 0, 0]))

    robots = [robot1, robot2]
    assigned = set()

    while True:
        for robot in robots:
            if robot.holding is None:
                pos = robot.get_position()
                available = [b for b in boxes if b not in assigned]
                if not available:
                    continue
                nearest = min(available, key=lambda b: math.dist(pos, p.getBasePositionAndOrientation(b)[0]))
                if robot.move_towards(p.getBasePositionAndOrientation(nearest)[0], robots):
                    robot.pick(nearest)
                    assigned.add(nearest)
            else:
                if robot.move_towards(home_pos, robots):
                    robot.drop()

        p.stepSimulation()
        time.sleep(1./240.)

if __name__ == "__main__":
    main()
