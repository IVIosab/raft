import sys
import time
from threading import Thread

import grpc
import raft_pb2 as pb2
import raft_pb2_grpc as pb2_grpc
from concurrent import futures
import random

DEBUG_MODE = True

ID = sys.argv[1]
SERVERS_INFO = {}
SERVERS_STATUS = {}
TIMER = random.uniform(0.150, 0.300)
TERM = 0
LEADER = -1
VOTED_FOR = -1


class Handler(pb2_grpc.ServiceServicer):
    def __init__(self, *args, **kwargs):
        pass

    def RequestVote(self, request, context):
        global LEADER, VOTED_FOR, TERM

        if DEBUG_MODE:
            print("Entered RequsetVote")

        # Request input
        candidate_term = request.term
        candidate_id = request.candidateId

        # Initialize reply
        reply = {"term": -1, "result": False}

        # Conditions
        if candidate_term == TERM:  # In the same term as me, we both are or were candidates
            # Leader is dead since we are in an election
            LEADER = -1

            if VOTED_FOR == -1:  # Did not vote
                # Vote for the requester
                VOTED_FOR = candidate_id
                reply = {"term": TERM, "result": True}
            else:  # Already voted
                # Return false to show that i can't vote for the requester
                reply = {"term": TERM, "result": False}
        elif candidate_term > TERM:  # I am in an earlier term
            # Leader is dead since I am in an early term
            LEADER = -1

            # Update my term
            TERM = candidate_term

            if VOTED_FOR == -1:  # Did not vote
                # Vote for the requester
                VOTED_FOR = candidate_id
                reply = {"term": TERM, "result": True}
            else:  # Already voted
                # Return false to show that i can't vote for the requester
                reply = {"term": TERM, "result": False}
        else:  # Candidate is in an earlier term
            # Return false and my term to show Candidate that he is in an earlier term
            reply = {"term": TERM, "result": False}
        return pb2.TermResultMessage(**reply)

    def AppendEntries(self, request, context):
        global LEADER, VOTED_FOR

        if DEBUG_MODE:
            print("Entered AppendEntries")

        # Request input
        leader_term = request.term
        leader_id = request.leaderId

        # Initialize reply
        reply = {"term": -1, "result": False}

        # Conditions
        if leader_term >= TERM:  # Requester is in the same or an upcoming term
            # Requester is the Leader, and remove my vote since there is no election
            LEADER = leader_id
            VOTED_FOR = -1
            reply = {"term": TERM, "result": True}
        else:  # Requester is in an earlier term
            # Return false and my term to show requester that they are in an earlier term
            reply = {"term": TERM, "result": False}
        return pb2.TermResultMessage(**reply)

    def Suspend(self, request, context):
        if DEBUG_MODE:
            print("Entered Suspend")

        # Request input
        period = request.period

        # Make the server sleep for {period} seconds
        time.sleep(period)
        print(f'Sleeping for {period} seconds')

        # Return an empty reply
        reply = {}
        return pb2.EmptyMessage(**reply)

    def GetLeader(self, requset, context):
        if DEBUG_MODE:
            print("Entered GetLeader")

        # Initialize reply
        reply = {"leader": -1, "address": ""}

        # Conditions
        if LEADER != -1:  # I have a leader
            # Return the leader
            reply = {"leader": LEADER, "address": SERVERS_INFO[LEADER]}
        else:  # I do not have a leader
            if VOTED_FOR != -1:  # I already voted
                # Return who i voted for
                reply = {"leader": VOTED_FOR, "address": SERVERS_INFO[VOTED_FOR]}
            else:  # I Did not vote
                # Return nothing
                reply = {}
                return pb2.EmptyMessage(**reply)
        return pb2.LeaderMessage(**reply)


# These functions are not calling the RPC methods right?
def heartbeat(id, address, port):
    x = 0


def request(id, address, port):
    x = 0
# worker function for candidate threads


def leader():
    threads = []
    for k, v in SERVERS_INFO:
        # will send vote to ourselves as well
        threads.append(Thread(target=heartbeat, args=(k, v[0], v[1])))

    for t in threads:
        t.start()


def candidate():
    threads = []
    for k, v in SERVERS_INFO:
        # will request vote from ourselves
        threads.append(Thread(target=request, args=(k, v[0], v[1])))

    for t in threads:
        t.start()
    # Send request vote to each server with threads


# Isn't the server a server and a client ?
def server():
    if DEBUG_MODE:
        print("Entered Server")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    pb2_grpc.add_ServiceServicer_to_server(Handler(), server)
    server.add_insecure_port(f'{SERVERS_INFO[ID][0]}:{SERVERS_INFO[ID][1]}')
    server.start()

    while True:
        try:
            if LEADER == ID:
                x = server.wait_for_termination(0.051)
                if x:
                    leader()
            else:
                # Shouldn't we have here a stub to wait for append_entry_Request from the leader
                # and a timeout for the response which is the difference betweeb our time out and 50? like request a heart beat?
                x = server.wait_for_termination(1)
                if x:
                    candidate()

        except grpc.RpcError:
            print("Unexpected Error")
            sys.exit()
        except KeyboardInterrupt:
            print("Shutting Down")
            sys.exit()


def configuration():
    with open('Config.conf') as f:
        global SERVERS_INFO
        lines = f.readlines()
        for line in lines:
            parts = line.split()
            id, address, port = parts[0], parts[1], parts[2]
            SERVERS_INFO[id] = (address, port)


if __name__ == "__main__":
    if DEBUG_MODE:
        print("Hello There!")
    configuration()
    server()
