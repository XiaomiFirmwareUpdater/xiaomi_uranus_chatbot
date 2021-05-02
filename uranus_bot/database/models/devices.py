from sqlalchemy import Column, Integer, String

from .. import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device = Column(String)

    def __repr__(self):
        return f"<Device(id={self.id}, device={self.device})>"
