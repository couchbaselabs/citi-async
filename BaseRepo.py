class BaseRepo:
    """
    Base repository class that defines a generic interface
    for database repositories.
    """

    def __init__(self):
        """
        Initialize the base repository.
        """
        self.conn = None  # Connection object placeholder

    def create_conn(self, conn_config):
        """
        Placeholder method for creating a connection.
        Should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def find_by_key(self, key, compress):
        """
        Placeholder method for retrieving a document by key.
        Should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def save(self, key, value, compress):
        """
        Placeholder method for saving a document.
        Should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def save_all(self, obj_to_save):
        """
        Placeholder method for saving multiple documents.
        Should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def native_query(self, query):
        """
        Placeholder method for executing a native query.
        Should be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")
