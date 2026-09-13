#!/usr/bin/env python3
"""交互式控制 Kuka 机械臂 - 独立运行，无需 dora"""
import pybullet as p
import pybullet_data
import time

# Kuka IIWA 的 7 个旋转关节索引
ARM_JOINTS = [0, 1, 2, 3, 4, 5, 6]

def setup_pybullet():
    """初始化 PyBullet 并加载 Kuka 机械臂"""
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)
    p.loadURDF("plane.urdf")
    
    robot_id = p.loadURDF("kuka_iiwa/model.urdf", useFixedBase=True)
    
    print(f"✓ Kuka 机械臂加载完成，robot_id = {robot_id}")
    print(f"✓ 关节数量: {p.getNumJoints(robot_id)}")
    return robot_id

def set_joint_angles(robot_id, angles):
    """设置所有关节角度（度）"""
    import math
    for i, joint_idx in enumerate(ARM_JOINTS):
        angle_rad = angles[i] * math.pi / 180.0
        p.setJointMotorControl2(
            robot_id, joint_idx,
            p.POSITION_CONTROL,
            targetPosition=angle_rad,
            force=500
        )

def main():
    robot_id = setup_pybullet()
    
    print("\n" + "="*50)
    print("  Kuka 机械臂交互控制")
    print("="*50)
    print("命令:")
    print("  home             - 回零")
    print("  0 45             - 关节0转45度")
    print("  batch 0 -30 45 -20 10 0 0  - 批量控制")
    print("  quit             - 退出")
    print("="*50)
    
    current_angles = [0.0] * 7
    
    while True:
        try:
            cmd = input("\n> ").strip()
            
            if not cmd:
                continue
                
            if cmd == "quit":
                break
                
            if cmd == "home":
                current_angles = [0.0] * 7
                set_joint_angles(robot_id, current_angles)
                print("✓ 回零")
                
            elif cmd.startswith("batch"):
                parts = cmd.split()[1:]
                if len(parts) != 7:
                    print("✗ 需要7个角度值")
                    continue
                current_angles = [float(x) for x in parts]
                set_joint_angles(robot_id, current_angles)
                print(f"✓ 设置角度: {current_angles}")
                
            else:
                parts = cmd.split()
                if len(parts) != 2:
                    print("✗ 格式错误")
                    continue
                joint_id = int(parts[0])
                angle = float(parts[1])
                if joint_id < 0 or joint_id >= 7:
                    print("✗ 关节号应为0-6")
                    continue
                current_angles[joint_id] = angle
                set_joint_angles(robot_id, current_angles)
                print(f"✓ 关节{joint_id}设置为{angle}度")
            
            # 步进仿真让机械臂移动到目标位置
            for _ in range(240):
                p.stepSimulation()
                time.sleep(1./240.)
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"✗ 错误: {e}")
    
    p.disconnect()
    print("\n再见！")

if __name__ == "__main__":
    main()
