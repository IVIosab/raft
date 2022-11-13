import sys
import os
from threading import Thread, Timer
from concurrent import futures
import random

import grpc
import raft_pb2 as pb2
import raft_pb2_grpc as pb2_grpc

ID = int(sys.argv[1])
SERVERS_INFO = {}

class Server:
    def __init__(self):
        self.state = "F"
        self.term = 0
        self.id = ID
        self.voted = False
        self.leaderid = -1
        self.sleep = False
        self.timeout = None
        self.timer = None
        self.threads = []
        self.votes = []
        self.start()
    
    def start(self):
        self.set_timeout()
        self.timer = Timer(self.timeout, self.follower_action)
        self.timer.start()

    def set_timeout(self):
        if self.sleep:
            return
        self.timeout = random.uniform(0.150,0.300)

    def restart_timer(self, time, func):
        if self.sleep:
            return
        self.timer.cancel()
        self.timer = Timer(time, func)
        self.timer.start()

    def update_state(self, state):
        if self.sleep:
            return
        self.state = state
    
    def update_term(self, term):
        if self.sleep:
            return
        self.voted= False
        self.term = term

    def follower_declaration(self):
        if self.sleep:
            return
        self.update_state("F")
        print(f'I am a follower. Term: {self.term}')
        self.restart_timer(self.timeout,self.follower_action)

    def follower_action(self):
        if self.sleep or self.state!="F":
            return
        print('The leader is dead')
        self.leaderid = -1
        self.candidate_declaration()
        
    def candidate_declaration(self):
        if self.sleep:
            return
        self.update_term(self.term+1)
        self.update_state("C")
        self.voted = True
        self.leaderid = self.id
        print(f'I am a candidate. Term: {self.term}')
        self.restart_timer(self.timeout, self.candidate_action)
        self.candidate_election()
    
    def candidate_election(self):
        if self.sleep or self.state!="C":
            return
        self.votes = [0 for _ in range(len(SERVERS_INFO))]
        self.threads = []
        for k, v in SERVERS_INFO.items():
            if k==ID: 
                self.votes[k]=1
                continue
            self.threads.append(Thread(target=self.request, args=(k, v))) 
        for t in self.threads:
            t.start()

    def candidate_action(self):
        if self.sleep or self.state!="C":
            return
        for t in self.threads:
            t.join(0)
        
        print("Votes recieved")

        if sum(self.votes) > (len(self.votes)//2):
            self.timeout = 0.050
            self.leader_declaration()
        else:
            self.set_timeout()
            self.follower_declaration()

    def leader_declaration(self):
        if self.sleep:
            return
        self.update_state("L")
        print(f'I am a leader, Term: {self.term}')
        self.leaderid = self.id
        self.leader_action()
        
    def leader_action(self):
        if self.sleep or self.state != "L":
            return
        self.threads = []
        for k, v in SERVERS_INFO.items():
            if k==ID:
                continue
            self.threads.append(Thread(target=self.heartbeat, args=(k, v))) 
        for t in self.threads:
            t.start()
        self.restart_timer(self.timeout, self.leader_action)
        
        
    def request(self, id, address):  
        if self.sleep or self.state != "C":
            return
        
        channel = grpc.insecure_channel(address)
        stub = pb2_grpc.ServiceStub(channel)
        message = pb2.TermIdMessage(term=int(self.term), id=int(self.id))
        try:
            response = stub.RequestVote(message)
            reciever_term = response.term
            reciever_result = response.result
            if reciever_term > self.term:
                self.update_term(reciever_term)
                self.set_timeout()
                self.follower_declaration()
            elif reciever_result:
                self.votes[id] = 1
        except grpc.RpcError:
            return

    def heartbeat(self, id, address):
        if self.sleep or (self.state != "L"):
            return
        
        channel = grpc.insecure_channel(address)
        stub = pb2_grpc.ServiceStub(channel)
        message = pb2.TermIdMessage(term=int(self.term), id=int(self.id))
        
        try: 
            response = stub.AppendEntries(message)
            reciever_term = response.term
            reciever_result = response.result
            if reciever_term > self.term:
                self.update_term(reciever_term)
                self.set_timeout()
                self.follower_declaration()
        except grpc.RpcError:
            return

    
    def wakeup(self):
        self.sleep = False
        if self.state == "L":
            self.leader_action()
        elif self.state == "C":
            self.candidate_action()
        else:
            self.follower_action()

class Handler(pb2_grpc.ServiceServicer, Server):
    def __init__(self):
        super().__init__()

    def RequestVote(self, request, context):
        print("Requesting")
        if self.sleep:
            context.set_details("Server suspended")
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            return pb2.TermResultMessage()
        candidate_term = request.term
        candidate_id = request.id
        reply = {"term": -1, "result": False}
        
        if candidate_term == self.term:  # In the same term as me, we both are or were candidates
            if self.state == "L":
                reply = {"term": int(self.term), "result": False}
            elif self.state == "C":
                reply = {"term": int(self.term), "result": False}
            elif not self.voted:
                self.voted = True
                self.leaderid = candidate_id
                reply = {"term": int(self.term), "result": True}
            else:
                reply = {"term": int(self.term), "result": False}
        elif candidate_term > self.term:  # I am in an earlier term
            self.update_state("F")
            self.update_term(candidate_term)
            self.leaderid = candidate_id 
            self.voted = True 
            reply = {"term": int(self.term), "result": True}
        else:  # Candidate is in an earlier term
            reply = {"term": int(self.term), "result": False}
        
        if reply["result"]:
            print(f'Voted for node {self.id}')         
        return pb2.TermResultMessage(**reply)

    def AppendEntries(self, request, context):
        print("Appending")
        if self.sleep:
            context.set_details("Server suspended")
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            return pb2.TermResultMessage()
        leader_term = request.term
        leader_id = request.id
        reply = {"term": -1, "result": False}
        
        if leader_term >= self.term:
            self.update_state("F")
            self.update_term(leader_term)
            self.leaderid = leader_id
            reply = {"term": int(self.term), "result": True}
        else:  # Requester is in an earlier term
            reply = {"term": int(self.term), "result": False}
        
        return pb2.TermResultMessage(**reply)

    def Suspend(self, request, context):
        if self.sleep:
            context.set_details("Server suspended")
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            return pb2.EmptyMessage()
        period = request.period
        
        print(f'Command from client: suspend {period}')
        self.sleep = True
        self.timer.cancel()
        self.timer = Timer(period, self.wakeup)
        self.timer.start()
        print(f'Sleeping for {period} seconds')
        
        reply = {}
        return pb2.EmptyMessage(**reply)

    def GetLeader(self, request, context):
        if self.sleep:
            context.set_details("Server suspended")
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            return pb2.LeaderMessage()
        reply = {"leader": -1, "address": ""}
        
        print(f'Command from client: getleader')
        
        if self.leaderid != -1:  # I have a leader
            reply = {"leader": int(self.leaderid), "address": SERVERS_INFO[self.leaderid]}
        else:  # I do not have a leader
            reply = {}
            
        return pb2.LeaderMessage(**reply)


def serve():
    print(f'The server starts at {SERVERS_INFO[ID]}')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_ServiceServicer_to_server(Handler(), server)
    server.add_insecure_port(SERVERS_INFO[ID])
    try:
        server.start()
        while True:
            server.wait_for_termination()
    except grpc.RpcError:
        print("Unexpected Error")
        os._exit(0)
    except KeyboardInterrupt:
        print("Shutting Down")
        os._exit(0)
        


def configuration():
    with open('Config.conf') as f:
        global SERVERS_INFO
        lines = f.readlines()
        for line in lines:
            parts = line.split()
            id, address, port = parts[0], parts[1], parts[2]
            SERVERS_INFO[int(id)] = (f'{str(address)}:{str(port)}')

def run():  
    configuration()
    serve()


if __name__ == "__main__":
    run()