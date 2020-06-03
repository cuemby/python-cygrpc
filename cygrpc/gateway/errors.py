import json


class HttpErr(Exception):
    status: int = 500
    value: str = "Internal Server Error"
    details = ""

    def __init__(self, details):
        self.details = details

    def __str__(self):
        return json.dumps(self.dict())

    def dict(self):
        return {"status": self.status, "message": self.value, "details": self.details}


# ===  4XX - Client errors ===


class HttpErrBadRequest(HttpErr):
    status = 400
    value = "Bad request"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrUnauthorized(HttpErr):
    status = 401
    value = "Unauthorized"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrPaymentRequired(HttpErr):
    status = 402
    value = "Payment Required"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrForbidden(HttpErr):
    status = 403
    value = "Forbidden"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrNotFound(HttpErr):
    status = 404
    value = "Not Found"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrMethodNotAllowed(HttpErr):
    status = 405
    value = "Method Not Allowed"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrNotAcceptable(HttpErr):
    status = 406
    value = "Not Acceptable"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrProxyAuthenticationRequired(HttpErr):
    status = 407
    value = "Proxy Authentication Required"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrRequestTimeout(HttpErr):
    status = 408
    value = "Request Timeout"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrConflict(HttpErr):
    status = 409
    value = "Conflict"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrGone(HttpErr):
    status = 410
    value = "Gone"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrLengthRequired(HttpErr):
    status = 411
    value = "Length Required"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrPreconditionFailed(HttpErr):
    status = 412
    value = "Precondition Failed"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrPayloadTooLarge(HttpErr):
    status = 413
    value = "Payload Too Large"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrURITooLong(HttpErr):
    status = 414
    value = "URI Too Long"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrUnsupportedMediaType(HttpErr):
    status = 415
    value = "Unsupported Media Type"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrRangeNotSatisfiable(HttpErr):
    status = 416
    value = "Range Not Satisfiable"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrExpectationFailed(HttpErr):
    status = 417
    value = "Expectation Failed"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrUnprocessableEntity(HttpErr):
    status = 422
    value = "Unprocessable Entity"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrLocked(HttpErr):
    status = 423
    value = "Locked"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrFailedDependency(HttpErr):
    status = 424
    value = "Locked"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrTooEarly(HttpErr):
    status = 425
    value = "Too Early"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrUpgradeRequired(HttpErr):
    status = 426
    value = "Upgrade Required"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrPreconditionRequired(HttpErr):
    status = 428
    value = "Precondition Required"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrTooManyRequests(HttpErr):
    status = 428
    value = "Too Many Requests"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrRequestHeaderFieldsTooLarge(HttpErr):
    status = 431
    value = "Request Header Fields Too Large"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrUnavailableForLegalReasons(HttpErr):
    status = 431
    value = "Unavailable For Legal Reasons"

    def __init__(self, details: str = ""):
        super().__init__(details)


# ===  5XX - Server errors ===

class HttpErrInternalServerError(HttpErr):
    status = 500
    value = "Internal Server Error"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrNotImplemented(HttpErr):
    status = 501
    value = "Not Implemented"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrBadGateway(HttpErr):
    status = 502
    value = "Bad Gateway"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrServiceUnavailable(HttpErr):
    status = 503
    value = "Service Unavailable"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrGatewayTimeout(HttpErr):
    status = 504
    value = "Gateway Timeout"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrHTTPVersionNotSupported(HttpErr):
    status = 505
    value = "HTTP Version Not Supported"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrVariantAlsoNegotiates(HttpErr):
    status = 506
    value = "Variant Also Negotiates "

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrInsufficientStorage(HttpErr):
    status = 507
    value = "Insufficient Storage"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrLoopDetected(HttpErr):
    status = 508
    value = "Loop Detected"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrNotExtended(HttpErr):
    status = 510
    value = "Not Extended"

    def __init__(self, details: str = ""):
        super().__init__(details)


class HttpErrNetworkAuthenticationRequired(HttpErr):
    status = 511
    value = "Network Authentication Required"

    def __init__(self, details: str = ""):
        super().__init__(details)


def http_status_from_grpc_code(status_code, details="") -> HttpErr:
    import grpc
    if grpc.StatusCode.UNKNOWN == status_code:
        return HttpErrInternalServerError(details)
    if grpc.StatusCode.CANCELLED == status_code:
        return HttpErrRequestTimeout(details)
    elif grpc.StatusCode.INVALID_ARGUMENT == status_code:
        return HttpErrBadRequest(details)
    elif grpc.StatusCode.DEADLINE_EXCEEDED == status_code:
        return HttpErrGatewayTimeout(details)
    elif grpc.StatusCode.NOT_FOUND == status_code:
        return HttpErrNotFound(details)
    elif grpc.StatusCode.ALREADY_EXISTS == status_code:
        return HttpErrConflict(details)
    elif grpc.StatusCode.PERMISSION_DENIED == status_code:
        return HttpErrForbidden(details)
    elif grpc.StatusCode.UNAUTHENTICATED == status_code:
        return HttpErrUnauthorized(details)
    elif grpc.StatusCode.RESOURCE_EXHAUSTED == status_code:
        return HttpErrTooManyRequests(details)
    elif grpc.StatusCode.FAILED_PRECONDITION == status_code:
        # Note, this deliberately doesn't translate to the similarly named 412 Precondition Failed HTTP response status
        return HttpErrBadRequest(details)
    elif grpc.StatusCode.ABORTED == status_code:
        return HttpErrConflict(details)
    elif grpc.StatusCode.OUT_OF_RANGE == status_code:
        return HttpErrBadRequest(details)
    elif grpc.StatusCode.UNIMPLEMENTED == status_code:
        return HttpErrNotImplemented(details)
    elif grpc.StatusCode.UNAVAILABLE == status_code:
        return HttpErrServiceUnavailable(details)
    elif grpc.StatusCode.DATA_LOSS == status_code:
        return HttpErrInternalServerError(details)
    else:
        return HttpErrInternalServerError(details)
