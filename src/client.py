import grpc
import drone_pb2
import drone_pb2_grpc

SERVER = "server:50053"


def main():
    ch = grpc.insecure_channel(SERVER)
    stub = drone_pb2_grpc.ServerStub(ch)

    print("Client ready. Type help.")

    while True:
        cmd = input("> ")
        reply = stub.SendCommand(drone_pb2.Command(text=cmd))
        print(reply.text)

        if cmd.strip().lower() == "quit":
            break


if __name__ == "__main__":
    main()