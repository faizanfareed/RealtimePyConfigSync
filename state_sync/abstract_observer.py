from abc import ABC, abstractmethod

from .sync_logger import logger


class Observer(ABC):
    @abstractmethod
    def update_received(self, key: str, value: str) -> None:
        raise NotImplementedError("Not implemented.")


class Subject(ABC):
    def __init__(self):
        self._observers = []

    def attach(self, observer) -> None:
        self._observers.append(observer)

    def detach(self, observer) -> None:
        self._observers.remove(observer)

    def notify_state_change(self, key: str, value: str) -> None:
        """

        :param key:
        :param value:
        :return:
        """
        logger.debug(f"Notifier called : key : '{key}' - value : '{value}'")
        for observer in self._observers:
            observer.update_received(key, value)
