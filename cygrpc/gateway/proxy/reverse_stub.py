"""
Utils for reverse protobuf
"""
from typing import Tuple

import grpc

from cygrpc.gateway import errors
from cygrpc.protobuf_to_dict import protobuf_to_dict, dict_to_protobuf
from cygrpc.utils import extractor

registry = {}


class RegisteringType(type):
    def __init__(cls, name, bases, attrs):
        for key, val in attrs.iteritems():
            properties = getattr(val, 'route', None)
            if properties is not None:
                registry['%s.%s' % (name, key)] = properties


class ReverseStub:
    """
    Create a stub instance for rest gateway from pb2_grpc compiled module
    """

    def __init__(self, grpc_host, grpc_port):
        self.stubs = dict()
        self.server_host = grpc_host
        self.server_port = grpc_port
        self.channel = None

    def add_service(self, pb2_grpc, impl):

        _stub = extractor.extract_stub_class(pb2_grpc)
        methods = extractor.extract_servicer_methods_names(pb2_grpc)
        module = extractor.extract_module(pb2_grpc)
        requests_responses = extractor.extract_requests_responses(pb2_grpc, methods=methods)
        self.stubs[impl.__class__.__name__.strip()] = dict()
        for method in methods:
            self.stubs[impl.__class__.__name__.strip()][method] = {
                "_stub": _stub,
                "stub": None,
                "module": module,
                "requests_response": requests_responses[method.strip()]
            }

    def init_channel(self):
        _host = "localhost" if self.server_host == "0.0.0.0" else self.server_host
        self.channel = grpc.insecure_channel(f"{_host}:{self.server_port}")
        current = ""
        temp_stub = None
        for impl in self.stubs:
            for method in self.stubs[impl]:
                if impl != current:
                    temp_stub = self.stubs[impl][method]["_stub"](self.channel)
                # self.stubs[impl][method]["stub"] = temp_stub
                del self.stubs[impl][method]["_stub"]
                self.stubs[impl][method]["stub_method"] = getattr(temp_stub, method)

    def execute(self, service: str, method: str, payload: dict, metadata: tuple = ()) -> Tuple[dict, dict]:
        """
        :param service:
        :param method:
        :param payload:
        :param metadata:
        :return: response body , metadata headers
        """
        request = None
        try:
            request = dict_to_protobuf(
                self.stubs[service.strip()][method.strip()]["requests_response"]["request"](),
                payload
            )
        except Exception as err:
            raise errors.HttpErrBadRequest(str(err))
        response, call = self.stubs[service.strip()][method.strip()]["stub_method"].with_call(request,
                                                                                              metadata=metadata)
        metadata_response = {}
        for key, value in call.trailing_metadata():
            metadata_response[key] = value
        return protobuf_to_dict(response, use_enum_labels=True, including_default_value_fields=True), metadata_response
