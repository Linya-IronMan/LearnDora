# echo.py —— 回声节点
# 职责：收到任何数据，都原样转发到自己的 data 输出上。

from dora import Node


def main():
    node = Node()

    for event in node:
        if event["type"] == "INPUT":
            # 原样转发：把收到的数据和元信息，一模一样地写回黑板
            node.send_output("data", event["value"], event["metadata"])

        elif event["type"] == "STOP":
            break


if __name__ == "__main__":
    main()
