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
        #Request input
        candidate_term = request.term
        candidate_id = request.candidateId
        
        #Initialize reply
        reply = {"term": -1, "result": False}
        
        #Conditions
        if candidate_term == TERM: #In the same term as me, we both are or were candidates
            #Leader is dead since we are in an election
            global LEADER
            LEADER = -1

            if VOTED_FOR == -1: #Did not vote
                #Vote for the requester
                global VOTED_FOR
                VOTED_FOR = candidate_id
                reply = {"term": TERM, "result": True}
            else: #Already voted
                #Return false to show that i can't vote for the requester
                reply = {"term": TERM, "result": False}
        elif candidate_term > TERM: #I am in an earlier term
            #Leader is dead since I am in an early term
            global LEADER
            LEADER = -1
            
            #Update my term
            global TERM
            TERM = candidate_term

            if VOTED_FOR == -1: #Did not vote
                #Vote for the requester
                global VOTED_FOR
                VOTED_FOR = candidate_id
                reply = {"term": TERM, "result": True}
            else: #Already voted 
                #Return false to show that i can't vote for the requester
                reply = {"term": TERM, "result": False}
        else: #Candidate is in an earlier term
            #Return false and my term to show Candidate that he is in an earlier term
            reply = {"term": TERM, "result": False}
        return pb2.TermResultMessage(**reply)

    def AppendEntries(self, request, context):
        #Request input
        leader_term = request.term
        leader_id = request.leaderId
        
        #Initialize reply
        reply = {"term": -1, "result": False}
        
        #Conditions
        if leader_term >= TERM: #Requester is in the same or an upcoming term
            #Requester is the Leader, and remove my vote since there is no election
            global LEADER, VOTED_FOR
            LEADER = leader_id
            VOTED_FOR = -1
            reply = {"term": TERM, "result": True}
        else: #Requester is in an earlier term
            #Return false and my term to show requester that they are in an earlier term
            reply = {"term": TERM, "result": False}
        return pb2.TermResultMessage(**reply)
        
    def Suspend(self, request, context):
        #Request input
        period = request.period
        
        #Make the server sleep for {period} seconds
        time.sleep(period)

        #Return an empty reply
        reply = {}
        return pb2.EmptyMessage(**reply)

    def GetLeader(self, requset, context):
        #Initialize reply
        reply = {"leader": -1}

        #Conditions
        if LEADER != -1: #I have a leader
            #Return the leader
            reply = {"leader": LEADER}
        else: #I do not have a leader
            if VOTED_FOR != -1: #I already voted
                #Return who i voted for 
                reply = {"leader": VOTED_FOR}
            else: #I Did not vote
                #Return nothing
                reply = {} 
                #maybe we should return here with empty message ?
        return pb2.LeaderMessage(**reply)

def server():
    print("hello there")
    channel = grpc.insecure_channel()
    stub = pb2_grpc.ServiceStub(channel)


if __name__ == "__main__":
    server()