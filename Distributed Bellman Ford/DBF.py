from collections import defaultdict
import threading
import time

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
        self.lock = threading.Lock()

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
        for neighbor_id, weight in node.neighbors.items():
            neighbor = self.nodes[neighbor_id]
            with self.lock:
                if node.distance + weight < neighbor.distance:
                    neighbor.distance = node.distance + weight
                    neighbor.predecessor = node_id

    def run(self, source, max_iterations=None):
        self.initialize_source(source)
        threads = []
        iteration = 0
        while max_iterations is None or iteration < max_iterations:
            print(f"Iteration {iteration + 1}")
            for node_id in self.nodes:
                thread = threading.Thread(target=self.relax, args=(node_id,))
                threads.append(thread)
                thread.start()

            # Wait for all threads to finish
            for thread in threads:
                thread.join()

            threads = []  # Reset threads for the next iteration
            iteration += 1
            # Check if there are updates (for an optimized version)
            # Optionally implement a termination condition here
            time.sleep(0.1)

        # Print final distances
        for node_id, node in self.nodes.items():
            print(f"Node {node_id}: Distance = {node.distance}, Predecessor = {node.predecessor}")

# Example usage
if __name__ == "__main__":
    network = DistributedBellmanFord()

    # Adding nodes
    for node_id in range(5):
        network.add_node(node_id)

    # Adding edges (directed graph with weights)
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

    # Running the distributed Bellman-Ford algorithm
    source_node = 0
    network.run(source_node, max_iterations=4)  # Set a maximum number of iterations
