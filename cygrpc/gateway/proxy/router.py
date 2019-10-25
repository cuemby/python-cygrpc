"""
Http router

"""
import json
import logging as _logging
import os

from bottle import BaseRequest, request, run, route, response
from cygrpc.gateway.proxy.reverse_stub import ReverseStub
# increase payload size
BaseRequest.MEMFILE_MAX = 1024 * 1024 * 100

_logging.basicConfig(
    level=os.getenv("LOGLEVEL", "INFO"),
    format='%(levelname)s | %(asctime)s - %(name)s - %(message)s')


class Router:
    __SINGLE_INSTANCE = None

    def __new__(cls, *args, **kwargs):
        if not Router.__SINGLE_INSTANCE:
            _router = Router.__Router()
            cls.__SINGLE_INSTANCE = _router
        return cls.__SINGLE_INSTANCE

    class __Router:
        reverse_stub: ReverseStub = None

        def add_route(self, service: str, grpc_method: str, url_path: str, http_method: str):
            @route(url_path, method=http_method)
            def intercent(**args):
                print(request.route.rule)
                request_json = request.json if request.json is not None else {}
                payload = {**args, **request_json}
                headers = dict(request.headers)
                head_to_metadata = [(str(key).lower(), headers[key]) for key in headers]
                head_to_metadata.append(("interface", "HTTP"))
                head_to_metadata = tuple(head_to_metadata)
                print(head_to_metadata)
                result = Router().reverse_stub.execute(service, grpc_method, payload=payload, metadata=head_to_metadata)
                response.set_header("Content-Type", "application/json")
                return json.dumps(result)

        def run_serve(self, port=3000, debug=True):
            _logging.info("starting http serve on port: "+str(port))
            run(host='0.0.0.0', port=port, debug=debug)
            exit(0)
