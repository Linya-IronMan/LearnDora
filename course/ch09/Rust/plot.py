# plot.py —— 把收到的信号值画成字符条形图
from dora import Node


def main():
    node = Node()

    for event in node:
        if event["type"] == "INPUT":
            if event["id"] == "value":
                value = event["value"][0].as_py()   # 读 Rust 发来的 Arrow 数据

                # 把 -10~10 映射成 0~20 的条长
                bar_len = int(value + 10)
                bar_len = max(0, min(20, bar_len))
                bar = "█" * bar_len
                print(f"{value:7.2f} | {bar}", flush=True)

        elif event["type"] == "STOP":
            break


if __name__ == "__main__":
    main()
