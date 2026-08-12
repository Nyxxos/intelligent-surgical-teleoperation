import pybullet as p
import pybullet_data

physics_client = p.connect(p.GUI)

p.setAdditionalSearchPath(pybullet_data.getDataPath())

plane_id = p.loadURDF("plane.urdf")

input("Press Enter to close the simulation...")

p.disconnect()
