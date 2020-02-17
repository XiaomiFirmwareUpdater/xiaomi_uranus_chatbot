""" Xiaomi Geeks Bot Database class"""
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
        except Error as err:
            print(err)
        finally:
            self.conn.commit()

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
        return bool(check.fetchone())

    def add_subscription(self, sender_info, sub_type, device):
        """ Add new subscription"""
        if self.is_subscribed(sender_info["id"], sub_type, device):
            return False
        try:
            self.cursor.execute(f"""INSERT INTO subscriptions (id, chat_type, sub_type, device)
            VALUES(:id, :chat_type, :sub_type, :device)""",
                                {'id': sender_info["id"],
                                 'chat_type': sender_info["type"],
                                 'sub_type': sub_type,
                                 'device': device})
            return True
        except Error as err:
            print(err)
        finally:
            self.conn.commit()

    def is_subscribed(self, sender_id, sub_type, device):
        """ Check if user is already subscribed """
        check = self.cursor \
            .execute("""SELECT * FROM subscriptions WHERE id=:id 
            AND sub_type=:sub_type AND device=:device""",
                     {'id': sender_id, 'sub_type': sub_type, 'device': device})
        return bool(check.fetchone())

    def remove_subscription(self, sender_info, sub_type, device):
        """ Remove user subscription """
        try:
            self.cursor \
                .execute("""DELETE FROM subscriptions WHERE id=:id AND sub_type=:sub_type 
                AND device=:device""",
                         {'id': sender_info["id"], 'sub_type': sub_type, 'device': device})
        except Error as err:
            print(err)
        finally:
            self.conn.commit()

    def get_subscriptions(self, sub_type, device):
        """ Get subscriptions list of a user """
        check = self.cursor \
            .execute("""SELECT id FROM subscriptions WHERE sub_type=:sub_type AND device=:device""",
                     {'sub_type': sub_type, 'device': device})
        return check.fetchall()

    def get_stats(self):
        """ Get stats of the bot """
        groups = self.cursor.execute("""SELECT COUNT(id) FROM chats WHERE type='group'""").fetchone()[0]
        channels = self.cursor.execute("""SELECT COUNT(id) FROM chats WHERE type='channel'""").fetchone()[0]
        users = self.cursor.execute("""SELECT COUNT(id) FROM chats WHERE type='user'""").fetchone()[0]
        firmware = self.cursor.execute("""SELECT COUNT(id) FROM subscriptions WHERE sub_type='firmware'""").fetchone()[0]
        miui = self.cursor.execute("""SELECT COUNT(id) FROM subscriptions WHERE sub_type='miui'""").fetchone()[0]
        vendor = self.cursor.execute("""SELECT COUNT(id) FROM subscriptions WHERE sub_type='vendor'""").fetchone()[0]
        return {"usage": {"groups": groups, "channels": channels, "users": users},
                "subscriptions": {"firmware": firmware, "miui": miui, "vendor": vendor}}

    def __del__(self):
        """ close the connection """
        self.conn.close()
