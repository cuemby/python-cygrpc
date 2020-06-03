from cygrpc.gateway.middleware.base import BasePreMiddleware


class CygrpcAuthMiddleware(BasePreMiddleware):

    def __init__(self, function):
        self.function = function

    def process(self, route: dict, request: dict, header: dict) -> None:
        self.function(route, request, header)
