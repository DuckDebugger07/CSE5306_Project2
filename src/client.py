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
#   ADD drone A (DONE)
#   VIEW drone A (DONE)
#      show specific or all drone date (DONE)
#      if seeing specific drone and has None in value, then call update (DONE)
#         Update updates database (TODO)
#            If sensor gives error, put None (TODO)
#            Else put sensor data
#      Server will get Ack from Update and read db
#   UPDATE drone A (TODO)
#      Update specific drone with new values
#      Server will get Ack from Update and read db


# SIMPLIFIED WITHOUT STORAGE
# server calls update
# update calls aggregation (DONE)
# aggregation calls all sensors (DONE)
#    sensors respond to aggregation (DONE)
#    aggregation sends sensor info to analysis (TODO)
#    analysis checks sensor info and respond (SEMI-DONE)
# aggregation sends results to update (TODO)
# update prints results (TODO)