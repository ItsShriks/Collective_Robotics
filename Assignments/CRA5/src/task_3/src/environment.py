import pybullet_data
import pybullet as p
import random

def load_plane():
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    return p.loadURDF("plane.urdf", [0, 0, 0])

def load_boxes(n, urdf_path):
    box_ids = []
    for _ in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        box_id = p.loadURDF(urdf_path, [x, y, 0])
        box_ids.append(box_id)
    return box_ids

def create_home_zone(pos=(1.5, 1.5, 0)):
    size = [0.4, 0.4, 0.01]
    col_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=size)
    vis_shape = p.createVisualShape(
        shapeType=p.GEOM_BOX,
        halfExtents=size,
        rgbaColor=[1, 1, 0, 0.6]  # yellow translucent
    )
    home_id = p.createMultiBody(
        baseCollisionShapeIndex=col_shape,
        baseVisualShapeIndex=vis_shape,
        basePosition=pos
    )
    return home_id, pos

def create_light_above(pos=(1.5, 1.5, 1)):
    p.configureDebugVisualizer(p.COV_ENABLE_SHADOWS, 1)
    p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
    p.addUserDebugLine(pos, (pos[0], pos[1], 0), [1, 1, 0], 5, 0)  # beam line
