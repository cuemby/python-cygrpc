from cygrpc.gateway.middleware.base import BasePosMiddleware


class MongoErrorsMiddleware(BasePosMiddleware):
    def on_success(self, request: dict, response: dict, header: dict) -> None:
        pass

    def on_error(self, request: dict, response: dict, header: dict, error: dict) -> None:
        pass
