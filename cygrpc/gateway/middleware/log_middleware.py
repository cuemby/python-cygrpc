import logging
import os

from cygrpc.gateway.middleware.base import BasePosMiddleware

logging.basicConfig(
    level=os.getenv("LOGLEVEL", "INFO"),
    format='%(levelname)s | %(asctime)s - %(message)s')


class CygrpcLogMiddleware(BasePosMiddleware):
    def on_success(self, request: dict, response: dict, header: dict) -> None:
        logging.info(
            f"{request['method']} | {request['route']} | length: f{request['headers']['content-length']} | status: {header['status']}")

    def on_error(self, request: dict, response: dict, header: dict, error: Exception) -> None:
        logging.error(
            f"{request['method']} | {request['route']}  | status: {header['status']} | type: {type(error)} | error :{str(error.__cause__ if error.__cause__ is not None else error)}")
