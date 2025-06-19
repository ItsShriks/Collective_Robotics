import pybullet as p
import pybullet_data
import time

p.connect(p.GUI)
p.setGravity(0, 0, -9.8)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.loadURDF("plane.urdf")

robot = p.loadURDF("assets/robot.urdf", basePosition=[0, 0, 0.1])

# Let the robot move forward
for _ in range(1000):
    p.setJointMotorControlArray(robot, [0, 1],
                                p.VELOCITY_CONTROL,
                                targetVelocities=[5, 5])
    p.stepSimulation()
    time.sleep(1/240)

p.disconnect()
