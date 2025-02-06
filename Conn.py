import logging
import asyncio
from datetime import timedelta
from acouchbase.cluster import Cluster, get_event_loop
from couchbase.auth import PasswordAuthenticator
from couchbase.options import ClusterOptions, ClusterTimeoutOptions, GetOptions, UpsertOptions
from couchbase.transcoder import RawBinaryTranscoder
from couchbase.exceptions import DocumentNotFoundException
from Config import ConnConfig
from BaseRepo import BaseRepo


logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


class _OnlineRepoCouchbase(BaseRepo):
    """
    Online repository implementation for Couchbase.
    """

    def __init__(self, conn_config: ConnConfig):
        """
        Initialize the Couchbase repository instance.
        """
        super().__init__()
        self.conn = None
        self.cluster = None
        self.conn_config = conn_config
        print("Initialization successful!")

    async def initialize_repo(self):
        """
        Initializes the Couchbase connection.
        """
        try:
            if self.conn is None:
                LOG.info("Connecting to Couchbase...")

                await self.create_conn(self.conn_config)

                LOG.info("Connection setup pending...")
            LOG.info("Online repo connection successful")
        except Exception as exe:
            LOG.error(f"Error initializing repository: {exe}")
            raise exe

    async def create_conn(self, conn_config: ConnConfig):
        """
        Creates and stores a connection to Couchbase.
        """
        try:
            LOG.info(f'Connecting to Couchbase at {conn_config.host_or_dsn}...')

            # Set up authentication
            auth = PasswordAuthenticator(conn_config.user_name, conn_config.password)

            LOG.info("Authentication setup successful")

            # Timeout settings
            timeout_opts = ClusterTimeoutOptions(
                connect_timeout=timedelta(seconds=conn_config.connect_timeout),
                kv_timeout=timedelta(seconds=conn_config.kv_timeout)
            )

            self.cluster = await Cluster.connect(
                f"couchbase://{conn_config.host_or_dsn}",
                ClusterOptions(auth, timeout_options=timeout_opts)
            )

            # Wait until cluster is ready
            await self.cluster.on_connect()
            LOG.info("Couchbase cluster connection successful!")

            # Select bucket, scope, and collection
            bucket = self.cluster.bucket(conn_config.bucket_name)
            await bucket.on_connect()  # Ensure the bucket is ready
            scope = bucket.scope(conn_config.scope_name)
            self.conn = scope.collection(conn_config.collection_name)

            LOG.info("Bucket and collection selected successfully.")

        except Exception as exception:
            LOG.error(f"Failed to connect to Couchbase: {exception}")
            raise exception

    async def validate(self):
        """
        Validates the Couchbase connection.
        """
        try:
            transcoder = RawBinaryTranscoder()
            result = await self.conn.get("dummykey", GetOptions(transcoder=transcoder))
            LOG.info("Online repo connection successful")
            return result
        except DocumentNotFoundException:
            LOG.info("Validation successful: dummykey not found (expected for validation).")
            return None
        except Exception as exception:
            LOG.error("Failed to validate Couchbase connection")
            raise exception

    async def find_by_key(self, key, compress):
        """
        Find online features by key.
        """
        try:
            result = await self.conn.get(key)

            # Debugging: Print raw content
            LOG.info(f"Retrieved raw content for key '{key}': {result.content_as[str]}")

            if compress:
                transcoder = RawBinaryTranscoder()
                return result.content_as[bytes]
            else:
                try:
                    return result.content_as[dict]
                except ValueError:
                    LOG.error(f"Document '{key}' is not in JSON format.")
                    return result.content_as[str]
        except DocumentNotFoundException:
            LOG.info(f"Document '{key}' not found.")
            return None
        except Exception as exception:
            LOG.error(f"Error retrieving document '{key}': {exception}")
            raise exception

    async def save(self, key, value, compress):
        """
        Save <key,value> object to online repository.
        """
        try:
            if compress:
                transcoder = RawBinaryTranscoder()
                return await self.conn.upsert(key, value, UpsertOptions(transcoder=transcoder))
            else:
                return await self.conn.upsert(key, value)
        except Exception as exception:
            raise exception

    def save_all(self, obj_to_save):
        """
        Save all objects into online repository.
        """
        try:

            for key, value in obj_to_save.items():
                self.conn.upsert(key, value)
        except Exception as exception:
            raise exception

    def native_query(self, query):
        """
        Execute native query, e.g., N1QL query.
        """
        try:
            result = self.cluster.query(query)
            return [row for row in result]
        except Exception as exception:
            raise exception


connection = ConnConfig(
    host_or_dsn="localhost",
    user_name="Administrator",
    password="password",
    bucket_name="test",
    scope_name="test",
    collection_name="test"
)


async def test_connection():
    """
    Test function to initialize and validate the repository.
    """
    repo = _OnlineRepoCouchbase(connection)
    await repo.initialize_repo()

    # Validate connection
    await repo.validate()
    await repo.save("101", "ok", False)
    await repo.find_by_key("foo", False)


if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(test_connection())


