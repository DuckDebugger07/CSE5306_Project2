import time, random, grpc
import drone_pb2, drone_pb2_grpc
from concurrent import futures

AGG = "aggregation:50051"

class IMU(drone_pb2_grpc.SensorServicer):
    def now (self):
        return int(time.time()*1000)
    
    def GetData(self, unknown, context):
        vib = random.uniform(0.1, 0.4)

        # fault injection: vibration spike
        if random.random() < 0.06:
            vib = random.uniform(0.9, 1.5)
        
        return drone_pb2.DroneData(
            node="imu",
            signal="vibration",
            value=vib,
            timestamp=self.now()
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    drone_pb2_grpc.add_SensorServicer_to_server(IMU(), server)
    server.add_insecure_port("[::]:50064")
    server.start()
    print("IMU sensor running...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

