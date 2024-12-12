import asyncio
import json

class Node:
    def __init__(self, node_id, neighbors, ip, port):
        self.node_id = node_id
        self.neighbors = neighbors  # List of tuples (neighbor_id, IP, Port, weight)
        self.ip = ip
        self.port = port
        self.distances = {node_id: float('inf') for node_id, _, _, _ in neighbors}
        self.distances[self.node_id] = 0
        self.updated = True

    async def send_message(self, neighbor_ip, neighbor_port, distance):
        reader, writer = await asyncio.open_connection(neighbor_ip, neighbor_port)
        message = json.dumps({"sender": self.node_id, "distance": distance})
        writer.write(message.encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def listen(self):
        server = await asyncio.start_server(self.handle_connection, self.ip, self.port)
        async with server:
            await server.serve_forever()

    async def handle_connection(self, reader, writer):
        data = await reader.read(1024)
        message = json.loads(data.decode())
        sender = message["sender"]
        distance = message["distance"]

        if distance < self.distances[self.node_id]:
            self.distances[self.node_id] = distance
            self.updated = True
        writer.close()
        await writer.wait_closed()

    async def propagate_updates(self):
        while True:
            if self.updated:
                self.updated = False
                for neighbor_id, neighbor_ip, neighbor_port, weight in self.neighbors:
                    new_distance = self.distances[self.node_id] + weight
                    await self.send_message(neighbor_ip, neighbor_port, new_distance)
            await asyncio.sleep(0.1)  # Simulate periodic updates
