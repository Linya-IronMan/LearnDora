# simulation_node.py —— DORA 仿真节点：把 PyBullet 包进数据流
import math
import os

import pyarrow as pa
import pybullet as p
import pybullet_data

from dora import Node

# Kuka IIWA 的 7 个旋转关节索引
ARM_JOINTS = [0, 1, 2, 3, 4, 5, 6]


def setup_pybullet():
    """初始化 PyBullet 并加载 Kuka 机械臂（SO-101 需要 assets 文件）。"""
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)
    p.loadURDF("plane.urdf")

    # 使用 Kuka 机械臂作为演示（7个关节）
    robot_id = p.loadURDF(
        "kuka_iiwa/model.urdf",
        useFixedBase=True,
    )

    # 禁用重力对非底座关节的影响（让仿真更稳定）
    for joint_idx in range(p.getNumJoints(robot_id)):
        p.changeDynamics(robot_id, joint_idx, linearDamping=0.2, angularDamping=0.2)

    print(f"[仿真节点] Kuka 机械臂加载完成，robot_id = {robot_id}", flush=True)
    return robot_id


def set_all_joint_positions(robot_id, angles):
    """把所有 5 个活动关节设为指定角度（角度制输入，自动转弧度）。"""
    for i, joint_idx in enumerate(ARM_JOINTS):
        angle_rad = angles[i] * math.pi / 180.0  # 角度 → 弧度
        p.setJointMotorControl2(
            bodyUniqueId=robot_id,
            jointIndex=joint_idx,
            controlMode=p.POSITION_CONTROL,
            targetPosition=angle_rad,
            maxVelocity=3.0,
        )


def get_all_joint_positions(robot_id):
    """读取所有 5 个活动关节的当前角度（返回角度制）。"""
    angles = []
    for joint_idx in ARM_JOINTS:
        state = p.getJointState(robot_id, joint_idx)
        angle_deg = state[0] * 180.0 / math.pi  # 弧度 → 角度
        angles.append(round(angle_deg, 2))
    return angles


def main():
    # 初始化 PyBullet
    robot_id = setup_pybullet()

    # 当前的 7 个关节目标角度（初始全 0）
    current_targets = [0.0] * len(ARM_JOINTS)

    node = Node()

    for event in node:
        # —— 处理 DORA 输入事件 ——
        if event["type"] == "INPUT":
            if event["id"] == "tick":
                # 定时器触发：步进仿真
                set_all_joint_positions(robot_id, current_targets)
                p.stepSimulation()

                # 发送当前关节状态
                joint_angles = get_all_joint_positions(robot_id)
                node.send_output(
                    "joint_state",
                    pa.array(joint_angles),
                )

            elif event["id"] == "joint_cmd":
                # 收到控制指令
                data = event["value"].to_pylist()

                if len(data) == 2 and data[0] < 10:
                    # 格式：[joint_idx, angle] —— 单个关节指令
                    joint_idx = int(data[0])
                    angle = float(data[1])
                    if 0 <= joint_idx < len(ARM_JOINTS):
                        current_targets[joint_idx] = angle
                        print(
                            f"[仿真节点] 关节 {joint_idx} 目标 → {angle}°",
                            flush=True,
                        )
                elif len(data) == 5:
                    # 格式：[angle_0, ..., angle_4] —— 全关节批量指令
                    current_targets = [float(a) for a in data]
                    print(
                        f"[仿真节点] 全关节目标 → {current_targets}°",
                        flush=True,
                    )

        elif event["type"] == "STOP":
            break

    p.disconnect()


if __name__ == "__main__":
    main()
