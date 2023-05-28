from enum import Enum

from etcd3.events import PutEvent
from etcd3.watch import WatchResponse

from .sync_logger import logger
from .etcd_connection import EtcdConnection
from .abstract_observer import Subject
from .app_config import ADD_NEW_WATCH_CHANGES_ON_PREFIX


class CallBackTypeEnum(Enum):
    PREFIX_TYPE = 'PREFIX'
    NON_PREFIX_TYPE = "NON-PREFIX"


class WatchForChanges(Subject):

    def __init__(self, host: str, port: int, number_of_retries: int, retry_interval: int, ca_cert=None, cert_key=None,
                 cert_cert=None, timeout=None, user=None, password=None, grpc_options=None):
        """

        :param host:
        :param port:
        :param number_of_retries:
        :param retry_interval:
        """
        super().__init__()
        # It will store the raw data.
        self.data = {}
        self.watch_id_map = {}
        # Whenever new changes are detected, the value is set to True.
        # After loading your changes, flip this value to False for future changes.
        self.is_change_detected = False
        self.watch_keys = None

        self.etcd_connection_obj = EtcdConnection(host=host, port=port, number_of_retries=number_of_retries,
                                                  retry_interval=retry_interval, ca_cert=ca_cert, cert_key=cert_key,
                                                  cert_cert=cert_cert, timeout=timeout, user=user, password=password,
                                                  grpc_options=grpc_options)

    def callback(self, event) -> None:
        """

        :param event:
        :return:
        """
        try:
            if isinstance(event, WatchResponse):
                logger.info('The Etcd callback detected new changes.')
                for event in event.events:
                    if isinstance(event, PutEvent):
                        key = event.key.decode('utf-8')
                        value = event.value.decode('utf-8')
                        if key in self.watch_keys:
                            self.data[key] = value
                        else:
                            if ADD_NEW_WATCH_CHANGES_ON_PREFIX:
                                self.data[key] = value
                            else:
                                logger.info("Changes were detected on a key that does not exist in our defined keys.")
                        self.is_change_detected = True
                        self.notify_state_change(key=key, value=value)
            else:
                debug_error_string = event.debug_error_string()

                if 'grpc_status:14' in debug_error_string:
                    logger.error(f"Server is currently unavailable or unreachable. Exception {debug_error_string}")
                else:
                    logger.error(f"Exception in callback {event}")
                self.etcd_connection_obj.is_connection_failed_with_etcd = True
        except Exception as e:
            logger.error(f'Callback exception:  {e}')

    def on_failure_connect_with_etcd_and_continue_watch_for_changes(self) -> None:
        """It attempts to connect with the etcd server, clears the watch_id_map,
        and then starts watching the keys again.

        :return:
        """
        logger.debug(f'Auto reconnecting with etcd.')
        self.etcd_connection_obj.establish_connection_with_etcd()
        logger.debug('On reconnecting start watching on keys.')
        self.watch_id_map = {}
        self.start_watch_keys(keys=self.watch_keys)

    def start_watch_keys(self, keys) -> None:
        """It iterates through all the keys one by one based on the call_back_type.
        It binds a callback function to each key and stores the returned key into the watch_id_map.

        :param keys:
        :return:
        """
        self.watch_keys = keys
        watch_id = None
        try:
            for watch_key, key_object in keys.items():
                call_back_type = CallBackTypeEnum.NON_PREFIX_TYPE.value
                if key_object:
                    if isinstance(key_object, dict):
                        call_back_type = key_object.get('call_back_type', CallBackTypeEnum.NON_PREFIX_TYPE.value)
                    else:
                        logger.debug(
                            f"Given key '{watch_key}' value is not dict type. Type of value is '{type(key_object)}'. "
                            f"Using NON-PREFIX call back for this key.")

                if call_back_type == CallBackTypeEnum.PREFIX_TYPE.value:
                    watch_id = self.etcd_connection_obj.etcd_client.add_watch_prefix_callback(watch_key, self.callback)
                    logger.debug(f"PREFIX base callback has been added. Key: '{watch_key}' - call_back_type: "
                                 f"'{call_back_type}'")
                elif call_back_type == CallBackTypeEnum.NON_PREFIX_TYPE.value:
                    watch_id = self.etcd_connection_obj.etcd_client.add_watch_callback(watch_key, self.callback)
                    logger.debug(f"NON-PREFIX base callback has been added. Key: '{watch_key}' - call_back_type: "
                                 f"'{call_back_type}'")
                else:
                    logger.error("The callback type is not valid.")
                self.watch_id_map[watch_key] = watch_id
        except Exception as e:
            logger.error(f'Exception in start_watch_keys() {e}')

    def stop_watch_keys(self) -> None:
        """It iterates through all the keys and stops watching for changes on each key.
        :return:
        """
        for key_name, watch_id in self.watch_id_map.items():
            logger.info(f"Stop watch changes on key: '{key_name}' - watch_id: {watch_id} .")
            self.etcd_connection_obj.etcd_client.cancel_watch(watch_id)
            if key_name in self.watch_keys:
                self.watch_keys.pop(key_name)

    def stop_watch_key(self, key_name: str) -> None:
        """It stops watching for changes on a specific key name.

        :param key_name:
        :return:
        """
        if key_name in self.watch_id_map:
            watch_id = self.watch_id_map.get(key_name)
            logger.info(f"Stop watch changes on key '{key_name}.")
            self.etcd_connection_obj.etcd_client.cancel_watch(watch_id)
            if key_name in self.watch_keys:
                self.watch_keys.pop(key_name)

    def close_connection(self) -> None:
        """Before closing the connection with etcd, it stops watching for changes on all keys.

        :return:
        """
        self.stop_watch_keys()
        # Etcd3 lib development in progress
        # self.etcd_connection_obj.close_connection()
