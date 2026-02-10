import grpc

import drone_pb2
import drone_pb2_grpc

AGG = "aggregation:50051"

def main():
    with grpc.insecure_channel(AGG) as channel:
        stub = drone_pb2_grpc.AggregationStub(channel)
        
        for ack in stub.GetSensorData(drone_pb2.Empty()):
            print(ack.reason.split(":"))

if __name__ == "__main__":
    main()

cols = ["NAME", "ALTITUDE", "VOLTAGE", "EGT", "LATITUDE", "VIBRATION"]

def print_table():
    amt = len(cols)
    
    print(*[c.center(9) for c in cols], sep=" | ")
    print('-' * ((9 * amt) + (3 * (amt - 1))) )
    # print('-' * 69)

NAME | ALTITUDE | VOLTAGE | EGT | LATITUDE | VIBRATION
