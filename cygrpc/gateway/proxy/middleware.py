import inspect
from typing import List

from cygrpc.gateway.middleware import base


class MiddlewareManager:
    __SINGLE_INSTANCE = None

    def __new__(cls, *args, **kwargs):
        if cls.__SINGLE_INSTANCE is not None:
            return cls.__SINGLE_INSTANCE
        else:
            cls.__SINGLE_INSTANCE = cls.__MiddlewareManager()
            return cls.__SINGLE_INSTANCE

    class __MiddlewareManager:

        def __init__(self):
            self.global_pre_middleware: List[base.BasePreMiddleware] = list()
            self.global_pos_middleware: List[base.BasePosMiddleware] = list()
            self.routes_middleware = {}

        def add_pre_middleware(self, middlewares):
            middleware_list = middlewares
            if not isinstance(middlewares, list):
                middleware_list = [middlewares]
            for middleware_class in middleware_list:
                middleware = middleware_class() if inspect.isclass(middleware_class) else middleware_class
                if isinstance(middleware, base.BasePreMiddleware):
                    self.global_pre_middleware.append(middleware)
                else:
                    raise NotImplementedError(
                        "middleware not implement cygrc.gateway.middleware.base.BasePreMiddleware abstract class")

        def add_pos_middleware(self, middlewares):
            middleware_list = middlewares
            if not isinstance(middlewares, list):
                middleware_list = [middlewares]
            for middleware_class in middleware_list:
                middleware = middleware_class() if inspect.isclass(middleware_class) else middleware_class
                if isinstance(middleware, base.BasePosMiddleware):
                    self.global_pos_middleware.append(middleware)
                else:
                    raise NotImplementedError(
                        "middleware not implement cygrc.gateway.middleware.base.BasePosMiddleware abstract class"
                    )

        def add_route_pre_middleware(self, middleware_class, route: str):
            middleware = middleware_class() if inspect.isclass(middleware_class) else middleware_class
            if isinstance(middleware, base.BasePreMiddleware):
                if route in self.routes_middleware:
                    self.routes_middleware[route]["pre_middleware"].append(middleware)
                else:
                    self.routes_middleware[route] = {"pre_middleware": [], "pos_middleware": []}
                    self.routes_middleware[route]["pre_middleware"].append(middleware)
            else:
                raise NotImplementedError(
                    "middleware not implement cygrc.gateway.middleware.base.BasePreMiddleware abstract class"
                )

        def add_route_pos_middleware(self, middleware_class, route: str):
            middleware = middleware_class() if inspect.isclass(middleware_class) else middleware_class
            if isinstance(middleware, base.BasePosMiddleware):
                if route in self.routes_middleware:
                    self.routes_middleware[route]["pos_middleware"].append(middleware)
                else:
                    self.routes_middleware[route] = {"pre_middleware": [], "pos_middleware": []}
                    self.routes_middleware[route]["pos_middleware"].append(middleware)
            else:
                raise NotImplementedError(
                    "middleware not implement cygrc.gateway.middleware.base.BasePosMiddleware abstract class"
                )
