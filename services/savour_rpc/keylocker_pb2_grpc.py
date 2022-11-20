# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from services.savour_rpc import keylocker_pb2 as savourrpc_dot_keylocker__pb2


class LeyLockerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.getSupportChain = channel.unary_unary(
                '/savourrpc.keylocker.LeyLockerService/getSupportChain',
                request_serializer=savourrpc_dot_keylocker__pb2.SupportChainReq.SerializeToString,
                response_deserializer=savourrpc_dot_keylocker__pb2.SupportChainRep.FromString,
                )
        self.setSocialKey = channel.unary_unary(
                '/savourrpc.keylocker.LeyLockerService/setSocialKey',
                request_serializer=savourrpc_dot_keylocker__pb2.SetSocialKeyReq.SerializeToString,
                response_deserializer=savourrpc_dot_keylocker__pb2.SetSocialKeyRep.FromString,
                )
        self.getSocialKey = channel.unary_unary(
                '/savourrpc.keylocker.LeyLockerService/getSocialKey',
                request_serializer=savourrpc_dot_keylocker__pb2.GetSocialKeyReq.SerializeToString,
                response_deserializer=savourrpc_dot_keylocker__pb2.GetSocialKeyRep.FromString,
                )


class LeyLockerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def getSupportChain(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def setSocialKey(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getSocialKey(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LeyLockerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'getSupportChain': grpc.unary_unary_rpc_method_handler(
                    servicer.getSupportChain,
                    request_deserializer=savourrpc_dot_keylocker__pb2.SupportChainReq.FromString,
                    response_serializer=savourrpc_dot_keylocker__pb2.SupportChainRep.SerializeToString,
            ),
            'setSocialKey': grpc.unary_unary_rpc_method_handler(
                    servicer.setSocialKey,
                    request_deserializer=savourrpc_dot_keylocker__pb2.SetSocialKeyReq.FromString,
                    response_serializer=savourrpc_dot_keylocker__pb2.SetSocialKeyRep.SerializeToString,
            ),
            'getSocialKey': grpc.unary_unary_rpc_method_handler(
                    servicer.getSocialKey,
                    request_deserializer=savourrpc_dot_keylocker__pb2.GetSocialKeyReq.FromString,
                    response_serializer=savourrpc_dot_keylocker__pb2.GetSocialKeyRep.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'savourrpc.keylocker.LeyLockerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class LeyLockerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def getSupportChain(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/savourrpc.keylocker.LeyLockerService/getSupportChain',
            savourrpc_dot_keylocker__pb2.SupportChainReq.SerializeToString,
            savourrpc_dot_keylocker__pb2.SupportChainRep.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def setSocialKey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/savourrpc.keylocker.LeyLockerService/setSocialKey',
            savourrpc_dot_keylocker__pb2.SetSocialKeyReq.SerializeToString,
            savourrpc_dot_keylocker__pb2.SetSocialKeyRep.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getSocialKey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/savourrpc.keylocker.LeyLockerService/getSocialKey',
            savourrpc_dot_keylocker__pb2.GetSocialKeyReq.SerializeToString,
            savourrpc_dot_keylocker__pb2.GetSocialKeyRep.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
