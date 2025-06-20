import pybullet as p
import math
import time
import numpy as np

class Robot:
    def __init__(self, urdf_path, start_pos, start_orientation, name="robot"):
        self.robot_id = p.loadURDF(urdf_path, start_pos, start_orientation)
        self.name = name
        self.holding = None
        self.constraint_id = None


    def get_position(self):
        return p.getBasePositionAndOrientation(self.robot_id)[0]

    def move_to(self, target, other_robots=[], step_size=0.01, safe_dist=0.3, halt_if_blocked=False):
        pos = self.get_position()
        dx = target[0] - pos[0]
        dy = target[1] - pos[1]
        dist = (dx**2 + dy**2)**0.5
        if dist < 0.01:
            return True

        move_x = step_size * dx / dist
        move_y = step_size * dy / dist
        next_pos = [pos[0] + move_x, pos[1] + move_y, pos[2]]

        # Check robots too close in next_pos
        for other in other_robots:
            if other is self:
                continue
            other_pos = other.get_position()
            d = ((next_pos[0] - other_pos[0])**2 + (next_pos[1] - other_pos[1])**2)**0.5
            if d < safe_dist:
                if halt_if_blocked:
                    # Halt and do NOT move
                    return False
                else:
                    # Other robots do side-step or keep moving anyway (optional)
                    break

        # Move robot
        p.resetBasePositionAndOrientation(
            self.robot_id,
            next_pos,
            p.getQuaternionFromEuler([0, 0, 0])
        )
        return dist < 0.05

    def pick(self, object_id):
        if self.holding is None:
            self.holding = object_id
            cid = p.createConstraint(
                parentBodyUniqueId=self.robot_id,
                parentLinkIndex=-1,
                childBodyUniqueId=object_id,
                childLinkIndex=-1,
                jointType=p.JOINT_FIXED,
                jointAxis=[0, 0, 0],
                parentFramePosition=[0, 0.1, 0.1],
                childFramePosition=[0, 0, 0]
            )
            self.constraint_id = cid

    def drop(self, drop_height=0.02, steps=50, sleep_time=0.01):
            if self.holding is None:
                return

            # Get current robot pos
            pos, orn = p.getBasePositionAndOrientation(self.robot_id)

            # Lower robot gradually by drop_height over `steps`
            for i in range(steps):
                z = pos[2] - (drop_height * (i+1) / steps)
                p.resetBasePositionAndOrientation(self.robot_id, [pos[0], pos[1], z], orn)
                p.stepSimulation()
                time.sleep(sleep_time)

            # Remove constraint to release object
            p.removeConstraint(self.constraint_id)
            self.holding = None

            # Optionally lift robot back up smoothly
            for i in range(steps):
                z = (pos[2] - drop_height) + (drop_height * (i+1) / steps)
                p.resetBasePositionAndOrientation(self.robot_id, [pos[0], pos[1], z], orn)
                p.stepSimulation()
                time.sleep(sleep_time)
    def get_proximity_readings(self, ray_length=0.5, ray_directions=None):
            """
            Cast rays around the robot and return distances to nearest object in each direction.
            ray_directions: list of 2D vectors (x,y) normalized
            """
            if ray_directions is None:
                # default directions: forward, left, right, diagonal
                ray_directions = [
                    (1, 0), (-1, 0), (0, 1), (0, -1),
                    (0.7, 0.7), (0.7, -0.7), (-0.7, 0.7), (-0.7, -0.7)
                ]

            pos, orn = p.getBasePositionAndOrientation(self.robot_id)
            pos = np.array(pos)
            # Get forward vector from orientation if you want relative rays (optional)

            ray_from = []
            ray_to = []

            for d in ray_directions:
                direction = np.array(d) / np.linalg.norm(d)
                start = pos + np.array([0, 0, 0.1])  # slightly above ground
                end = start + ray_length * np.array([direction[0], direction[1], 0])
                ray_from.append(start)
                ray_to.append(end)

            results = p.rayTestBatch(ray_from, ray_to)
            distances = []
            for res, start, end in zip(results, ray_from, ray_to):
                hit_fraction = res[2]
                if hit_fraction < 1.0:
                    hit_distance = np.linalg.norm(np.array(end) - np.array(start)) * hit_fraction
                else:
                    hit_distance = ray_length  # no hit
                distances.append(hit_distance)
            return distances

    def get_bumper_force(self):
            """
            Sum contact forces on the robot's base link (or bumper link if available)
            """
            contacts = p.getContactPoints(bodyA=self.robot_id)
            total_normal_force = 0.0
            for c in contacts:
                # c[9] = normal force magnitude
                total_normal_force += c[9]

            return total_normal_force

    def estimate_objects_pushed(self, single_object_force=10.0):
            """
            Estimate number of objects being pushed based on total force
            """
            total_force = self.get_bumper_force()
            n_objects = int(round(total_force / single_object_force))
            return max(0, n_objects)

    def step_controller(self, home_pos, arena_size=2.0, proximity_threshold=0.2, single_object_force=10.0):
            output = {}

            # (a) Actuator values (stub movement logic)
            # E.g., simple forward motion
            motor_left = 1.0
            motor_right = 1.0
            output["motor_left"] = motor_left
            output["motor_right"] = motor_right

            # (b) Error
            # Here: unknown = we can't evaluate error, but can be expanded
            output["error"] = "unknown"

            # (c) Collision (bumper force)
            contact_force = self.get_bumper_force()
            output["collision"] = contact_force > 1.0

            # (d) Arena boundary
            pos = self.get_position()
            if abs(pos[0]) > arena_size or abs(pos[1]) > arena_size:
                output["arena_boundary"] = True
            else:
                output["arena_boundary"] = False

            # (e) Transporting object
            output["transporting_object"] = self.holding is not None

            # (f) Home zone detection (simple radius check)
            distance_to_home = ((pos[0] - home_pos[0])**2 + (pos[1] - home_pos[1])**2) ** 0.5
            if distance_to_home < 0.3:
                output["home_zone"] = True
            else:
                output["home_zone"] = False

            return output
