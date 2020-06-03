import abc


class BasePreMiddleware(metaclass=abc.ABCMeta):
    """
    Execute action method
    """

    @abc.abstractmethod
    def process(self, route: dict, request: dict, header: dict) -> None:
        raise NotImplementedError("BasePreMiddleware.action")


class BasePosMiddleware(metaclass=abc.ABCMeta):
    """
    Pos middleware if process is done call on_success, if any except is returned call on_error
    """

    @abc.abstractmethod
    def on_success(self, request: dict, response: dict, header: dict) -> None:
        raise NotImplementedError("BasePreMiddleware.action")

    @abc.abstractmethod
    def on_error(self, request: dict, response: dict, header: dict, error: dict) -> None:
        raise NotImplementedError("BasePreMiddleware.action")
