import time, math, random, grpc
import drone_pb2, drone_pb2_grpc
from concurrent import futures

AGG = "aggregation:50051"

class Airdata(drone_pb2_grpc.SensorServicer):
    t = 0
    
    def now (self):
        return int(time.time()*1000)
    
    def GetData(self, unknown, context):
        altitude = 200 + 10*math.sin(self.t/5) + random.uniform(-1,1)
        self.t += 1
        
        return drone_pb2.DroneData(
            node="airdata",
            signal="altitude",
            value=altitude,
            timestamp=self.now()
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    drone_pb2_grpc.add_SensorServicer_to_server(Airdata(), server)
    server.add_insecure_port("[::]:50060")
    server.start()
    print("Airdata sensor running...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()