# database.py

from tinydb import TinyDB, Query

class Database:
    def __init__(self, db_path='jarvis_db.json'):
        self.db = TinyDB(db_path)

    def get_user_preference(self, key):
        """Retrieves a user preference from the database."""
        User = Query()
        result = self.db.search(User.key == key)
        return result[0]['value'] if result else None

    def set_user_preference(self, key, value):
        """Sets a user preference in the database."""
        User = Query()
        self.db.upsert({'key': key, 'value': value}, User.key == key)

    def log_interaction(self, command, response):
        """Logs an interaction to the database."""
        self.db.table('interactions').insert({
            'command': command,
            'response': response,
            'timestamp': self.get_timestamp()
        })

    def get_timestamp(self):
        """Returns the current timestamp."""
        import datetime
        return datetime.datetime.now().isoformat()
