import os                     # 读环境变量要用 os
import pyarrow as pa
from dora import Node


def main():
    node = Node()

    # 从环境变量读参数；第二个值是"没配置时用的默认值"
    on_text = os.getenv("ON_TEXT", "开")     # 没配就默认"开"
    off_text = os.getenv("OFF_TEXT", "关")   # 没配就默认"关"

    state = False
    for event in node:
        if event["type"] == "INPUT":
            state = not state
            text = on_text if state else off_text
            node.send_output("data", pa.array([text]))
        elif event["type"] == "STOP":
            break


if __name__ == "__main__":
    main()
