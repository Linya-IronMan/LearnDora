import os
from dora import Node

def main():
    node = Node()
    message = os.getenv("MESSAGE", "小莫还活着~")
    for event in node:
        if event["type"] == "INPUT":
            print(message, flush=True)
        elif event["type"] == "STOP":
            break

if __name__ == "__main__":
    main()
