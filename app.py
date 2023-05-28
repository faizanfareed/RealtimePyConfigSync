import time

import etcd3

from state_sync.sync_logger import logger
from state_sync.parser_engine import ParserEngine
from state_sync.watcher import WatchForChanges
from state_sync.custom_exceptions import MaximumRetiresReachedException


def main():
    watcher = None

    try:

        host = 'localhost'
        port = 2379
        number_of_retries = 3
        retry_interval = 10

        # Setting the call_back_type parameter to "PREFIX" allows you to watch changes on a prefix key.
        keys_for_watch = {
            "feature": None,  # Listen to the key-value pair without the need to pass any other details.
            "/spacecrafts/orbit/": None,
            "/spacecrafts/": {"call_back_type": "PREFIX"},
            "/customer_config/customer1/": {"serialization": "JSON"},
            "/customer_config/customer4": None,
            "/customer_config/": {"call_back_type": "PREFIX"},
        }

        watcher = WatchForChanges(host=host, port=port, number_of_retries=number_of_retries,
                                  retry_interval=retry_interval, ca_cert=None, cert_key=None,
                                  cert_cert=None, timeout=10, user=None, password=None,
                                  grpc_options=None)

        # Establish connection with etcd
        watcher.etcd_connection_obj.establish_connection_with_etcd()

        watcher.start_watch_keys(keys=keys_for_watch)
        logger.debug(f"Watch id map: {watcher.watch_id_map}")

        # Create an instance of the ParserEngine class and subscribe to receive notifications for new changes.
        parser_engine = ParserEngine(keys=keys_for_watch)
        # You can create your own observer and attach it to listen for all changes.
        # To do this, you need to implement the Observer class.
        watcher.attach(observer=parser_engine)

        for i in range(0, 50000):

            # Performing business logic processing.
            time.sleep(1)

            # View the changes using the is_change_detected and perform the necessary operations.
            if watcher.is_change_detected:
                # You can directly retrieve the data from the watcher instance.
                logger.info(f"Raw key-value data : {watcher.data}")
                watcher.is_change_detected = False

                # Retrieve the parsed data.
                logger.info(f"Parser engine data : {parser_engine.data}")

            # Whenever a connection fails with etcd, it will attempt to reconnect and continue listening for changes
            if watcher.etcd_connection_obj.is_connection_failed_with_etcd:
                watcher.on_failure_connect_with_etcd_and_continue_watch_for_changes()

    except etcd3.exceptions.ConnectionFailedError as connect_ex:
        logger.error(f"A connection failure occurred while watching the key. {connect_ex}")

    except MaximumRetiresReachedException as max_ex:
        logger.error(f"MaximumRetiresReachedException {max_ex}")

    watcher.close_connection()


if __name__ == '__main__':
    main()
