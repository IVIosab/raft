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
        self.timer = Timer(10, self.start)
        self.threads = []
        self.votes = []
        self.commitIndex = 0
        self.lastApplied = 0 
        self.database = {}
        self.log = []
        self.nextIndex = []
        self.matchIndex = []
        self.start()
    
    def start(self):
        self.set_timeout()
        self.follower_declaration()

    def set_timeout(self):
        if self.sleep:
            return
        self.timeout = random.uniform(0.150,0.300)

    def restart_timer(self, time, func):
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
        print(f'Voted for node {self.id}')
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
        self.nextIndex = [(len(self.log)+1) for i in SERVERS_INFO]
        self.matchIndex = [0 for i in SERVERS_INFO]  
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
        self.restart_timer(self.timeout, self.leader_check)
        
    def leader_check(self):
        if self.sleep or self.state!="L":
            return
        for t in self.threads:
            t.join(0)

        self.nextIndex[ID] = len(self.log)+1
        self.matchIndex[ID] = len(self.log)

        commits = 0
        for element in self.matchIndex:
            if element >= self.commitIndex+1:
                commits += 1
        
        if commits > int(len(self.matchIndex)//2):
            self.commitIndex += 1
        while self.commitIndex>self.lastApplied:
            key, value = self.log[self.lastApplied]["update"]["key"], self.log[self.lastApplied]["update"]["value"]
            self.database[key] = value
            self.lastApplied+=1
            
        self.leader_action()
        
        
    def request(self, id, address):  
        if self.sleep or self.state != "C":
            return
        
        channel = grpc.insecure_channel(address)
        stub = pb2_grpc.ServiceStub(channel)
        message = pb2.RequestTermIdMessage(term=int(self.term), id=int(self.id), last_log_index=len(self.log), last_log_term=(0 if len(self.log)==0 else self.log[-1]["term"]))
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

        entries = []
        if self.nextIndex[id]<=len(self.log):
            entries = [self.log[self.nextIndex[id]-1]]
        
        prev_log_term = 0
        if self.nextIndex[id] > 1:
            prev_log_term = self.log[self.nextIndex[id]-2]["term"]

        message = pb2.AppendTermIdMessage(term=int(self.term), id=int(self.id), prev_log_index=self.nextIndex[id]-1, prev_log_term=prev_log_term, entries=entries, leader_commit=self.commitIndex)
        
        try: 
            response = stub.AppendEntries(message)
            reciever_term = response.term
            reciever_result = response.result
            if reciever_term > self.term:
                self.update_term(reciever_term)
                self.set_timeout()
                self.follower_declaration()
            else:
                if reciever_result:
                    if len(entries) != 0:
                        self.matchIndex[id] = self.nextIndex[id]
                        self.nextIndex[id] += 1
                else:
                    self.nextIndex[id] -= 1
                    self.matchIndex[id] = min(self.matchIndex[id], (self.nextIndex[id]-1))
        except grpc.RpcError:
            return

    def gotosleep(self, period):
        self.sleep = True
        self.restart_timer(int(period), self.wakeup)
    
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
        if self.sleep:
            context.set_details("Server suspended")
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            return pb2.TermResultMessage()
        reply = {"term": -1, "result": False}
        
        if request.term == self.term:  # In the same term as me, we both are or were candidates
            if self.voted or request.last_log_index < len(self.log) or self.state != "F":
                reply = {"term": int(self.term), "result": False}
            elif request.last_log_index == len(self.log):
                if self.log[request.last_log_index-1]["term"] != request.last_log_term:
                    reply = {"term": int(self.term), "result": False}
            else:
                self.voted = True
                self.leaderid = request.id
                print(f'Voted for node {request.id}')
                reply = {"term": int(self.term), "result": True}    

            if self.state == "F":
                self.restart_timer(self.timeout, self.follower_action)
        
        elif request.term > self.term:  # I am in an earlier term
            self.update_term(request.term)
            print(f'Voted for node {request.id}')
            self.leaderid = request.id 
            self.voted = True 
            self.follower_declaration()
            reply = {"term": int(self.term), "result": True}
        
        else:  # Candidate is in an earlier term
            reply = {"term": int(self.term), "result": False}
            if self.state == "F":
                self.restart_timer(self.timeout, self.follower_action)    
                     
        return pb2.TermResultMessage(**reply)

    def AppendEntries(self, request, context):
        if self.sleep:
            context.set_details("Server suspended")
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            return pb2.TermResultMessage()
        reply = {"term": -1, "result": False}
        
        if request.term >= self.term:
            if request.term > self.term:
                self.update_term(request.term)
                self.follower_declaration
                self.leaderid = request.id
                
            if len(self.log) < request.prev_log_index:
                reply = {"term": int(self.term), "result": False}
                if self.state == "F":
                    self.restart_timer(self.timeout, self.follower_action)    
            
            else:
                if len(self.log) > request.prev_log_index:
                    self.log = self.log[:request.prev_log_index]
                
                if len(request.entries) != 0 :
                    self.log.append({"term": request.entries[0].term, "update": {"command": request.entries[0].update.command, "key": request.entries[0].update.key, "value": request.entries[0].update.value}})
                
                if request.leader_commit > self.commitIndex:
                    self.commitIndex = min(request.leader_commit, len(self.log))
                    while self.commitIndex > self.lastApplied:
                        key, value = self.log[self.lastApplied]["update"]["key"], self.log[self.lastApplied]["update"]["value"]
                        self.database[key] = value
                        self.lastApplied+=1
                            
                reply = {"term": int(self.term), "result": True}    
                self.restart_timer(self.timeout, self.follower_action)
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
        self.gotosleep(period)
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
            print(f'{int(self.leaderid)} {SERVERS_INFO[self.leaderid]}')
        else:  # I do not have a leader
            reply = {}
            
        return pb2.LeaderMessage(**reply)

    def SetVal(self, request, context):
        if self.sleep:
            context.set_details("Server suspended")
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            return pb2.SuccessMessage
        reply = {"success": False}
        
        if self.state == "L":
            self.log.append({"term": self.term, "update": {"command": 'set', "key": request.key, "value": request.value}})
            reply = {"success": True}
        elif self.state == "F":
            channel = grpc.insecure_channel(f'{SERVERS_INFO[self.leaderid]}')
            stub = pb2_grpc.ServiceStub(channel)
            message = pb2.KeyValMessage(key=request.key, value=request.value)
            try:
                response = stub.SetVal(message)
                reply = {"success": response.success}
            except grpc.RpcError:
                print("Server is not avaliable")
        return pb2.SuccessMessage(**reply)


    def GetVal(self, request, context):
        if self.sleep:
            context.set_details("Server suspended")
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            return pb2.SuccessValMessage
        reply = {"success": False, "value": "None"}
        if request.key in self.database:
            reply = {"success": True, "value": self.database[request.key]}
        return pb2.SuccessValMessage(**reply)


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