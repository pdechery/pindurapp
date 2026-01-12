from datetime import datetime, timezone, timedelta

from typing import List, Optional

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pindurapp import db

time_now_utc = datetime.now(timezone(timedelta(hours=-3)))


class Bills(db.Model):
    __tablename__ = "bills"
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"), primary_key=True)
    bar_id: Mapped[int] = mapped_column(ForeignKey("bar.id"), primary_key=True)
    bill: Mapped[float]
    bar: Mapped["Bar"] = relationship(back_populates="bills")
    client: Mapped["Client"] = relationship(back_populates="bills")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=time_now_utc)

    def __repr__(self) -> str:
        return f"Bills(bill={self.bill!r})"


class Client(db.Model): 
    __tablename__ = "client"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    bills: Mapped[List["Bills"]] = relationship(back_populates="client", cascade="all, delete")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=time_now_utc)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=time_now_utc)
    
    def __repr__(self) -> str:
        return f"Client(id={self.id!r}, name={self.name!r})"


class Bar(db.Model):
    __tablename__ = "bar"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    bills: Mapped[List["Bills"]] = relationship(back_populates="bar")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=time_now_utc)
    
    def __repr__(self) -> str:
        return f"Bar(id={self.id!r}, name={self.name!r})"

