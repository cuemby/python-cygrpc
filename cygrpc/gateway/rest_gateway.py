"""
Gateway instance
"""
import os
import threading

from cygrpc.gateway.proxy.reverse_stub import ReverseStub
from cygrpc.gateway.proxy.router import Router

PORT = 8080
_ENABLE_DEBUG = True if os.getenv("ENVIRONMENT", "develop").lower() == "develop" else False


def _run_http(stub_handler: ReverseStub, port: int):
    """
    stub_handler.init_channel()
    _HttpHandler.proto_handler = stub_handler
    with socketserver.TCPServer(("", PORT), _HttpHandler) as httpd:
        print("serving http at port", PORT)
        httpd.serve_forever()
    """
    stub_handler.init_channel()
    router = Router()
    router.reverse_stub = stub_handler
    router.run_serve(port=port, debug=_ENABLE_DEBUG)


class HttpGateway:
    """
    Gateway implementation
    """

    def __init__(self, grpc_host="0.0.0.0", grpc_port=50051):
        self.stub_handler = ReverseStub(grpc_host=grpc_host, grpc_port=grpc_port)

    def add_service(self, pb2_grpc, impl):
        self.stub_handler.add_service(pb2_grpc, impl)

    def start(self, port=3000):
        thread = threading.Thread(target=_run_http, args=(self.stub_handler, port,))
        thread.run()
