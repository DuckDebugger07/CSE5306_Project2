import os
import sqlite3
import grpc
from concurrent import futures

import drone_pb2
import drone_pb2_grpc

UPDT = "update:50054"

class Query(drone_pb2_grpc.QueryServicer):
    def __init__ (self):
        super().__init__()
        
        self.db_path = "/data/data.db"
        
        self.update_channel = grpc.insecure_channel(UPDT)
        self.update_stub = drone_pb2_grpc.UpdateStub(self.update_channel)
        
        self.init_db()
    
    def init_db (self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensors (
                id          INTEGER     PRIMARY KEY     AUTOINCREMENT,
                name        TEXT        UNIQUE          NOT NULL,
                altitude    REAL,
                voltage     REAL,
                egt         REAL,
                latitude    REAL,
                vibration   REAL
            )
        """)
        conn.commit()
        conn.close()
    
    def add_drone(self, drone_name):        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO sensors (name) VALUES (?)", (drone_name.upper()))
        
        conn.commit()
        conn.close()
        
        return f"Added {drone_name}!"
    
    def view_drone(self, drone_name):
        cols = ["Name", "Altitude", "Voltage", "EGT", "Latitude", "Vibration"]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if drone_name == "ALL":
            cursor.execute("SELECT * FROM sensors")
            data = cursor.fetchall()
            
            if len(data) == 0:
                ret = "No drones in database!"
            
            else:
                # Table Header
                ret = " | ".join([c.center(9).upper() for c in cols])
                ret += '\n' + '-' * 69 + '\n'
                # breakpoint()
                # Table Data
                for record in data:
                    ret += " | ".join(
                        [
                            f"{item:3.5f}".center(9) if isinstance(item, float) else
                            f"{item}".center(9)
                            for item in record[1:]
                        ]
                    )
                    ret += "\n"
        
        else:
            cursor.execute("SELECT * FROM sensors WHERE name = ?", (drone_name))
            data = cursor.fetchall()
            
            if len(data) == 1:
                data = data[0]
                ret = f"Name: {data[1]}"
                
                for idx, metric in enumerate(cols[1:]):
                    ret += f"\n   -{metric.center(10)} : {data[idx + 2]}"
            
            else:
                ret = "Drone not in database!"
        
        conn.commit()
        conn.close()
        
        return ret
    
    def update_data(self, drone_name):
        failures = []
        
        for ack in self.update_stub.UpdateSensors(drone_pb2.ClientQuery(request=drone_name)):
            if not ack.ok:
                failures.append(ack.reason)
        
        if failures:
            reply = "ERRORS:\n"
            for fail in failures:
                reply += f"   -{fail}\n"
        
        else:
            reply = "Updated Successfully!"
        
        return reply
        
    def CheckRunning(self, unknown, context):
        return drone_pb2.Ack(ok=True, reason="")
    
    def SendQuery(self, query, context):
        print(query.request.upper())
        
        if query.request.upper() == "QUIT":
            return drone_pb2.ServerReply(reply="Quitting...")
        
        query_parts = query.request.split(" ")
        
        if len(query_parts) == 1:
            query_parts.append("ALL")
        
        # Format Drone Name
        query_parts[1] = query_parts[1].upper()
        query_parts[1] = query_parts[1][:10]
        
        if query_parts[0].upper() == "ADD":
            reply = self.add_drone(query_parts[1])
        
        elif query_parts[0].upper() == "VIEW":
            reply = self.view_drone(query_parts[1])
        
        elif query_parts[0].upper() == "UPDATE":
            reply = self.update_data(query_parts[1])
        
        else:
            reply = f"Unknown Request: {query_parts[0].upper()}"
        
        return drone_pb2.ServerReply(reply=reply)

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