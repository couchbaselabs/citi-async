from typing import Optional


class ConnConfig:
    """
    Configuration class for Couchbase connection settings.
    """

    def __init__(
        self,
        host_or_dsn: str,
        user_name: str,
        password: str,
        bucket_name: str,
        scope_name: str = "_default",
        collection_name: str = "_default",
        ssl: bool = False,
        ca_cert: Optional[str] = None,
        connect_timeout: int = 10,
        kv_timeout: int = 5,
        wait_timeout: int = 5,
        sasl_mech: str = "PLAIN"
    ):
        """
        Initializes the Couchbase connection configuration.

        :param host_or_dsn: The Couchbase cluster hostname or DSN.
        :param user_name: Username for Couchbase authentication.
        :param password: Password for Couchbase authentication.
        :param bucket_name: Name of the Couchbase bucket to connect to.
        :param scope_name: Name of the scope (default is "_default").
        :param collection_name: Name of the collection (default is "_default").
        :param ssl: Whether to use SSL (default is False).
        :param ca_cert: Path to CA certificate if SSL is enabled.
        :param connect_timeout: Timeout for cluster connection in seconds.
        :param kv_timeout: Timeout for key-value operations in seconds.
        :param wait_timeout: Timeout for waiting for cluster readiness.
        :param sasl_mech: SASL mechanism for authentication (default is "PLAIN").
        """
        self.host_or_dsn = host_or_dsn
        self.user_name = user_name
        self.password = password
        self.bucket_name = bucket_name
        self.scope_name = scope_name
        self.collection_name = collection_name
        self.ssl = ssl
        self.ca_cert = ca_cert
        self.connect_timeout = connect_timeout
        self.kv_timeout = kv_timeout
        self.wait_timeout = wait_timeout
        self.sasl_mech = sasl_mech

    def __repr__(self):
        """
        Returns a string representation of the connection config.
        """
        return (f"ConnConfig(host_or_dsn='{self.host_or_dsn}', user='{self.user_name}', "
                f"bucket='{self.bucket_name}', scope='{self.scope_name}', collection='{self.collection_name}', "
                f"ssl={self.ssl}, connect_timeout={self.connect_timeout}, kv_timeout={self.kv_timeout}, "
                f"wait_timeout={self.wait_timeout}, sasl_mech='{self.sasl_mech}')")
