import sys
import grpc
import raft_pb2 as pb2
import raft_pb2_grpc as pb2_grpc

SERVER_ADDRESS = -1
SERVER_PORT = -1


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
            print(f'Nothing\n')
    except grpc.RpcError:
        print("Server is not avaliable\n")


def suspend(period):
    channel = grpc.insecure_channel(f'{SERVER_ADDRESS}:{SERVER_PORT}')
    stub = pb2_grpc.ServiceStub(channel)
    message = pb2.PeriodMessage(period=period)

    try:
        _ = stub.Suspend(message)
    except grpc.RpcError:
        print("Server is not avaliable\n")


def getVal(key):
    channel = grpc.insecure_channel(f'{SERVER_ADDRESS}:{SERVER_PORT}')
    stub = pb2_grpc.ServiceStub(channel)
    message = pb2.KeyMessage(key=key)

    try:
        response = stub.GetVal(message)
        print(response.value)
    except grpc.RpcError:
        print("Server is not avaliable\n")


def setVal(key, value):
    channel = grpc.insecure_channel(f'{SERVER_ADDRESS}:{SERVER_PORT}')
    stub = pb2_grpc.ServiceStub(channel)
    message = pb2.KeyValMessage(key=key, value=value)

    try:
        response = stub.SetVal(message)
        if response.success:
            pass
        else:
            print("Something went wrong, try again later\n")
    except grpc.RpcError:
        print("Server is not available\n")


def check(intended_args, recieved_args):
    if recieved_args < intended_args:
        print("Not enouch arguments\n")
        return True
    elif recieved_args > intended_args:
        print("Too many arguments\n")
        return True
    return False


def quit():
    print("Client Terminated\n")
    sys.exit()


def client():
    print("Client Started\n")
    while True:
        try:
            input_buffer = input("> ")
            if len(input_buffer) <= 1:  # User entered an empty line
                continue

            command = input_buffer.split()[0]  # command type
            command_args = input_buffer.split()[1:]  # command arguments

            if command == "connect":
                if check(2, len(command_args)):
                    continue
                connect(str(command_args[0]), str(command_args[1]))
            elif command == "getleader":
                if check(0, len(command_args)):
                    continue
                get_leader()
            elif command == "suspend":
                if check(1, len(command_args)):
                    continue
                suspend(int(command_args[0]))
            elif command == "getval":
                if check(1, len(command_args)):
                    continue
                getVal(command_args[0])
            elif command == "setval":
                if check(2, len(command_args)):
                    continue
                setVal(command_args[0], command_args[1])
            elif command == "quit":
                if check(0, len(command_args)):
                    continue
                quit()
            else:
                print(f'command: {command}, is not supported\n')
        except KeyboardInterrupt:
            return


if __name__ == "__main__":
    client()
