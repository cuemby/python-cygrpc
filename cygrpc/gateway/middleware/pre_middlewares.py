from cygrpc.gateway.middleware.base import BasePreMiddleware


class CygrpcAuthMiddleware(BasePreMiddleware):

    def __init__(self, function):
        self.function = function

    def process(self, request: dict, header: dict) -> None:
        self.function(request=request, header=header)
