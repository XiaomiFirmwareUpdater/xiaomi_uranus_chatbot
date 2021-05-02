from sqlalchemy import Column, Integer, String

from .. import Base


class I18n(Base):
    __tablename__ = "i18n"

    id = Column(Integer, primary_key=True, index=True)
    lang = Column(String)

    def __repr__(self):
        return f"<I18n(id={self.id}, lang={self.lang})>"
