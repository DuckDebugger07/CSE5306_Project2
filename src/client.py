import grpc

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
        
        with grpc.insecure_channel(SERVER_ADDR) as channel:
            stub = drone_pb2_grpc.QueryStub(channel)
            response = stub.SendQuery(drone_pb2.ClientQuery(request=usr_query))
        
        print(f"\n{'=' * 20}")
        print(response.reply)
        print(f"{'=' * 20}\n")


if __name__ == "__main__":
    run()


# client queries server
# server processes queries to database
#   ADD drone A
#   VIEW drone A
#      if empty, call update
#      update calls aggregation
#      aggregation calls sensors || sensors call aggregation with data
#      aggregation calls analyze
#      analyze sends Succeed (no errors) or Fail (yes errors) with msg to aggregation
#      if aggregation gets Fail from analyze, send err msg to update
#      else send sensor data to update
#      update updates database
#      update sends ack to database
#      server queries database and sends results to client


# SIMPLIFIED WITHOUT STORAGE
# server calls update
# update calls aggregation (DONE)
# aggregation calls all sensors (DONE)
#    sensors respond to aggregation (DONE)
#    aggregation sends sensor info to analysis (TODO)
#    analysis checks sensor info and respond (SEMI-DONE)
# aggregation sends results to update (TODO)
# update prints results (TODO)