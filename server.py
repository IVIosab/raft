import sys
import time
import grpc
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
    
    def request_vote(self, request, context):
        canditate_term = request.term
        canditate_id = request.id
        if canditate_term == TERM:
            if not VOTED:
                #return (my_term, true)
            else:
                #return (my_term, false)
        elif canditate_term > TERM:
            global TERM
            TERM = canditate_term
            #return(my_term, false)
        else: 
            #return(my_term, false)

    def append_entries(self, request, context):
        leader_term = request.term
        leader_id = request.id
        if leader_term >= TERM:
            #return(my_term, true)
        else:
            #return(my_term, false)
        
    def suspend(self, request, context):
        period = request.period
        time.sleep(period)

    def get_leader(self, requset, context):
        if LEADER != -1:
            #return LEADER
        else:
            if VOTED_FOR != -1:
                #return VOTED_FOR
            else 
                #return nothing

def server():


if __name__ == "__main__":
    print("hello there")