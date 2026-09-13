#!/usr/bin/env python3
"""直接向仿真节点发送关节命令"""
import sys
import pyarrow as pa
from dora import Node

def main():
    if len(sys.argv) < 2:
        print("用法: python send_command.py <命令>")
        print("示例:")
        print("  python send_command.py home           # 回零")
        print("  python send_command.py 0 45           # 关节0转45度")
        print("  python send_command.py batch 0 -30 45 -20 10 0 0  # 批量控制")
        return
    
    node = Node("command_sender")
    cmd = " ".join(sys.argv[1:])
    
    if cmd == "home":
        angles = [0.0] * 7
        node.send_output("joint_cmd", pa.array(angles))
        print("✓ 回零指令已发送")
    elif cmd.startswith("batch"):
        parts = cmd.split()[1:]
        if len(parts) != 7:
            print("✗ batch 需要7个角度值")
            return
        angles = [float(x) for x in parts]
        node.send_output("joint_cmd", pa.array(angles))
        print(f"✓ 批量指令已发送: {angles}")
    else:
        parts = cmd.split()
        if len(parts) != 2:
            print("✗ 格式错误，应为: 关节号 角度")
            return
        joint_id = int(parts[0])
        angle = float(parts[1])
        # 获取当前状态并修改单个关节
        angles = [0.0] * 7
        angles[joint_id] = angle
        node.send_output("joint_cmd", pa.array(angles))
        print(f"✓ 关节{joint_id}设置为{angle}度")

if __name__ == "__main__":
    main()
