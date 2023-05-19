import json
from abc import ABC, abstractmethod

from logger import logger


class DeserializerHandler(ABC):
    def __init__(self, successor=None):
        self._successor = successor

    @abstractmethod
    def handle_request(self, serialization, data):
        raise NotImplementedError("Not implemented")


class AbstractDataDeserializer(ABC):

    @staticmethod
    @abstractmethod
    def deserialize(data):
        raise NotImplementedError("Not Implemented")


class JSONDeserializer(AbstractDataDeserializer, DeserializerHandler):

    def handle_request(self, serialization, data):
        if serialization == 'JSON':
            return JSONDeserializer.deserialize(data)
        elif self._successor:
            return self._successor.handle_request(serialization=serialization, data=data)
        else:
            return False, None

    @staticmethod
    def deserialize(data):
        try:
            deserialized_data = json.loads(data)
            logger.debug('Data successfully deserialized.')
            return True, deserialized_data
        except json.JSONDecodeError as e:
            logger.error(f'JSONDecodeError: {e}')
            return False, None
