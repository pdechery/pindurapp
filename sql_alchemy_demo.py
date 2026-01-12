from sqlalchemy import ForeignKey, String, DateTime, create_engine, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, DeclarativeBase

from typing import List, Optional

class Base(DeclarativeBase):
    pass

class Client(Base): 
    __tablename__ = "client"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    bills: Mapped[List["Bills"]] = relationship(back_populates="client", cascade="all, delete")

    def __repr__(self) -> str:
        return f"Client(name={self.name!r})"

class Bar(Base):
    __tablename__ = "bar"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    bills: Mapped[List["Bills"]] = relationship(back_populates="bar")

    def __repr__(self) -> str:
        return f"Bar(name={self.name!r})"

class Bills(Base):
    __tablename__ = "bills"
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"), primary_key=True)
    bar_id: Mapped[int] = mapped_column(ForeignKey("bar.id"), primary_key=True)
    bill: Mapped[float]
    bar: Mapped["Bar"] = relationship(back_populates="bills")
    client: Mapped["Client"] = relationship(back_populates="bills")

    def __repr__(self) -> str:
        return f"Bills(bill={self.bill!r})"

try:

    print("Criando Cliente")
    cliente = Client(name="Amigo do Zé")
    print(cliente)

    print("Criando Conta!")
    conta = Bills(bill=20.5)

    print("Ligando Conta ao Cliente")
    cliente.bills.append(conta)

    print("Vendo Conta")
    print(conta)

    print("Vendo Contas do Cliente")
    print(cliente.bills)

    # print("Vendo Cliente da Conta - back populated")
    # print(conta.client)

    print("Criando Bar")
    bar = Bar(name="Bar do Zé")

    print("Ligando Bar à Conta")
    conta.bar = bar
    print(conta.bar)

    print("Vendo Bar do Cliente")
    print(cliente.bills[0].bar.name)

    print("Vendo Cliente da Conta")
    print(conta.client.name)

    print("Vendo Contas do Bar - back populated")
    print(bar.bills)

except Exception as e:

    print(type(e))

    print(e.code)
    
    print(e)










