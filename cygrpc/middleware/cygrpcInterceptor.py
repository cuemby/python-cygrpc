from abc import ABC, abstractmethod

import grpc


def _unary_unary_rpc_terminator(code, details):
    def terminate(ignored_request, context):
        context.abort(code, details)

    return grpc.unary_unary_rpc_method_handler(terminate)


class CyGrpcInterceptor(ABC, grpc.ServerInterceptor):

    @classmethod
    def get_metadata_value(cls, context, key_name: str):
        for item in context.invocation_metadata:
            if item.key == key_name:
                return item.value
        return None

    @classmethod
    def get_service_name(cls, handler_call_details):
        return handler_call_details[0].split("/")[1]

    @classmethod
    def get_method_name(cls, handler_call_details):
        return handler_call_details[0].split("/")[-1]

    @abstractmethod
    def intercept_service(self, continuation, handler_call_details):
        pass

    @classmethod
    def terminator(cls, code, details):
        return _unary_unary_rpc_terminator(code, details)
