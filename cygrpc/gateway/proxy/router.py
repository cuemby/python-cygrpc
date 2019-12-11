"""
Http router

"""
import json
import logging as _logging
import os
import traceback

import bottle
import grpc
from bottle import request, response

from cygrpc.gateway import errors
from cygrpc.gateway.middleware import CygrpcLogMiddleware
from cygrpc.gateway.proxy.middleware import MiddlewareManager
from cygrpc.gateway.proxy.reverse_stub import ReverseStub

debuger = False
# increase payload size
bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024 * 100

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
            @bottle.route(url_path, method=http_method)
            def intercent(**args):
                # print(bottle.request.route)
                # get request json payload
                request_json = bottle.request.json if request.json is not None else {}
                # routing dict
                route = {"method": bottle.request.route.method, "rule": bottle.request.route.rule, "path": bottle.request.path}
                # merge json payload with url params
                payload = {**args, **request_json}
                # extract request headers
                request_headers = {}
                for key in dict(request.headers):
                    request_headers[key.lower()] = dict(request.headers)[key]
                # dictionary with all request content
                request_obj = {"route": bottle.request.path, "method": http_method, "payload": payload,
                               "headers": request_headers}
                # request headers base
                response_headers = {"Content-Type": "application/json", "status": 200}
                try:
                    # execute all pre middleware http
                    for middleware in MiddlewareManager().global_pre_middleware:
                        middleware.process(route, payload, request_headers)
                    # parse request headers to metadata
                    head_to_metadata = [(str(key).lower(), request_headers[key]) for key in request_headers]
                    head_to_metadata.append(("interface", "HTTP"))
                    head_to_metadata = tuple(head_to_metadata)
                    # call stub ...
                    result, result_headers = Router().reverse_stub.execute(service, grpc_method, payload=payload,
                                                                           metadata=head_to_metadata)
                    # merge result metadata headers in response headers base
                    for key in result_headers:
                        response_headers[key] = result_headers[key]
                    # keep status code
                    status = response_headers["status"]
                    # execute all pos middleware
                    for middleware in MiddlewareManager().global_pos_middleware:
                        middleware.on_success(request_obj, result, response_headers)
                    # put all headers in response object
                    for key in response_headers:
                        response.set_header(key, response_headers[key])
                    # set  status from headers if is present
                    if "status" in response_headers:
                        status = int(response_headers["status"])
                    return bottle.HTTPResponse(status=status, body=json.dumps(result), headers=response_headers)
                except RuntimeError as err:
                    http_error = errors.HttpErrBadRequest(str(err.__cause__ if err.__cause__ is not None else err))
                    response_headers['status'] = http_error.status
                    error_response = http_error.dict()
                    for middleware in MiddlewareManager().global_pos_middleware:
                        middleware.on_error(request_obj, error_response, response_headers, err)
                    status = response_headers['status'] if "status" in response_headers else http_error.status
                    return bottle.HTTPResponse(status=status, body=json.dumps(error_response), headers=response_headers)
                except grpc.RpcError as err:
                    http_error = errors.http_status_from_grpc_code(err.code(), err.details())
                    response_headers['status'] = http_error.status
                    error_response = http_error.dict()
                    for middleware in MiddlewareManager().global_pos_middleware:
                        middleware.on_error(request_obj, error_response, response_headers, err)
                    status = response_headers['status'] if "status" in response_headers else http_error.status
                    return bottle.HTTPResponse(status=status, body=json.dumps(error_response), headers=response_headers)
                except errors.HttpErr as http_error:
                    response_headers['status'] = http_error.status
                    error_response = http_error.dict()
                    for middleware in MiddlewareManager().global_pos_middleware:
                        middleware.on_error(request_obj, error_response, response_headers, http_error)
                    status = response_headers['status'] if "status" in response_headers else http_error.status
                    return bottle.HTTPResponse(status=status, body=json.dumps(error_response), headers=response_headers)
                except Exception as err:
                    error_response = {}
                    traceback.print_exc()
                    status = response_headers['status'] = 500
                    for middleware in MiddlewareManager().global_pos_middleware:
                        middleware.on_error(request_obj, error_response, response_headers, err)
                    if "status" in response_headers:
                        status = int(response_headers["status"])
                    return bottle.HTTPResponse(status=status, body=json.dumps(error_response), headers=response_headers)

        def run_serve(self, port=3000, debug=False):
            debuger = debug
            MiddlewareManager().add_pos_middleware(CygrpcLogMiddleware)
            _logging.info(f"starting http serve on port: {port}")
            bottle.run(host='0.0.0.0', port=port, debug=debug, quiet=True, server='paste')
            exit(0)
