import time, random, grpc
import drone_pb2, drone_pb2_grpc
from concurrent import futures

AGG = "aggregation:50060"

class Battery(drone_pb2_grpc.SensorServicer):
    voltage = 16.8
    
    def now (self):
        return int(time.time()*1000)
    
    def GetData(self, unknown, context):
        self.voltage -= 0.002
        
        if random.random() < 0.04:
            self.voltage -= random.uniform(1.5, 3.0)
        
        return drone_pb2.DroneData(
            node="battery",
            signal="voltage",
            value=self.voltage,
            timestamp=self.now()
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    drone_pb2_grpc.add_SensorServicer_to_server(Battery(), server)
    server.add_insecure_port("[::]:50061")
    server.start()
    print("Battery sensor running...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()