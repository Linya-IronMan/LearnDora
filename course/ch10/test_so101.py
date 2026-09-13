# test_so101.py —— 在 PyBullet GUI 中加载并显示 SO-101 机械臂
import os
import time

import pybullet as p
import pybullet_data

# —— 路径设置 ——
# 使用 PyBullet 自带的 Kuka 机械臂作为示例
# 如需使用 SO-101，请确保 so101_new_calib.urdf 和 assets/ 目录都存在

# —— 启动仿真 ——
p.connect(p.GUI)  # GUI 模式：打开可视化窗口
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.81)  # 设置重力

# 加载地面
p.loadURDF("plane.urdf")

# 加载 Kuka 机械臂（PyBullet 自带，用于演示）
robot_id = p.loadURDF(
    "kuka_iiwa/model.urdf",
    basePosition=[0, 0, 0],
    baseOrientation=[0, 0, 0, 1],  # 四元数：(x, y, z, w)，无旋转
    useFixedBase=True,  # 机械臂底座固定，不能移动
)

print(f"SO-101 已加载，robot_id = {robot_id}", flush=True)

# —— 查看关节信息 ——
num_joints = p.getNumJoints(robot_id)
print(f"关节数量: {num_joints}\n", flush=True)

for i in range(num_joints):
    info = p.getJointInfo(robot_id, i)
    joint_name = info[1].decode()  # info[1] 是名称（bytes）
    joint_type = info[2]  # info[2] 是类型
    type_name = {
        0: "旋转关节 (Revolute)",
        1: "棱柱关节 (Prismatic)",
        4: "固定关节 (Fixed)",
    }.get(joint_type, f"其他 ({joint_type})")
    print(
        f"  关节 {i}: {joint_name:30s}  类型: {type_name}",
        flush=True,
    )

# —— 持续运行 ——
print("\n运行中... 按 Ctrl+C 退出", flush=True)
try:
    while True:
        p.stepSimulation()  # 推进仿真一步
        time.sleep(1 / 240)  # 约 240Hz 的仿真频率
except KeyboardInterrupt:
    print("\n停止仿真", flush=True)

p.disconnect()  # 关闭窗口
