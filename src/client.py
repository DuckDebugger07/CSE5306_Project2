import grpc

import drone_pb2
import drone_pb2_grpc

SERVER_ADDR = "server:50053"

def run():
    print("Checking if Server is up ...")
    
    with grpc.insecure_channel(SERVER_ADDR) as channel:
        stub = drone_pb2_grpc.QueryStub(channel)
        response = stub.CheckRunning(drone_pb2.Empty())

    if response.ok:
        print("Server is up!")
    else:
        print("Server is not up, exiting...!")
        exit()
    
    usr_query = ""
    
    while usr_query != "quit":
        usr_query = input("Query: ")
        
        with grpc.insecure_channel(SERVER_ADDR) as channel:
            stub = drone_pb2_grpc.QueryStub(channel)
            response = stub.SendQuery(drone_pb2.ClientQuery(request=usr_query))
        
        print(f"\n{'=' * 20}")
        print(response.reply)
        print(f"{'=' * 20}\n")


if __name__ == "__main__":
    run()