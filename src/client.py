import grpc
from time import time

import drone_pb2
import drone_pb2_grpc

SERVER_ADDR = "server:50053"

def run():
    print("Checking if Server is up ...")
    
    while True:
        with grpc.insecure_channel(SERVER_ADDR) as channel:
            stub = drone_pb2_grpc.QueryStub(channel)
            response = stub.CheckRunning(drone_pb2.Empty())

        if response.ok:
            print("Server is up!")
            break
        else:
            print("Retrying...!")
    
    usr_query = ""
    
    while usr_query != "quit":
        usr_query = input("Query: ")
        
        start = time()
        
        with grpc.insecure_channel(SERVER_ADDR) as channel:
            stub = drone_pb2_grpc.QueryStub(channel)
            response = stub.SendQuery(drone_pb2.ClientQuery(request=usr_query))
        
        end = time()
        
        print(f"\n{'=' * 20}")
        print(f"Time Taken: {end - start}", end="\n\n")
        print(response.reply)
        print(f"{'=' * 20}", end="\n\n")


if __name__ == "__main__":
    run()