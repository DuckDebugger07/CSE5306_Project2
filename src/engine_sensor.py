import time, math, random, grpc
import drone_pb2, drone_pb2_grpc
from concurrent import futures

AGG = "aggregation:50051"

class Engine(drone_pb2_grpc.SensorServicer):   
    t = 0
    
    def now (self):
        return int(time.time()*1000)
    
    def GetData(self, unknown, context):
        egt = 650 + 50*math.sin(self.t/10) + random.uniform(-5,5)
        self.t += 1
        
        if random.random() < 0.05:
            egt += random.uniform(180, 250)
        
        return drone_pb2.DroneData(
            node="engine",
            signal="egt",
            value=egt,
            timestamp=self.now()
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    drone_pb2_grpc.add_SensorServicer_to_server(Engine(), server)
    server.add_insecure_port("[::]:50062")
    server.start()
    print("Engine sensor running...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()