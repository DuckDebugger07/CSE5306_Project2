import time
import grpc
from concurrent import futures

import drone_pb2
import drone_pb2_grpc

ANALYSIS_ADDR = "analysis:50052"
SENSOR_PORT = 50060


class AggregationServicer(drone_pb2_grpc.AggregationServicer):
    def __init__(self):
        self.analysis_channel = grpc.insecure_channel(ANALYSIS_ADDR)
        self.analysis_stub = drone_pb2_grpc.AnalysisStub(self.analysis_channel)
        
        self.airdata_channel = grpc.insecure_channel(f"airdata:{SENSOR_PORT + 0}")
        self.airdata_stub = drone_pb2_grpc.SensorStub(self.airdata_channel)
        
        self.battery_channel = grpc.insecure_channel(f"battery:{SENSOR_PORT + 1}")
        self.battery_stub = drone_pb2_grpc.SensorStub(self.battery_channel)
        
        self.engine_channel = grpc.insecure_channel(f"engine:{SENSOR_PORT + 2}")
        self.engine_stub = drone_pb2_grpc.SensorStub(self.engine_channel)
        
        self.gps_channel = grpc.insecure_channel(f"gps:{SENSOR_PORT + 3}")
        self.gps_stub = drone_pb2_grpc.SensorStub(self.gps_channel)
        
        # self.imu_channel = grpc.insecure_channel(f"gps:{SENSOR_PORT + 4}")
        # self.imu_stub = drone_pb2_grpc.SensorStub(self.imu_channel)
        
        self.stubs = [
            self.airdata_stub,
            self.battery_stub,
            self.engine_stub,
            self.gps_stub,
            # self.imu_stub
        ]
    
    def GetSensorData(self, request, context):        
        for stub in self.stubs:
            response = stub.GetData(drone_pb2.Empty())
            reason = f"{response.node}: {response.signal}, {response.value}, {response.timestamp}\n"
            
            analysis = self.analysis_stub.Analyze(response)
            
            yield drone_pb2.Ack(ok=True, reason=reason)
            


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    drone_pb2_grpc.add_AggregationServicer_to_server(
        AggregationServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()

    print("Aggregation node running...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
