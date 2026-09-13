# keyboard_control.py —— 键盘控制 SO-101 的 DORA 节点
import pyarrow as pa

from dora import Node

# SO-101 的 5 个活动关节名称
JOINT_NAMES = [
    "shoulder_pan (基座旋转)",
    "shoulder_lift (大臂抬起)",
    "elbow_flex (肘部弯曲)",
    "wrist_flex (手腕俯仰)",
    "wrist_roll (手腕旋转)",
]


def main():
    node = Node()

    print("=" * 50, flush=True)
    print("  SO-101 键盘控制", flush=True)
    print("=" * 50, flush=True)
    print("  命令格式：", flush=True)
    print("    关节号 角度     如 '0 45'", flush=True)
    print("    batch a0 a1 a2 a3 a4  如 'batch 0 -30 45 -20 10'", flush=True)
    print("    home            回零", flush=True)
    print("    list            显示关节列表", flush=True)
    print("=" * 50, flush=True)

    for event in node:
        if event["type"] == "INPUT" and event["id"] == "tick":
            cmd = input("> ").strip()

            if not cmd:
                continue

            # —— 回零 ——
            if cmd == "home":
                node.send_output("joint_cmd", pa.array([0.0, 0.0, 0.0, 0.0, 0.0]))
                print("  → 回零指令已发送", flush=True)
                continue

            # —— 显示关节列表 ——
            if cmd == "list":
                for i, name in enumerate(JOINT_NAMES):
                    print(f"    {i}: {name}", flush=True)
                continue

            # —— 批量控制 ——
            if cmd.startswith("batch"):
                parts = cmd.split()
                if len(parts) != 6:
                    print("  batch 命令格式：batch a0 a1 a2 a3 a4", flush=True)
                    continue
                angles = [float(a) for a in parts[1:]]
                node.send_output("joint_cmd", pa.array(angles))
                print(f"  → 全关节 → {angles}°", flush=True)
                continue

            # —— 单关节控制 ——
            parts = cmd.split()
            if len(parts) != 2:
                print("  格式错误：关节号 角度", flush=True)
                continue

            joint_idx = int(parts[0])
            angle = float(parts[1])

            if joint_idx < 0 or joint_idx >= len(JOINT_NAMES):
                print(f"  关节号范围 0-{len(JOINT_NAMES) - 1}", flush=True)
                continue

            # 发送单关节指令：用 [joint_idx, angle] 格式
            node.send_output("joint_cmd", pa.array([joint_idx, angle]))
            print(
                f"  → 关节 {joint_idx} ({JOINT_NAMES[joint_idx]}) → {angle}°",
                flush=True,
            )

        elif event["type"] == "STOP":
            break


if __name__ == "__main__":
    main()
