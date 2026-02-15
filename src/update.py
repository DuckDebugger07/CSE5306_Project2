import os
import sqlite3
import grpc
from concurrent import futures

import drone_pb2
import drone_pb2_grpc

AGG = "aggregation:50051"

"""
def main():
    with grpc.insecure_channel(AGG) as channel:
        stub = drone_pb2_grpc.AggregationStub(channel)
        
        for ack in stub.GetSensorData(drone_pb2.Empty()):
            print(ack.reason.split(":"))
"""

class UpdateServicer(drone_pb2_grpc.UpdateServicer):
    def __init__(self):
        self.db_path = "/data/data.db"
        
        self.aggregation_channel = grpc.insecure_channel(AGG)
        self.aggregation_stub = drone_pb2_grpc.AggregationStub(self.aggregation_channel)
        
    def UpdateSensors(self, request, context):
        drone_name = request.request
        sensor_data = {}
        
        for ack in self.aggregation_stub.GetSensorData(drone_pb2.Empty()):
            key, value = ack.reason.split(":")
            if ack.ok:
                sensor_data[key] = value
            
            else:
                sensor_data[key] = None
            
            yield drone_pb2.Ack(ok=ack.ok, reason=f"{key} : {value}")
        
        # cursor.execute("""
            # UPDATE sensors
            # SET
                # altitude = ?
                # voltage = ?
                # egt = ?
                # latitude = ?
                # vibration = ?
            # WHERE name = ?
        # """, (sensor_data))
        
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    drone_pb2_grpc.add_UpdateServicer_to_server(
        UpdateServicer(), server
    )
    server.add_insecure_port("[::]:50054")
    server.start()

    print("Update node running...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()