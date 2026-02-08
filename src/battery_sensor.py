import time, random, grpc
import drone_pb2, drone_pb2_grpc

AGG = "aggregation:50051"

def now(): return int(time.time()*1000)

def main():
    stub = drone_pb2_grpc.AggregationStub(grpc.insecure_channel(AGG))
    voltage = 16.8

    while True:
        voltage -= 0.002

        # fault injection: sudden sag
        if random.random() < 0.04:
            voltage -= random.uniform(1.5, 3.0)

        msg = drone_pb2.DroneData(
            node="battery",
            signal="voltage",
            value=voltage,
            timestamp=now()
        )

        stub.Send(msg)
        print(f"Battery V {voltage:.2f}")

        time.sleep(0.1)

if __name__ == "__main__":
    main()
