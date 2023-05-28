import json
from abc import ABC, abstractmethod
from typing import Union, Tuple, Any

from .sync_logger import logger


class DeserializerHandler(ABC):
    def __init__(self, successor=None):
        """

        :param successor:
        """
        self._successor = successor

    @abstractmethod
    def handle_request(self, serialization, data) -> Union[Union[bool, dict, None, Tuple[bool, None]], Any]:
        """

        :param serialization:
        :param data:
        :return:
        """
        raise NotImplementedError("Not implemented")


class AbstractDataDeserializer(ABC):

    @staticmethod
    @abstractmethod
    def deserialize(data) -> Tuple[bool, Any]:
        """

        :param data:
        :return:
        """
        raise NotImplementedError("Not Implemented")


class JSONDeserializer(AbstractDataDeserializer, DeserializerHandler):

    def handle_request(self, serialization: str, data) -> Union[Union[bool, dict, None, Tuple[bool, None]], Any]:
        """

        :param serialization:
        :param data:
        :return:
        """
        if serialization == 'JSON':
            return JSONDeserializer.deserialize(data)
        elif self._successor:
            return self._successor.handle_request(serialization=serialization, data=data)
        else:
            return False, None

    @staticmethod
    def deserialize(data) -> Tuple[bool, Any]:
        """

        :param data:
        :return:
        """
        try:
            deserialized_data = json.loads(data)
            logger.debug('Data successfully deserialized.')
            return True, deserialized_data
        except json.JSONDecodeError as e:
            logger.error(f'JSONDecodeError: {e}')
            return False, None
