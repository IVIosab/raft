import sys
import grpc
import raft_pb2 as pb2
import raft_pb2_grpc as pb2_grpc

SERVER_ADDRESS = -1
SERVER_PORT = -1


# "... You only specify the address of the node you will later connect to (using getleader/suspend commands). You should check availability of the given address only on getleader/suspend invocation." -Alexey Stepanov
def connect(address, port):
    global SERVER_ADDRESS, SERVER_PORT
    SERVER_ADDRESS = address
    SERVER_PORT = port

def get_leader():
    channel = grpc.insecure_channel(f'{SERVER_ADDRESS}:{SERVER_PORT}')
    stub = pb2_grpc.ServiceStub(channel)
    message = pb2.EmptyMessage()
    
    try:
        response = stub.GetLeader(message)
        if response:
            leader = response.leader
            leader_address = response.address
            print(f'{leader} {leader_address}')
        else:
            print(f'Nothing')
    except grpc.RpcError:
        print("Server is not avaliable")

def suspend(period):
    channel = grpc.insecure_channel(f'{SERVER_ADDRESS}:{SERVER_PORT}')
    stub = pb2_grpc.ServiceStub(channel)
    message = pb2.PeriodMessage(period=period)
    
    try:
        response = stub.Suspend(message)
    except grpc.RpcError:
        print("Server is not avaliable")

def getVal(key):
    channel = grpc.insecure_channel(f'{SERVER_ADDRESS}:{SERVER_PORT}')
    stub = pb2_grpc.ServiceStub(channel)
    message = pb2.KeyMessage(key=key)
    
    try:
        response = stub.GetVal(message)
        if response.success:
            print(response.value)
        else:
            print("Something went wrong")
    except grpc.RpcError:
        print("Server is not avaliable")

def setVal(key, value):
    channel = grpc.insecure_channel(f'{SERVER_ADDRESS}:{SERVER_PORT}')
    stub = pb2_grpc.ServiceStub(channel)
    message = pb2.KeyValMessage(key=key, value=value)
    
    try:
        response = stub.SetVal(message)
        if response.success:
            print("Success")
        else:
            print("Something went wrong")
    except grpc.RpcError:
        print("Server is not available")

def quit():
    print("The client ends")
    sys.exit()

def client():
    print("The client starts")
    while True:
        try:
            input_buffer = input("> ")
            if len(input_buffer) <= 1:  # User entered an empty line
                continue

            command = input_buffer.split()[0]  # command type
            command_args = input_buffer.split()[1:]  # command arguments

            if command == "connect":
                connect(str(command_args[0]), str(command_args[1]))
            elif command == "getleader":
                get_leader()
            elif command == "suspend":
                suspend(int(command_args[0]))
            elif command == "quit":
                quit()
            elif command == "getval":
                getVal(command_args[0])
            elif command == "setval":
                setVal(command_args[0], command_args[1])
            else:
                print(f'command: {command}, is not supported')
        except KeyboardInterrupt:
            sys.exit()

if __name__ == "__main__":
    client()