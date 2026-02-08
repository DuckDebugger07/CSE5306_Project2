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
        lat = 32.7357 + 0.0001*math.cos(t/10)
        lon = -97.1081 + 0.0001*math.sin(t/10)

        lat += random.uniform(-1e-5, 1e-5)
        lon += random.uniform(-1e-5, 1e-5)

        msg = drone_pb2.DroneData(
            node="gps",
            signal="latitude",
            value=lat,
            timestamp=now()
        )

        stub.Send(msg)

        print(f"GPS {lat:.6f},{lon:.6f}")

        t += 1
        time.sleep(0.1)

main()
