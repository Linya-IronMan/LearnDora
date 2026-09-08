import pyarrow as pa
from dora import Node


def main():
	node = Node()

	state = False

	for event in node:
		if event["type"] == "INPUT":
			state = not state

			status_text = "开" if state else "关"
			node.send_output("data", pa.array([status_text]))

		elif event["type"] == "STOP":
			break

if __name__ == "__main__":
	main()
