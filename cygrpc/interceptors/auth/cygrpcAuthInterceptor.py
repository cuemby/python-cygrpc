from abc import abstractmethod

import grpc

from cygrpc.middleware import CyGrpcInterceptor


class CyGrpcAuthInterceptor(CyGrpcInterceptor):
    @abstractmethod
    def auth_process(self, continuation, handler_call_details) -> bool:
        pass

    def intercept_service(self, continuation, handler_call_details):
        print("service: ", self.get_service_name(handler_call_details))
        print("method: ", self.get_method_name(handler_call_details))
        result = self.auth_process(continuation, handler_call_details)
        if result:
            return self.on_success(continuation, handler_call_details)
        else:
            return self.on_failed(grpc.StatusCode.UNAUTHENTICATED, "Validate authentication failed.")
