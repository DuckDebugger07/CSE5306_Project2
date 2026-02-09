import time, math, random, grpc
import drone_pb2, drone_pb2_grpc
from concurrent import futures

AGG = "aggregation:50051"

class Gps(drone_pb2_grpc.SensorServicer):
    t = 0
    
    def now (self):
        return int(time.time()*1000)
    
    def GetData(self, unknown, context):
        lat = 32.7357 + 0.0001*math.cos(self.t/10)
        lon = -97.1081 + 0.0001*math.sin(self.t/10)

        lat += random.uniform(-1e-5, 1e-5)
        lon += random.uniform(-1e-5, 1e-5)
        
        self.t += 1
        
        return drone_pb2.DroneData(
            node="gps",
            signal="latitude",
            value=lat,
            timestamp=self.now()
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    drone_pb2_grpc.add_SensorServicer_to_server(Gps(), server)
    server.add_insecure_port("[::]:50063")
    server.start()
    print("Gps sensor running...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()