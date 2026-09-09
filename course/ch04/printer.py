# printer.py —— 打印机节点
# 职责：收到数据就打印到屏幕，让我们肉眼确认数据在流动。

from dora import Node


def main():
    node = Node()

    for event in node:
        if event["type"] == "INPUT":
            # event["value"] 是 Arrow 数组，用 .to_pylist() 变回普通 Python 列表好打印
            data = event["value"].to_pylist()
            if event["id"] == "sender":
                print(f"printer 收到来自 sender 的数据: {data}", flush=True)
            elif event["id"] == "echo":
                print(f"printer 收到来自 echo 的数据: {data}", flush=True)
            # print(f"printer 收到：{data}", flush=True)

        elif event["type"] == "STOP":
            break


if __name__ == "__main__":
    main()
