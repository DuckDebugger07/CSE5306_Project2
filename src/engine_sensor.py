import time, math, random, grpc
import drone_pb2, drone_pb2_grpc

AGG = "aggregation:50051"

def now(): return int(time.time()*1000)

def main():
    stub = drone_pb2_grpc.AggregationStub(grpc.insecure_channel(AGG))
    t = 0

    while True:
        # normal engine behavior
        egt = 650 + 50*math.sin(t/10) + random.uniform(-5,5)

        # fault injection: occasional over-temp spike
        if random.random() < 0.05:
            egt += random.uniform(180, 250)

        msg = drone_pb2.DroneData(
            node="engine",
            signal="EGT",
            value=egt,
            timestamp=now()
        )

        stub.Send(msg)
        print(f"Engine EGT {egt:.1f}")

        t += 1
        time.sleep(0.1)

if __name__ == "__main__":
    main()
