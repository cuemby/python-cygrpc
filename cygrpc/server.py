import inspect as _inspect
import logging as _logging
import os
import time
from concurrent import futures

import grpc

from cygrpc.gateway.proxy.middleware import MiddlewareManager
from cygrpc.gateway.rest_gateway import HttpGateway
from cygrpc.utils import extractor as _extractor

_logging.basicConfig(
    level=os.getenv("LOGLEVEL", "INFO"),
    format='%(levelname)s | %(asctime)s - %(name)s - %(message)s')


class Server:
    """
    Create and run grpc server.
    """
    __SINGLE_INSTANCE = None

    def __new__(cls, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :keyword port
        :keyword host
        :keyword max_threads
        :keyword secure
        :keyword interceptors
        :return:
        """
        if not Server.__SINGLE_INSTANCE:
            Server.__SINGLE_INSTANCE = Server.__Server()
            Server.__SINGLE_INSTANCE._port = 50051 if "port" not in kwargs else kwargs["port"]
            Server.__SINGLE_INSTANCE._host = "0.0.0.0" if "host" not in kwargs else kwargs["host"]
            Server.__SINGLE_INSTANCE._max_threads = 10 if "max_threads" not in kwargs else kwargs["max_threads"]
            Server.__SINGLE_INSTANCE._secure = False if "secure" not in kwargs else kwargs["secure"]
            Server.__SINGLE_INSTANCE._interceptors = None if "interceptors" not in kwargs else kwargs["interceptors"]
            Server.__SINGLE_INSTANCE._rest_port = 3000 if "http_port" not in kwargs else kwargs["http_port"]
            Server.__SINGLE_INSTANCE._debug = False if "http_debug" not in kwargs else kwargs["http_debug"]
            Server.__SINGLE_INSTANCE.init()
        return Server.__SINGLE_INSTANCE

    class __Server:
        _grpc_server: grpc.Server = None
        _max_threads: int = 10
        _host: str = "0.0.0.0"
        _port: int = 50051
        _secure: bool = False
        _interceptors: tuple = ()
        _pb2_grpc = None
        _gateway = None
        _rest_port: int = 3000
        _debug: bool = False

        def get_grpc_server(self):
            return self._grpc_server

        def init(self):
            self._grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=self._max_threads),
                                            interceptors=self._interceptors)
            if not self._secure:
                self._grpc_server.add_insecure_port(f"{self._host}:{self._port}")
            return self

        def add_service(self, pb2_grpc, service, rest=False):
            """
            Add service to grpc server
            :param pb2_grpc: pb2_grpc module
            :param service: service implementation
            :param rest: enable http rest gateway for service. default False
            :return:
            """

            add_to_server = _extractor.extract_add_server(pb2_grpc)
            if _inspect.isclass(service):
                service = service()
            add_to_server(service, self._grpc_server)
            if rest:
                if self._gateway is None:
                    self._gateway: HttpGateway = HttpGateway(grpc_host=self._host, grpc_port=self._port)
                self._gateway.add_service(pb2_grpc, service)

        @staticmethod
        def add_http_pre_middleware(middleware_class):
            MiddlewareManager().add_pre_middleware(middleware_class)

        @staticmethod
        def add_http_pos_middleware(middleware_class):
            MiddlewareManager().add_pos_middleware(middleware_class)

        def start(self):
            """
            Start server
            :return:
            """
            _logging.info(f"Server start in port:  {self._port}")
            self._grpc_server.start()
            if self._gateway is not None:
                time.sleep(0.15)
                self._gateway.start(port=self._rest_port, http_debug=self._debug)
            try:
                while True and self._grpc_server is not None:
                    time.sleep(3000)
            except KeyboardInterrupt as ex:
                _logging.error("Server stop.... reason: KeyboardInterrupt")
                exit(0)

        def stop(self):
            self._grpc_server.stop(0)
            exit(0)
