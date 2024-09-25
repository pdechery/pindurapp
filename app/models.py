from typing import List, Optional

from sqlalchemy import ForeignKey, String,Table, Column
from sqlalchemy import create_engine
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db


class Bills(db.Model):
    __tablename__ = "bills"
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"), primary_key=True)
    bar_id: Mapped[int] = mapped_column(ForeignKey("bar.id"), primary_key=True)
    bill: Mapped[float]
    bars: Mapped["Bar"] = relationship(back_populates="clients")
    clients: Mapped["Client"] = relationship(back_populates="bars")


class Client(db.Model): 
    __tablename__ = "client"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    bars: Mapped[List["Bills"]] = relationship(back_populates="clients")
    
    def __repr__(self) -> str:
        return f"Client(id={self.id!r}, name={self.name!r})"


class Bar(db.Model):
    __tablename__ = "bar"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))
    clients: Mapped[List["Bills"]] = relationship(back_populates="bars")
    
    def __repr__(self) -> str:
        return f"Bar(id={self.id!r}, name={self.name!r})"

