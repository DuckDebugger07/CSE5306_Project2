import grpc
from concurrent import futures

import drone_pb2
import drone_pb2_grpc

class Query(drone_pb2_grpc.QueryServicer):
    def CheckRunning(self, unknown, context):
        return drone_pb2.Ack(ok=True, reason="")
    
    def SendQuery(self, query, context):
        return drone_pb2.ServerReply(reply="I see you just said, %s!" % query.request);

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    drone_pb2_grpc.add_QueryServicer_to_server(Query(), server)
    server.add_insecure_port("[::]:50053")

    server.start()
    print(f"Server started...")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

# # https://stackoverflow.com/questions/31768665/can-i-define-a-grpc-call-with-a-null-request-or-response
# # https://stackoverflow.com/questions/68436373/docker-compose-up-with-input-argumen