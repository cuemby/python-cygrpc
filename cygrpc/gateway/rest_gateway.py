"""
Gateway instance
"""
import os
import socketserver
import threading
import traceback
from http import HTTPStatus
from time import sleep

from cygrpc.gateway.proxy.reverse_stub import ReverseStub
from http.server import HTTPServer, BaseHTTPRequestHandler

from cygrpc.gateway.proxy.router import Router

PORT = 8080
_ENVIRONMENT = os.getenv("ENVIRONMENT", "production").lower()

"""
class _HttpHandler(BaseHTTPRequestHandler):
    proto_handler: ReverseStub = None

    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def _build_response(self, message):
        #This just generates an HTML document that includes `message`
        #in the body. Override, or re-write this do do more interesting stuff.
        
        content = f"{message}"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self.process("GET")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self.process("POST")

    def do_DELETE(self):
        self.process("DELETE")

    def do_PUT(self):
        self.process("PUT")

    def process(self, method):
        path = self.path
        header = dict(self.headers)
        body = self.rfile.read(int(header["Content-Length"]))
        body = body.decode("utf-8")
        try:
            route_definition = Router().get_route(method, path)
            response = self.proto_handler.execute(route_definition["service"], route_definition["grpc_method"], body)
            self._set_headers()
            self.wfile.write(self._build_response(str(response)))
        except Exception as err:
            # traceback.print_exc()
            print(type(err), ":", str(err.__str__()))
            if type(err) == KeyError:
                if err.__str__() == f"'{path}'":
                    # not found
                    self._set_headers(HTTPStatus.NOT_FOUND.value)
                    self.wfile.write(self._build_response(""))
                elif err.__str__().count("does not have a field") > 0:
                    # bad request
                    self._set_headers(HTTPStatus.BAD_REQUEST.value)
            else:
                # internal
                self._set_headers(HTTPStatus.INTERNAL_SERVER_ERROR.value)
                self.wfile.write(self._build_response(str(err) if _ENVIRONMENT != "production" else ""))

"""


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
    router.run_serve(port=port)


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
