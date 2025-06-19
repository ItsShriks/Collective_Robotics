import pybullet as p
import random

def spawn_objects(num_objects):
    obj_ids = []
    for _ in range(num_objects):
        x, y = random.uniform(-2, 2), random.uniform(-2, 2)
        obj_id = p.loadURDF("sphere_small.urdf", basePosition=(x, y, 0.1))
        obj_ids.append(obj_id)
    return obj_ids

def spawn_home_zone():
    light_id = p.loadURDF("cube_small.urdf", basePosition=(0, 3, 0.1),
                          useFixedBase=True)
    return light_id
