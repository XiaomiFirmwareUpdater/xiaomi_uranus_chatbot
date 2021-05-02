from sqlalchemy import Column, Integer, String

from .. import Base


class Guild(Base):
    __tablename__ = "guilds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String, nullable=False)
    guild_id = Column(Integer)
    guild_name = Column(String)

    def __repr__(self):
        return f"<Chat(id={self.id}, guild_name={self.guild_name}, type={self.type})>"
