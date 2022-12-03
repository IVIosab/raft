# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import raft_pb2 as raft__pb2


class ServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RequestVote = channel.unary_unary(
                '/Service/RequestVote',
                request_serializer=raft__pb2.TermIdMessage.SerializeToString,
                response_deserializer=raft__pb2.TermResultMessage.FromString,
                )
        self.AppendEntries = channel.unary_unary(
                '/Service/AppendEntries',
                request_serializer=raft__pb2.TermIdMessage.SerializeToString,
                response_deserializer=raft__pb2.TermResultMessage.FromString,
                )
        self.Suspend = channel.unary_unary(
                '/Service/Suspend',
                request_serializer=raft__pb2.PeriodMessage.SerializeToString,
                response_deserializer=raft__pb2.EmptyMessage.FromString,
                )
        self.GetLeader = channel.unary_unary(
                '/Service/GetLeader',
                request_serializer=raft__pb2.EmptyMessage.SerializeToString,
                response_deserializer=raft__pb2.LeaderMessage.FromString,
                )
        self.SetVal = channel.unary_unary(
                '/Service/SetVal',
                request_serializer=raft__pb2.KeyValMessage.SerializeToString,
                response_deserializer=raft__pb2.SuccessMessage.FromString,
                )
        self.GetVal = channel.unary_unary(
                '/Service/GetVal',
                request_serializer=raft__pb2.KeyMessage.SerializeToString,
                response_deserializer=raft__pb2.SuccessValMessage.FromString,
                )


class ServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RequestVote(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AppendEntries(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Suspend(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetLeader(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetVal(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetVal(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RequestVote': grpc.unary_unary_rpc_method_handler(
                    servicer.RequestVote,
                    request_deserializer=raft__pb2.TermIdMessage.FromString,
                    response_serializer=raft__pb2.TermResultMessage.SerializeToString,
            ),
            'AppendEntries': grpc.unary_unary_rpc_method_handler(
                    servicer.AppendEntries,
                    request_deserializer=raft__pb2.TermIdMessage.FromString,
                    response_serializer=raft__pb2.TermResultMessage.SerializeToString,
            ),
            'Suspend': grpc.unary_unary_rpc_method_handler(
                    servicer.Suspend,
                    request_deserializer=raft__pb2.PeriodMessage.FromString,
                    response_serializer=raft__pb2.EmptyMessage.SerializeToString,
            ),
            'GetLeader': grpc.unary_unary_rpc_method_handler(
                    servicer.GetLeader,
                    request_deserializer=raft__pb2.EmptyMessage.FromString,
                    response_serializer=raft__pb2.LeaderMessage.SerializeToString,
            ),
            'SetVal': grpc.unary_unary_rpc_method_handler(
                    servicer.SetVal,
                    request_deserializer=raft__pb2.KeyValMessage.FromString,
                    response_serializer=raft__pb2.SuccessMessage.SerializeToString,
            ),
            'GetVal': grpc.unary_unary_rpc_method_handler(
                    servicer.GetVal,
                    request_deserializer=raft__pb2.KeyMessage.FromString,
                    response_serializer=raft__pb2.SuccessValMessage.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Service', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Service(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RequestVote(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Service/RequestVote',
            raft__pb2.TermIdMessage.SerializeToString,
            raft__pb2.TermResultMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AppendEntries(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Service/AppendEntries',
            raft__pb2.TermIdMessage.SerializeToString,
            raft__pb2.TermResultMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Suspend(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Service/Suspend',
            raft__pb2.PeriodMessage.SerializeToString,
            raft__pb2.EmptyMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetLeader(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Service/GetLeader',
            raft__pb2.EmptyMessage.SerializeToString,
            raft__pb2.LeaderMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetVal(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Service/SetVal',
            raft__pb2.KeyValMessage.SerializeToString,
            raft__pb2.SuccessMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetVal(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Service/GetVal',
            raft__pb2.KeyMessage.SerializeToString,
            raft__pb2.SuccessValMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
