import asyncio
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, node_id, neighbors):
        self.node_id = node_id
        self.neighbors = neighbors  # List of tuples (neighbor_id, weight)
        self.distances = {node_id: float('inf') for node_id, _ in neighbors}
        self.distances[self.node_id] = 0
        self.message_queue = asyncio.Queue()
        self.updated = True  # Track if updates occur for termination

    async def send_message(self, to_node, distance):
        await to_node.message_queue.put((self.node_id, distance))

    async def process_messages(self, nodes, max_iterations):
        iteration = 0
        while iteration < max_iterations:
            self.updated = False
            try:
                while not self.message_queue.empty():
                    sender, distance = await self.message_queue.get()
                    if distance < self.distances[self.node_id]:
                        self.distances[self.node_id] = distance
                        self.updated = True

                # Propagate updated distances to neighbors
                if self.updated:
                    for neighbor_id, weight in self.neighbors:
                        new_distance = self.distances[self.node_id] + weight
                        await self.send_message(nodes[neighbor_id], new_distance)
            except Exception as e:
                print(f"Error in Node {self.node_id}: {e}")

            await asyncio.sleep(0.1)  # Simulate periodic updates
            iteration += 1


async def main():
    # Define the graph as adjacency list
    graph = {
        0: [(1, 1), (2, 4)],
        1: [(0, 1), (2, 2), (3, 6)],
        2: [(0, 4), (1, 2), (3, 3)],
        3: [(1, 6), (2, 3)]
    }

    # Create nodes
    nodes = {node_id: Node(node_id, neighbors) for node_id, neighbors in graph.items()}

    # Define maximum iterations to simulate distributed system
    max_iterations = len(graph) * 2  # At most 2x the number of nodes
    tasks = [node.process_messages(nodes, max_iterations) for node in nodes.values()]

    # Start processing
    await asyncio.gather(*tasks)

    # Draw the graph with networkx
    G = nx.DiGraph()
    for node_id, neighbors in graph.items():
        for neighbor, weight in neighbors:
            G.add_edge(node_id, neighbor, weight=weight)

    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    # Draw the nodes, edges, and labels
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2000, font_size=15)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")
    plt.title("Graph Representation with Weights")
    plt.show()

    # Print final distances
    for node_id, node in nodes.items():
        print(f"Node {node_id} distances: {node.distances}")

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
