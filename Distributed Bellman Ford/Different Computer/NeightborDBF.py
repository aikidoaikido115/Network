import asyncio


async def main():
    # Define the graph
    # (neighbor_id, IP, Port, weight)
    node_definitions = {
        0: [(1, "127.0.0.1", 9001, 1), (2, "127.0.0.1", 9002, 4)],
        1: [(0, "127.0.0.1", 9000, 1), (2, "127.0.0.1", 9002, 2), (3, "127.0.0.1", 9003, 6)],
        2: [(0, "127.0.0.1", 9000, 4), (1, "127.0.0.1", 9001, 2), (3, "127.0.0.1", 9003, 3)],
        3: [(1, "127.0.0.1", 9001, 6), (2, "127.0.0.1", 9002, 3)]
    }

    # Define IPs and ports for this node
    node_id = int(input("Enter this node's ID: "))
    ip = "127.0.0.1"  # Change to your computer's IP
    port = 9000 + node_id

    neighbors = node_definitions[node_id]
    node = Node(node_id, neighbors, ip, port)

    # Start listening and propagating
    await asyncio.gather(node.listen(), node.propagate_updates())

if __name__ == "__main__":
    asyncio.run(main())
