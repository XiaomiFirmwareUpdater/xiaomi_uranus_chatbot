import json
import logging
from sys import path
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql.functions import count

from . import Base
from .models.chat import Chat
from .models.devices import Device
from .models.i18n import I18n
from .models.subscription import Subscription

path.append("..")
from uranus_bot import PARENT_DIR, TG_BOT_DB

logger = logging.getLogger(__name__)

tg_engine = create_engine(f"sqlite+pysqlite:///{PARENT_DIR}/{TG_BOT_DB}",
                          connect_args={'check_same_thread': False})

Base.metadata.create_all(bind=tg_engine)

TGSession = scoped_session(sessionmaker(bind=tg_engine))
tg_session = TGSession()


class Database:
    def __init__(self, session):
        self.session: Session = session

    def is_known_chat(self, sender_id):
        """ Check if user is already in database """
        return bool(self.session.query(Chat).filter(Chat.id == sender_id).first())

    def add_chat_to_db(self, sender_info):
        """ Add new row to the table"""
        if self.is_known_chat(sender_info["id"]):
            return
        try:
            chat = Chat(id=sender_info["id"], username=sender_info["username"],
                        name=sender_info["name"], type=sender_info["type"])
            self.session.add(chat)
        except SQLAlchemyError as err:
            logger.error(f"DB Error while adding a chat to the database:\n{err}\n{sender_info}")
            self.session.rollback()
        finally:
            self.session.commit()

    def get_chats(self, chat_type):
        """ get chats list from  database """
        return self.session.query(Chat).filter(Chat.type == chat_type).all()

    def is_subscribed(self, sender_id, sub_type, device):
        """ Check if user is already subscribed """
        return bool(
            self.session.query(
                Subscription).filter(Subscription.user_id == sender_id).filter(
                Subscription.sub_type == sub_type).filter(Subscription.device == device).first()
        )

    def add_subscription(self, sender_info, sub_type, device):
        """ Add new subscription"""
        if self.is_subscribed(sender_info["id"], sub_type, device):
            return False
        try:
            subscription = Subscription(user_id=sender_info["id"],
                                        chat_type=sender_info["type"],
                                        sub_type=sub_type,
                                        device=device)
            self.session.add(subscription)
        except SQLAlchemyError as err:
            logger.error(f"DB Error while adding a subscription ({sub_type} - {device}):\n{err}\n{sender_info}")
            self.session.rollback()
        finally:
            self.session.commit()
            return True

    def remove_subscription(self, sender_info, sub_type, device):
        """ Remove user subscription """
        try:
            self.session.query(Subscription).filter(
                Subscription.user_id == sender_info["id"]).filter(Subscription.sub_type == sub_type).filter(
                Subscription.device == device).delete()
        except SQLAlchemyError as err:
            logger.error(f"DB Error while removing a subscription ({sub_type} - {device}):\n{err}\n{sender_info}")
            self.session.rollback()
        finally:
            self.session.commit()

    def get_chat_subscriptions(self, chat_id):
        """ Get all subscriptions of a chat """
        if str(chat_id).startswith('-100'):
            chat_id = int(str(chat_id).replace('-100', ''))
        return self.session.query(Subscription).filter(Subscription.user_id == chat_id).all()

    def get_subscriptions(self, sub_type, device):
        """ Get subscriptions list of a user """
        return self.session.query(Subscription).filter(Subscription.sub_type == sub_type).filter(
            Subscription.device == device).all()

    def get_locale(self, chat_id):
        """ Get locale of a chat """
        locale: Optional[I18n] = self.session.query(I18n).filter(I18n.id == chat_id).first()
        return locale.lang if locale else 'en'

    def set_locale(self, chat_id, lang):
        """ Set the locale of a chat """
        try:
            locale: Optional[I18n] = self.session.query(I18n).filter(I18n.id == chat_id).first()
            if locale:
                locale.lang = lang
            else:
                locale = I18n(id=chat_id, lang=lang)
            self.session.add(locale)
        except SQLAlchemyError as err:
            logger.error(f"DB Error while setting locale ({lang}) for a chat ({chat_id}):\n{err}")
            self.session.rollback()
        finally:
            self.session.commit()
            return True

    def get_codename(self, chat_id):
        """ Get preferred device of a chat """
        device: Optional[Device] = self.session.query(Device).filter(Device.id == chat_id).first()
        return device.device if device else None

    def set_codename(self, chat_id, device):
        """ Set the preferred device of a chat """
        try:
            device_: Optional[Device] = self.session.query(Device).filter(Device.id == chat_id).first()
            if device_:
                device_.device = device
            else:
                device_ = Device(id=chat_id, device=device)
            self.session.add(device_)
        except SQLAlchemyError as err:
            logger.error(f"DB Error while setting codename ({device}) for a chat ({chat_id}):\n{err}")
            self.session.rollback()
        finally:
            self.session.commit()
            return True

    # def get_last_updates(self, user_id, sub_type, device):
    #     query = self.session.query(Subscription).filter(Subscription.user_id == user_id).filter(
    #         Subscription.sub_type == sub_type).filter(Subscription.device == device).first()
    #     if query:
    #         return json.loads(query.last_updates)

    def set_last_updates(self, subscription: Subscription, last_update: dict):
        subscription.last_updates = json.dumps(last_update)
        try:
            self.session.commit()
        except (SQLAlchemyError, IntegrityError) as err:
            logger.error(f"DB Error while updating last update ({subscription.sub_type} - {subscription.device})"
                         f" for a chat ({subscription.user_id}):\n{err}")
            self.session.rollback()
        finally:
            return True

    def get_stats(self):
        """ Get stats of the bot """
        groups = self.session.query(count(Chat.id).filter(Chat.type == "group")).first()
        channels = self.session.query(count(Chat.id).filter(Chat.type == "channel")).first()
        users = self.session.query(count(Chat.id).filter(Chat.type == "user")).first()

        firmware = self.session.query(count(Subscription.id).filter(Subscription.sub_type == "firmware")).first()
        miui = self.session.query(count(Subscription.id).filter(Subscription.sub_type == "miui")).first()
        vendor = self.session.query(count(Subscription.id).filter(Subscription.sub_type == "vendor")).first()

        preferred_devices = self.session.query(count(Device.id)).first()
        preferred_languages = self.session.query(count(I18n.id)).first()

        return {"usage": {"groups": groups[0] if groups else 0, "channels": channels[0] if channels else 0,
                          "users": users[0] if users else 0},
                "subscriptions": {"firmware": firmware[0] if firmware else 0, "miui": miui[0] if miui else 0,
                                  "vendor": vendor[0] if vendor else 0},
                "preferred_devices": preferred_devices[0] if preferred_devices else 0,
                "preferred_languages": preferred_languages[0] if preferred_languages else 0}

    def __del__(self):
        """ close the connection """
        self.session.close()
