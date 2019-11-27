from typing import Any


def rest(url: str, method="GET", pre_request=None, pos_request=None) -> Any:
    """
    Decorator for add route to http rest interface
    :param pos_request: array of Middleware's that implement BasePosMiddleware class
    :param pre_request: array of Middleware's that implement BasePreMiddleware class
    :param url: Route url. example. /api/v1/service/method
    :param method: http method. GET, POST, DELETE, PUT ...
    :return: None
    """
    from cygrpc.gateway.proxy.router import Router as _Router
    from cygrpc.gateway.proxy.middleware import MiddlewareManager as _MiddlewareManager

    def inner(func):
        """
        Inject route definition to Router
        :param func:
        :return:
        """

        service = func.__qualname__.split(".")[0]
        _Router().add_route(
            service=service,
            grpc_method=func.__name__,
            url_path=url,
            http_method=method
        )
        if pre_request is not None and len(pre_request) > 0:
            _MiddlewareManager().add_route_pre_middleware(pre_request, url)
        if pos_request is not None and len(pos_request) > 0:
            _MiddlewareManager().add_route_pre_middleware(pos_request, url)
        return func

    return inner
