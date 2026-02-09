import grpc
from concurrent import futures

import drone_pb2
import drone_pb2_grpc


class AnalysisServicer(drone_pb2_grpc.AnalysisServicer):

    def Analyze(self, request, context):
        reason = ""
        
        if request.signal == "EGT" and request.value > 800:
            reason = "Engine: over-temp!\n"
            # print("[ALERT] Engine over-temp!")
        else:
            reason += "Engine: good"

        if request.signal == "voltage" and request.value < 13:
            reason += "Battery: low!\n"
            # print("[ALERT] Battery low!")
        else:
            reason += "Battery: good"

        if request.signal == "vibration" and request.value > 0.8:
            reason += "Vibration: excess!\n"
            # print("[ALERT] Excess vibration!")
        else:
            reason += "Vibration: good"

        return drone_pb2.Ack(ok=True, reason=reason)


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
