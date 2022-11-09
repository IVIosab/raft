import sys
import time
import grpc
import raft_pb2 as pb2
import raft_pb2_grpc as pb2_grpc
import random

DEBUG_MODE = True

ID = sys.argv[1]
SERVERS_INFO = {}
SERVERS_STATUS = {}
TIMER = random.randint(150,300)
TERM = 0
LEADER = -1
VOTED_FOR = -1

class Handler(pb2_grpc.ServiceServicer):
    def __init__(self, *args, **kwargs):
        pass  
    
    def RequestVote(self, request, context):
        candidate_term = request.term
        candidate_id = request.candidateid
        reply = {"term": -1, "result": False}
        if candidate_term == TERM:
            if VOTED_FOR != -1:
                reply = {"term": TERM, "result": True}
            else:
                reply = {"term": TERM, "result": False}
        elif candidate_term > TERM:
            global TERM
            TERM = candidate_term
            reply = {"term": TERM, "result": False}
        else: 
            reply = {"term": TERM, "result": False}
        return pb2.TermResultMessage(**reply)

    def AppendEntries(self, request, context):
        leader_term = request.term
        leader_id = request.leaderid
        reply = {"term": -1, "result": False}
        if leader_term >= TERM:
            reply = {"term": TERM, "result": True}
        else:
            reply = {"term": TERM, "result": False}
        return pb2.TermResultMessage(**reply)
        
    def Suspend(self, request, context):
        period = request.period
        time.sleep(period)
        reply = {}
        return pb2.EmptyMessage(**reply)

    def GetLeader(self, requset, context):
        reply = {"leader": -1}
        if LEADER != -1:
            reply = {"leader": LEADER}
        else:
            if VOTED_FOR != -1:
                reply = {"leader": VOTED_FOR}
            else: 
                reply = {"leader": -1} # TODO: Should return nothing not -1
        return pb2.LeaderMessage(**reply)

def server():
    print("hello there")
    channel = grpc.insecure_channel()
    stub = pb2_grpc.ServiceStub(channel)


if __name__ == "__main__":
    server()