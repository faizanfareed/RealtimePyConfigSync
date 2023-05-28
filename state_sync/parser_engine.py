from .sync_logger import logger
from .abstract_observer import Observer
from .deserializer import JSONDeserializer
from .app_config import ADD_NEW_WATCH_CHANGES_ON_PREFIX, SERIALIZATION_SUPPORT


class ParserEngine(Observer):
    """It serializes and deserializes the data in different formats.
    """

    def __init__(self, keys: dict):
        self.keys = keys
        self.data = {}
        self.deserializer_handler_instance = JSONDeserializer()

    def update_received(self, key: str, value: str) -> None:
        logger.debug(f"An update has been received in the ParserEngine.. key : '{key}' -  value : '{value}'")
        self.template_method(key=key, value=value)

    def update_the_new_changes(self, key: str, value):
        """

        :param key:
        :param value:
        :return:
        """
        self.data[key] = value

    def template_method(self, key: str, value: str) -> None:
        """

        :param key:
        :param value:
        :return:
        """

        if key in self.keys:
            keys_details = self.keys.get(key)
            if isinstance(keys_details, dict) and 'serialization' in keys_details:
                serialization = keys_details.get('serialization')
                logger.info(f"The serialization key exists in the defined keys, and deserialization is being applied."
                            f" {serialization}.")
                is_deserialized, data = self.deserializer_handler_instance.handle_request(serialization=serialization,
                                                                                          data=value)
                if is_deserialized:
                    self.update_the_new_changes(key=key, value=data)
                else:
                    logger.info(f"The data was not successfully deserialized.")
            else:
                logger.info("Key-value pairs have been successfully stored..")
                self.update_the_new_changes(key=key, value=value)
        else:
            logger.info("Changes have been detected on a key that does not exist in our defined keys.")
            self.parse_undefined_keys_base_on_prefix(key=key, value=value)

    def parse_undefined_keys_base_on_prefix(self, key: str, value: str) -> None:
        """

        :param key:
        :param value:
        :return:
        """
        if ADD_NEW_WATCH_CHANGES_ON_PREFIX:
            logger.info("ADD_NEW_WATCH_CHANGES_ON_PREFIX is enabled.")
            # There might be a key that requires different types of deserialization,
            # so applying a brute force technique to handle it.
            is_deserialized = False
            logger.debug("Applying different deserialization techniques to the key and value.")
            data = None
            for serialization in SERIALIZATION_SUPPORT:
                logger.debug(f"Trying to deserialized data with : '{serialization}' method.")
                is_deserialized_data, data = self.deserializer_handler_instance.handle_request(serialization=
                                                                                               serialization,
                                                                                               data=value)
                if is_deserialized_data:
                    is_deserialized = True
                    logger.info(f"The data has been successfully deserialized using '{serialization}' method.")
                    self.update_the_new_changes(key=key, value=data)
                    break
                logger.info(f"The data was not successfully deserialized using the '{serialization}' method.")
            if not is_deserialized:
                self.update_the_new_changes(key=key, value=value)
                logger.info(f"All available deserialization methods '{SERIALIZATION_SUPPORT}' were applied to the data,"
                            f" but it was not successfully deserialized. Therefore, the data will be stored as it is.")
        else:
            logger.info("If you want to detect these changes as well, you can enable the configuration "
                        "option 'ADD_NEW_WATCH_CHANGES_ON_PREFIX' and set it to True.")
