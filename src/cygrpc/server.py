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
        return Server.__SINGLE_INSTANCE

    class __Server:
        server: grpc.Server = None
        _threads_executors: int = 10
        port: int = 50051
        services: list = []

        def for_port(self, port: int):
            self.port = port
            return self

        def max_workers(self, size: int):
            self._threads_executors = size
            return self

        def build(self):
            self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=self._threads_executors))
            return self

        def start(self):
            _logging.info(f"Server start in port:  {self.port}")
            self.serve.start()
            try:
                while True and self.server is not None:
                    time.sleep(3000)
            except KeyboardInterrupt as ex:
                _logging.error("Server stop.... reason: KeyboardInterrupt")

        def stop(self):
            self.server.stop(0)
            self.server = None
