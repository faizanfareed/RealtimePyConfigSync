import time
from typing import NoReturn

import etcd3

from .sync_logger import logger
from .custom_exceptions import MaximumRetiresReachedException, FutureFeatureException


class EtcdConnection:
    def __init__(self, host: str, port: int, number_of_retries: int, retry_interval: int,
                 ca_cert=None, cert_key=None, cert_cert=None, timeout=None,
                 user=None, password=None, grpc_options=None):

        self.host = host
        self.port = port

        self.ca_cert = ca_cert
        self.cert_key = cert_key
        self.cert_cert = cert_cert
        self.timeout = timeout
        self.user = user
        self.password = password
        self.grpc_options = grpc_options

        self.number_of_retries = number_of_retries
        self.retry_interval = retry_interval
        self.retried_count = 1
        self.is_connection_failed_with_etcd = False
        self.etcd_client = None
        self._initialize_etcd_client()

    def _initialize_etcd_client(self):
        logger.debug('Initializing the etcd3 client. ')
        self.etcd_client = etcd3.client(host=self.host, port=self.port,
                                        ca_cert=self.ca_cert, cert_key=self.cert_key, cert_cert=self.cert_cert,
                                        timeout=self.timeout,
                                        user=self.user, password=self.password, grpc_options=self.grpc_options)

    def establish_connection_with_etcd(self) -> None:
        try:
            if self.retried_count <= self.number_of_retries:
                logger.debug('Establishing a connection with etcd.')
                # self._initialize_etcd_client()
                self._initiate_etcd_connection()
                logger.info("Connection successfully established to etcd.")
                self.is_connection_failed_with_etcd = False
                self.retried_count = 1
            else:
                self.is_connection_failed_with_etcd = True
                logger.error('The maximum number of retries has been reached.')
                raise MaximumRetiresReachedException(f"Maximum retires reached.")
        except etcd3.exceptions.ConnectionFailedError as e:
            logger.error(f"The connection to etcd has failed. Exception: {e}")
            self._retry_countdown()
            self.establish_connection_with_etcd()

    def _initiate_etcd_connection(self) -> None:
        self.etcd_client.get('some_key')

    def _retry_countdown(self) -> None:
        logger.info(f"Retry count: '{self.retried_count}'.")
        self.retried_count += 1
        logger.info(f"Retrying after a {self.retry_interval}-seconds delay.")
        sleep_time = self.retry_interval
        for _ in range(0, self.retry_interval):
            time.sleep(1)
            sleep_time -= 1
            logger.debug(f"Retrying after a {sleep_time}-seconds delay.")

    def close_connection(self) -> NoReturn:
        raise FutureFeatureException("This feature is not yet implemented but will be available in future releases.")
        # Core etcd3 lib development in progress.
        # self.etcd_client.close()
