import time
import pybullet as p
import pybullet_data

physics_client = p.connect(p.GUI)

# Let PyBullet find its built-in URDF models and assets.
p.setAdditionalSearchPath(pybullet_data.getDataPath())

plane_id = p.loadURDF("plane.urdf")

# Keep the Panda base fixed while allowing the arm joints to move.
robot_id = p.loadURDF(
    "franka_panda/panda.urdf",
    basePosition=[0, 0, 0],
    useFixedBase=True
)

num_joints = p.getNumJoints(robot_id)
print("Number of joints:", num_joints)

for joint_index in range(num_joints):
    joint_info = p.getJointInfo(robot_id, joint_index)
    joint_name = joint_info[1].decode("utf-8")
    joint_type = joint_info[2]

    print(joint_index, joint_name, joint_type)


arm_joint_indices = list(range(7))
end_effector_link_index = 11

# Move the end effector towards a target position using inverse kinematics.
target_position = [0.5, 0.0, 0.5]

joint_targets = p.calculateInverseKinematics(
    robot_id,
    end_effector_link_index,
    target_position
)

for joint_index in arm_joint_indices:
    p.setJointMotorControl2(
        bodyUniqueId=robot_id,
        jointIndex=joint_index,
        controlMode=p.POSITION_CONTROL,
        targetPosition=joint_targets[joint_index]
    )

# Advance the simulation long enough to observe the movement.
for _ in range(240):
    p.stepSimulation()
    time.sleep(1 / 240)


input("Press Enter to close the simulation...")

if p.isConnected():
    p.disconnect()
