import os
import time
from concurrent import futures

import grpc
import logging as _logging

_logging.basicConfig(
    level=os.getenv("LOGLEVEL", "INFO"),
    format='%(levelname)s | %(asctime)s - %(name)s - %(message)s')


class Server:
    __SINGLE_INSTANCE = None

    def __new__(cls, *args, **kwargs):
        if not Server.__SINGLE_INSTANCE:
            Server.__SINGLE_INSTANCE = Server.__Server()
            Server.__SINGLE_INSTANCE._port = 50051 if "port" not in kwargs else kwargs["port"]
            Server.__SINGLE_INSTANCE._host = "0.0.0.0" if "host" not in kwargs else kwargs["host"]
            Server.__SINGLE_INSTANCE._max_threads = 10 if "max_threads" not in kwargs else kwargs["max_threads"]
            Server.__SINGLE_INSTANCE._secure = False if "secure" not in kwargs else kwargs["secure"]
            Server.__SINGLE_INSTANCE._interceptors = None if "interceptors" not in kwargs else kwargs["interceptors"]
            Server.__SINGLE_INSTANCE.init()
        return Server.__SINGLE_INSTANCE

    class __Server:
        _grpc_server: grpc.Server = None
        _max_threads: int = 10
        _host: str = "0.0.0.0"
        _port: int = 50051
        _secure: bool = False
        _interceptors: tuple = ()

        def get_grpc_server(self):
            return self._grpc_server

        def init(self):
            self._grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=self._max_threads), interceptors=self._interceptors)
            if not self._secure:
                self._grpc_server.add_insecure_port(f"{self._host}:{self._port}")
            return self

        def start(self):
            _logging.info(f"Server start in port:  {self._port}")
            self._grpc_server.start()
            try:
                while True and self._grpc_server is not None:
                    time.sleep(3000)
            except KeyboardInterrupt as ex:
                _logging.error("Server stop.... reason: KeyboardInterrupt")

        def stop(self):
            self._grpc_server.stop(0)
            self._grpc_server = None
