import time, math, random, grpc
import drone_pb2, drone_pb2_grpc

AGG = "aggregation:50051"

def now(): return int(time.time()*1000)

def main():

    stub = drone_pb2_grpc.AggregationStub(
        grpc.insecure_channel(AGG)
    )

    t = 0

    while True:
        altitude = 200 + 10*math.sin(t/5) + random.uniform(-1,1)

        msg = drone_pb2.DroneData(
            node="airdata",
            signal="altitude",
            value=altitude,
            timestamp=now()
        )

        stub.Send(msg)
        print(f"Altitude {altitude:.1f}")

        t += 1
        time.sleep(0.1)

main()
