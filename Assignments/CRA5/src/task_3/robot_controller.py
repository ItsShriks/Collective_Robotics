import pybullet as p
import numpy as np

class Robot:
    def __init__(self, start_pos, robot_id):
        self.id = robot_id
        self.robot = p.loadURDF("assets/robot.urdf", basePosition=start_pos)
        self.carrying_object = False

    def read_sensors(self):
        # Simulated sensor values
        light_left = np.random.random()
        light_right = np.random.random()
        bumper_force = np.random.uniform(0, 10)
        proximity = [np.random.random() for _ in range(8)]

        return light_left, light_right, bumper_force, proximity

    def decide(self, sensors):
        light_left, light_right, bumper_force, proximity = sensors

        transporting_object = bumper_force > 5  # Simulate pushing
        collision = max(proximity) > 0.8
        home_zone = (light_left + light_right) > 1.5

        # Simple behavior: go forward or turn
        if collision:
            left, right = -1.0, 1.0
        elif home_zone and transporting_object:
            self.carrying_object = False
            return (0, 0), False, True, False, False, True
        elif transporting_object:
            left, right = light_right, light_left
        else:
            left, right = 1.0, 1.0

        return (left, right), False, collision, False, transporting_object, home_zone

    def step(self, objects, home_zone):
        sensors = self.read_sensors()
        (left, right), error, collision, arena_boundary, transporting_object, home_zone_flag = self.decide(sensors)

        p.setJointMotorControlArray(self.robot, [0, 1],
                                    p.VELOCITY_CONTROL,
                                    targetVelocities=[left, right])

        # If object is delivered
        if not self.carrying_object and transporting_object:
            self.carrying_object = True
        elif self.carrying_object and home_zone_flag:
            self.carrying_object = False
            return 1  # Delivered
        return 0
