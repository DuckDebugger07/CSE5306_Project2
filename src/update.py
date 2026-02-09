import grpc

import drone_pb2
import drone_pb2_grpc

AGG = "aggregation:50051"

def main():
    with grpc.insecure_channel(AGG) as channel:
        stub = drone_pb2_grpc.AggregationStub(channel)
        # response = stub.GetSensorData(drone_pb2.Empty())
        
        for ack in stub.GetSensorData(drone_pb2.Empty()):
            print(ack.reason.split(":"))

if __name__ == "__main__":
    main()