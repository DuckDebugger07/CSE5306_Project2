import time
import grpc
from concurrent import futures

import drone_pb2
import drone_pb2_grpc

ANALYSIS_ADDR = "analysis:50052"


class AggregationServicer(drone_pb2_grpc.AggregationServicer):
    def __init__(self):
        self.analysis_channel = grpc.insecure_channel(ANALYSIS_ADDR)
        self.analysis_stub = drone_pb2_grpc.AnalysisStub(self.analysis_channel)

    def Send(self, request, context):
        print(f"[AGG] {request.node}:{request.signal} = {request.value:.2f}")

        # Forward to analysis
        self.analysis_stub.Analyze(request)

        return drone_pb2.Ack(ok=True)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    drone_pb2_grpc.add_AggregationServicer_to_server(
        AggregationServicer(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()

    print("Aggregation node running...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
