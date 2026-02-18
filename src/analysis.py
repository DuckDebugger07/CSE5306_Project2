import grpc
from concurrent import futures

import drone_pb2
import drone_pb2_grpc


class AnalysisServicer(drone_pb2_grpc.AnalysisServicer):

    def Analyze(self, request, context):
        ack_bool = True
        reason = ""
        
        if request.signal == "egt":
            if request.value > 800:
                reason = "Engine: over-temp!"
                ack_bool = False
            else:
                reason = "Engine: good"

        if request.signal == "voltage":
            if request.value < 13:
                reason = "Battery: low!"
                ack_bool = False
            else:
                reason = "Battery: good"

        if request.signal == "vibration":
            if request.value > 0.8:
                reason = "Vibration: excess!"
                ack_bool = False
            else:
                reason = "Vibration: good"
        print(f"{request.signal} {ack_bool} {reason}")
        return drone_pb2.Ack(ok=ack_bool, reason=reason)


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
