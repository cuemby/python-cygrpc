"""
Extract data from _pb2_grpc compiled file

"""
import importlib as _importlib
import inspect as _inspect
import typing as _typing


def extract_stub_class(pb2_grpc) -> _typing.ClassVar:
    """
    Extract the stub class from pb2_grpc compiled
    and return class for instance

    :param pb2_grpc:
    :return:
    """
    members = dir(pb2_grpc)
    for name in members:
        if name.find("Stub") > 0:
            _stub = getattr(pb2_grpc, name)
            return _stub
    return None


def extract_add_server(pb2_grpc):
    """
    Extract add to server function from pb2_grpc module
    :param pb2_grpc:
    :return: function for add_to_server
    :type: function
    """
    members = dir(pb2_grpc)
    for name in members:
        if name.startswith("add_") and name.endswith("_to_server"):
            _add_to_server = getattr(pb2_grpc, name)
            return _add_to_server
    return None


def extract_module(pb2_grpc):
    """
    Extract module pb2 that contains all response and request objects used
    in grpc service methods.

    is equals to: import example_pb2
    :param pb2_grpc:
    :return:
    """
    lines = _inspect.getsource(pb2_grpc).split("\n")
    for line in lines:
        if line.count("from") > 0 and line.count("as") >= 0 and line.count("_pb2") > 0:
            full_module_name = line.split(" as ")[0]
            full_module_name = full_module_name.replace(" import ", ".")
            full_module_name = full_module_name.replace("from ", "")
            return _importlib.import_module(full_module_name)


def extract_stub_methods_names(grpc_stub_class) -> _typing.List[str]:
    """
    Extract the stub methods from pb2_grpc compiled
    :param pb2_grpc:
    :return:
    """
    return list(grpc_stub_class.__dict__.keys())


def extract_servicer_methods_names(pb2_grpc):
    members = dir(pb2_grpc)
    for name in members:
        if name.endswith("Servicer"):
            servicer = getattr(pb2_grpc, name)
        return [x for x in servicer.__dict__.keys() if not str(x).startswith("__")]


def extract_requests_responses(pb2_grpc, **kwargs) -> _typing.Dict:
    """
    Extract all request and response from pb2_grpc and return a dictionary
    with the next extructure:
    {
        "method":{
            "grpc_path": path,
            "request": obj_request,
            "response": obj_response
        },
        ...
    }
    :param pb2_grpc: pb2_grpc modules
    :keyword methods_list: names for methods list. if not set auto extract from pb2_grpc
    :type: list
    :keyword module: _pb2 module, if not set auto extract from pb2_grpc
    :type: module
    :return:
    """
    lines = _inspect.getsource(pb2_grpc).split("\n")
    # print("lines", len(lines))
    methods = kwargs["methods"] if "methods" in kwargs else \
        extract_servicer_methods_names(pb2_grpc)
    module = kwargs["module"] if "module" in kwargs else \
        extract_module(pb2_grpc)
    requests_responses = dict()
    processed = list()
    for numb, line in enumerate(lines):
        for method in methods:
            if line.count(f"{method}") > 0 and method not in processed:
                processed.append(method)
                path = __sanitize_path(lines[numb + 1])
                request = __extract_protobuf_request_object_from_str(lines[numb + 2])
                response = __extract_protobuf_response_object_from_str(lines[numb + 3])
                obj_request = getattr(module, request)
                obj_response = getattr(module, response)
                requests_responses[method] = {
                    "grpc_path": path,
                    "request": obj_request,
                    "response": obj_response
                }
    return requests_responses


def __sanitize_path(line: str):
    return line.replace("'", "").replace(",", "").replace('"', "")


def __extract_protobuf_request_object_from_str(line: str):
    line = line.strip().replace(",", "").replace("request_serializer=", "").replace(".SerializeToString", "")
    line = line.split(".")
    return line[-1]


def __extract_protobuf_response_object_from_str(line: str):
    line = line.strip().replace(",", "").replace("response_deserializer=", "").replace(".FromString", "")
    # print(line)
    line = line.split(".")
    return line[-1]
