"""
Http router

"""
import json

from bottle import request, run, route, response

from cygrpc.gateway.proxy.reverse_stub import ReverseStub


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
                print(dir(request.route))
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

        def run_serve(self, port=3000):
            print("starting http serve")
            run(host='0.0.0.0', port=port, debug=True)
            exit(0)


"""
class Router:
    __SINGLE_INSTANCE = None

    def __new__(cls, *args, **kwargs):
        if not Router.__SINGLE_INSTANCE:
            _router = Router.__Router()
            cls.__SINGLE_INSTANCE = _router
        return cls.__SINGLE_INSTANCE

    class __Router:
        services = list()
        routes = {
            "GET": dict(),
            "POST": dict(),
            "PATCH": dict(),
            "PUT": dict(),
            "DELETE": dict()
        }

        def add_route(self, service: str, grpc_method: str, url_path: str, http_method: str):
            route = {
                "service": service,
                "grpc_method": grpc_method
            }
            self.routes[http_method.upper()][url_path] = route

        def get_route(self, http_method, url_path):
            return self.routes[http_method][url_path]

        def print(self):
            print(self.routes)


"""
