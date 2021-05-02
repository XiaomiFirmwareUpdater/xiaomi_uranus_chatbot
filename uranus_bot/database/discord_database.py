""" Xiaomi Geeks Discord Bot Database class"""
import logging
from sys import path

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql.functions import count

from . import Base
from .database import Database as TGDatabase
from .models.guild import Guild
from .models.subscription import Subscription

path.append("..")
from uranus_bot import PARENT_DIR, DISCORD_DB

discord_engine = create_engine(f"sqlite+pysqlite:///{PARENT_DIR}/{DISCORD_DB}",
                               connect_args={'check_same_thread': False})

Base.metadata.create_all(bind=discord_engine)

DiscordSession = scoped_session(sessionmaker(bind=discord_engine))
discord_session = DiscordSession()

logger = logging.getLogger(__name__)


class Database(TGDatabase):
    def __init__(self, db):
        super().__init__(db)

    def is_known_chat(self, sender_id):
        """ Check if user is already in database """
        return bool(self.session.query(Guild).filter(Guild.id == sender_id).first())

    def add_chat_to_db(self, sender_info):
        """ Add new row to the table"""
        if self.is_known_chat(sender_info["id"]):
            return
        try:
            chat = Guild(id=sender_info["id"], name=sender_info["name"],
                         guild_name=sender_info["guild_name"], guild_id=sender_info["guild_id"],
                         type=sender_info["type"])
            self.session.add(chat)
        except SQLAlchemyError as err:
            logger.error(f"DB Error while adding a chat to the database:\n{err}\n{sender_info}")
            self.session.rollback()
        finally:
            self.session.commit()

    def get_chats(self, chat_type):
        """ get chats list from  database """
        return self.session.query(Guild).filter(Guild.type == chat_type).all()

    def get_stats(self):
        """ Get stats of the bot """
        miui = self.session.query(count(Subscription.id).filter(Subscription.sub_type == "miui")).first()
        firmware = self.session.query(count(Subscription.id).filter(Subscription.sub_type == "firmware")).first()
        vendor = self.session.query(count(Subscription.id).filter(Subscription.sub_type == "vendor")).first()

        users = self.session.query(count(Guild.id).filter(Guild.type == "user")).first()
        groups = self.session.query(count(Guild.id).filter(Guild.type == "group")).first()
        channels = self.session.query(count(Guild.id).filter(Guild.type == "channel")).first()

        return {"usage": {
            "groups": groups[0] if groups else 0,
            "channels": channels[0] if channels else 0,
            "users": users[0] if users else 0
        },
            "subscriptions": {
                "firmware": firmware[0] if firmware else 0,
                "miui": miui[0] if miui else 0,
                "vendor": vendor[0] if vendor else 0
            },
            "preferred_devices": 0,
            "preferred_languages": 0
        }
