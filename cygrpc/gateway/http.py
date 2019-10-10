from bottle import route

from cygrpc.gateway.proxy.router import Router as _Router
import importlib as _importlib


def rest(url: str, method="GET") -> None:
    """
    Decorator for add route to http rest interface
    :param url: Route url. example. /api/v1/service/method
    :param method: http method. GET, POST, DELETE, PUT ...
    :return: None
    """

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
        return func

    return inner
