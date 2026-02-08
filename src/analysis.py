import grpc
from concurrent import futures

import drone_pb2
import drone_pb2_grpc


class AnalysisServicer(drone_pb2_grpc.AnalysisServicer):

    def Analyze(self, request, context):
        if request.signal == "EGT" and request.value > 800:
            print("[ALERT] Engine over-temp!")

        if request.signal == "voltage" and request.value < 13:
            print("[ALERT] Battery low!")

        if request.signal == "vibration" and request.value > 0.8:
            print("[ALERT] Excess vibration!")

        return drone_pb2.Ack(ok=True)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    drone_pb2_grpc.add_AnalysisServicer_to_server(
        AnalysisServicer(), server
    )
    server.add_insecure_port("[::]:50052")
    server.start()

    print("Analysis node running...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
