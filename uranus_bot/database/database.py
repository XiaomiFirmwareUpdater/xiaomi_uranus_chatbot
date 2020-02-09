""" Xiaomi Geeks Telegram Bot Database class"""
from sqlite3 import connect, Row, Error


class Database:
    """Database connection class"""
    def __init__(self, db):
        self.conn = connect(db)
        self.cursor = self.conn.cursor()
        self.conn.row_factory = Row  # to return dictionaries from sqlite3 queries

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement """
        try:
            self.cursor.execute(create_table_sql)
            self.conn.commit()
        except Error as err:
            print(err)

    # def drop_table(self, table_name):
    #     """ drop a table from the database """
    #     try:
    #         self.cursor.execute(f"""DROP TABLE IF EXISTS {table_name}""")
    #     except Error as e:
    #         print(e)

    def add_chat_to_db(self, sender_info):
        """ Add new row to the table"""
        if self.is_known_chat(sender_info["id"]):
            return
        try:
            self.cursor.execute(f"""INSERT INTO chats (id, username, name, type)
            VALUES(:id, :username, :name, :type)""",
                                {'id': sender_info["id"],
                                 'username': sender_info["username"],
                                 'name': sender_info["name"],
                                 'type': sender_info["type"]})
        except Error as err:
            print(err)
        finally:
            self.conn.commit()

    def is_known_chat(self, sender_id):
        """ Check if user is already in database """
        check = self.cursor.execute(f"""SELECT id FROM chats WHERE id=:id""", {'id': sender_id})
        return True if check.fetchone() else False

    def __del__(self):
        """ close the connection """
        self.conn.close()
