# test_so101_joints.py —— 逐关节测试 SO-101 的运动范围
import os
import pybullet as p
import pybullet_data
import time

urdf_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "docs/public/SO101",
)
urdf_path = os.path.join(urdf_dir, "so101_new_calib.urdf")

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)
p.loadURDF("plane.urdf")
p.setAdditionalSearchPath(urdf_dir)

robot_id = p.loadURDF(
    urdf_path,
    useFixedBase=True,
)

# —— 逐关节旋转演示 ——
joint_indices = [0, 1, 2, 3, 4]        # 5 个活动旋转关节
angles = [0.5, -0.5, 0.5, -0.5, 0.5]  # 目标角度（弧度）

for step in range(500):
    for i, joint_idx in enumerate(joint_indices):
        p.setJointMotorControl2(
            bodyUniqueId=robot_id,
            jointIndex=joint_idx,
            controlMode=p.POSITION_CONTROL,
            targetPosition=angles[i],          # 目标角度（弧度）
            maxVelocity=3.0,                   # 最大角速度
        )
    p.stepSimulation()
    time.sleep(1 / 240)

# —— 读取当前关节状态 ——
print("\n当前关节角度:", flush=True)
for i in joint_indices:
    state = p.getJointState(robot_id, i)
    pos = state[0]                            # 当前角度（弧度）
    print(f"  关节 {i}: {pos * 180 / 3.14159:.1f}°", flush=True)

# 保持窗口打开
print("\n观察机械臂姿态，按 Ctrl+C 退出", flush=True)
try:
    while True:
        p.stepSimulation()
        time.sleep(1 / 240)
except KeyboardInterrupt:
    p.disconnect()
