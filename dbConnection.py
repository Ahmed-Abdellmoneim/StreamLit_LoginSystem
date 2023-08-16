import mysql.connector

class DatabaseSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def connect_to_database(self):
        if self.connection is None:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='meal_rec'
            )
        return self.connection

# Usage example:
db_singleton = DatabaseSingleton()
db_connection = db_singleton.connect_to_database()

# Now use the 'db_connection' object to interact with the database.
# For example:
# cursor = db_connection.cursor()
# cursor.execute('SELECT * FROM table_name')
# rows = cursor.fetchall()
# ...
