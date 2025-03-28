import database

class Analyser:
    def __init__(self) -> None:
        self._db_client = database.Client()
        self._db_client.query_all_instances()