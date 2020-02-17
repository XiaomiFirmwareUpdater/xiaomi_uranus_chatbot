""" Xiaomi Geeks Discord Bot Database class"""
from sqlite3 import Error

from uranus_bot.database.database import Database as TGDatabase


class Database(TGDatabase):
    def __init__(self, db):
        super().__init__(db)

    def add_chat_to_db(self, sender_info):
        """ Add new row to the table"""
        if self.is_known_chat(sender_info["id"]):
            return
        try:
            self.cursor.execute(f"""INSERT INTO chats (id, name, type, guild_id, guild_name)
            VALUES(:id, :name, :type, :guild_id, :guild_name)""",
                                {'id': sender_info["id"],
                                 'name': sender_info["name"],
                                 'type': sender_info["type"],
                                 'guild_id': sender_info["guild_id"],
                                 'guild_name': sender_info["guild_name"]})
        except Error as err:
            print(err)
        finally:
            self.conn.commit()

    def get_subscriptions(self, sub_type, device):
        """ Get subscriptions list of a user """
        check = self.cursor \
            .execute("""SELECT id, chat_type FROM subscriptions WHERE sub_type=:sub_type AND device=:device""",
                     {'sub_type': sub_type, 'device': device})
        return check.fetchall()
