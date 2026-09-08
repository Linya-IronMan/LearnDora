# counter.py —— 可配置的计数器
import os
import pyarrow as pa
from dora import Node


def main():
    node = Node()

    start = int(os.getenv("START", "0"))     # 从几开始数
    step = int(os.getenv("STEP", "1"))       # 每次加多少

    count = start
    for event in node:
        if event["type"] == "INPUT":
            node.send_output("data", pa.array([count]))
            count = count + step             # 按配置的步长递增
        elif event["type"] == "STOP":
            break


if __name__ == "__main__":
    main()
