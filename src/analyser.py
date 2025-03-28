import database

class Anayser:
    def __init__(self) -> None:
        self.db_client = database.client.Client()