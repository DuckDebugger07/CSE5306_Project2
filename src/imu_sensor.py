import time, random, grpc
import drone_pb2, drone_pb2_grpc

AGG = "aggregation:50051"

def now(): return int(time.time()*1000)

def main():
    stub = drone_pb2_grpc.AggregationStub(grpc.insecure_channel(AGG))

    while True:
        vib = random.uniform(0.1, 0.4)

        # fault injection: vibration spike
        if random.random() < 0.06:
            vib = random.uniform(0.9, 1.5)

        msg = drone_pb2.DroneData(
            node="imu",
            signal="vibration",
            value=vib,
            timestamp=now()
        )

        stub.Send(msg)
        print(f"Vibration {vib:.2f}")

        time.sleep(0.1)

if __name__ == "__main__":
    main()
