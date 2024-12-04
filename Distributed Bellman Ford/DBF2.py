# จาก ver 1
# เพิ่ม early stopping, multithreading, ThreadPoolExecutor
from collections import defaultdict
import threading
from concurrent.futures import ThreadPoolExecutor

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.neighbors = {}
        self.distance = float('inf')
        self.predecessor = None

    def add_neighbor(self, neighbor_id, weight):
        self.neighbors[neighbor_id] = weight

    def __repr__(self):
        return f"Node({self.node_id}, dist={self.distance}, pred={self.predecessor})"

class DistributedBellmanFord:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node_id):
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id)

    def add_edge(self, src, dest, weight):
        if src in self.nodes and dest in self.nodes:
            self.nodes[src].add_neighbor(dest, weight)

    def initialize_source(self, source):
        if source in self.nodes:
            self.nodes[source].distance = 0

    def relax(self, node_id):
        node = self.nodes[node_id]
        updated = False
        for neighbor_id, weight in node.neighbors.items():
            neighbor = self.nodes[neighbor_id]
            if node.distance + weight < neighbor.distance:
                neighbor.distance = node.distance + weight
                neighbor.predecessor = node_id
                updated = True
        return updated

    def run(self, source, max_iterations=None):
        self.initialize_source(source)
        iteration = 0
        with ThreadPoolExecutor(max_workers=len(self.nodes)) as executor:
            while True:
                print(f"Iteration {iteration + 1}")
                futures = []

                # Submit jobs to each node to perform relaxation
                for node_id in self.nodes:
                    futures.append(executor.submit(self.relax, node_id))

                # Wait for all threads to complete and check if any update happened
                updated = any(future.result() for future in futures)

                iteration += 1

                # Early stopping condition: If no updates happened, break
                if not updated:
                    print("Convergence detected. Stopping early.")
                    break

                # Optional: Break after max_iterations if specified
                if max_iterations is not None and iteration >= max_iterations:
                    break

        # Output the final results
        for node_id, node in self.nodes.items():
            print(f"Node {node_id}: Distance = {node.distance}, Predecessor = {node.predecessor}")

# Example usage
if __name__ == "__main__":
    network = DistributedBellmanFord()

    # Add nodes to the graph
    for node_id in range(5):
        network.add_node(node_id)

    # Add edges to the graph
    network.add_edge(0, 1, 6)
    network.add_edge(0, 2, 7)
    network.add_edge(1, 2, 8)
    network.add_edge(1, 3, 5)
    network.add_edge(1, 4, -4)
    network.add_edge(2, 3, -3)
    network.add_edge(2, 4, 9)
    network.add_edge(3, 1, -2)
    network.add_edge(4, 0, 2)
    network.add_edge(4, 3, 7)

    # Run Bellman-Ford algorithm
    source_node = 0
    network.run(source_node, max_iterations=4)  # Set max iterations if desired
