from sqlalchemy import Column, Integer, String

from .. import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    name = Column(String)
    type = Column(String, nullable=False)

    def __repr__(self):
        return f"<Chat(id={self.id}, name={self.name}, type={self.type})>"
