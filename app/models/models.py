import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Date, ForeignKey
from app.settings.database import Base


class DocumentsOrm(Base):
    __tablename__ = 'Documents'

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    path: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)

class DocumentsTextOrm(Base):
    __tablename__ = 'Documents_text'

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    id_doc: Mapped[int] = mapped_column(ForeignKey('Documents.id', ondelete='CASCADE'), nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)