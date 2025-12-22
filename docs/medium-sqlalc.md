# Representando relação Many to Many com tabela associativa no SQL Alchemy

Resolvi finalmente estudar um pouco mais a fundo o SQL Alchemy, o famoso pacote do Python que possibilita integração do Python com Bancos de Dados relacionais, opcionalmente através de uma ORM (Object Relational Mapper).

As ORMs, relembrando, possibilitam o mapeamento entre Classes e Tabelas de um banco de dados. Grosso modo, se sua aplicação usa Orientação a Objetos, você pode criar Classes que representarão (e se tornarão de fato) tabelas num banco de dados (MySQL, Postgres etc).

Além disso, usando essas mesmas classes e seus atributos (que agora podemos chamar de "modelos") você pode controlar todas as operações com suas tabelas, como INSERT, UPDATE e DELETE.

Vamos exemplificar isto aqui através de três entidades bem comuns no cotidiano: Clientes, Bares e Contas. 

A relação entre Clientes e Bares seria do tipo "Many to Many", já que:

- Clientes podem "ter" múltiplos Bares
- Bares podem "ter" múltiplos clientes

Relembrando a teoria dos relacionamentos, a relação "Many to Many" prevê que haja uma entidade "Pai" e uma "Filho" e ambas possam ter múltiplos relacionamentos entre si. Para representar isso num banco de dados, uma terceira tabela tem que ser criada, a Tabela Associativa ou Pivô, para persistir a chave primária da entidade "Pai" e da entidade "Filho"  em cada relacionamento.

O gráfico ERD pode ajudar a entender:

![Gráfico ERP](pindurapp/static/erd.png)

Falamos até aqui de Clientes e Bares, mas e as Contas?

As Contas são parte integrante de cada relacionamento entre em Cliente e um Bar e, como no mundo real são Dinheiro, no banco de dados seriam uma coluna do tipo "float" (número com ponto).

É aí que entra o tema central desse artigo. Como inserir dados adicionais numa relação Many To Many - que não pertençam nem ao Pai nem ao Filho, mas à relaçao em si?

Quando a Tabela Associativa traz dados assim, isso é considerado uma variante do "Many to Many" e o SQL Alchemy prevê esse caso [aqui](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#association-object)

Basicamente essa tal variante é denominada "Associative Object" e descrição oferecida na documentação oficial é mais ou menos assim: quando a Tabela Associativa contém colunas adicionais (fora as chaves primárias das entidades Pai e Filho) é necessário que essa tabela seja representada na sua própria classe.

Vamos então primeiro ver como representar essas entidades no Python, usando a API do SQL Alchemy.

```
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List

class Base(DeclarativeBase):
    pass

class Bills(Base):
    __tablename__ = "bills"
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"), primary_key=True)
    bar_id: Mapped[int] = mapped_column(ForeignKey("bar.id"), primary_key=True)
    bill: Mapped[float]
    bars: Mapped["Bar"] = relationship(back_populates="clients")
    clients: Mapped["Client"] = relationship(back_populates="bills")


class Client(Base): 
    __tablename__ = "client"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    bills: Mapped[List["Bills"]] = relationship(back_populates="clients", cascade="all, delete")

 
class Bar(Base):
    __tablename__ = "bar"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    clients: Mapped[List["Bills"]] = relationship(back_populates="bars")

```
O código acima define três classes/modelos, que são:

- Client
- Bills
- Bar

As propriedade de Client e Bar são simplemente o nome ("name"). Já Bills, por ser a Tabela Associativa, possui as chaves estrangeiras de Client e Bar e também a propriedade "bill", que é justamente o valor da conta que falamos acima.

O SQL Alchemy possui uma API algo complexa, onde existem muitas formas de integrar o código Python com o Banco. A solução adotada aqui foi a chamada "Declarativa". Basicamente ela entregará uma ORM e para definir as colunas da tabela é necessário seguir o formato mostrado nos exemplos acima.

aque vai necessitar algumas explicações, que vamos tentar dar agora.

Logo no início podemos ver a criaçao de uma classe `Base` que é uma sub-classe de `DeclarativeBase`. No SQL ALchemy 2.0 a integração com o BD pode ser feita de diversas formas (chamadas formas de "mapeamento") e aqui estamos optando pelo mapeamento estilo "Declarativo", por isso temos que ter a classe `DeclarativeBase` como classe-pai de todos nossos modelos, através de `Base`.

[Documentação oficial](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#orm-declarative-models:~:text=%C2%B6,typing%20support%20using)

[Mapping Styles](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#orm-mapping-styles)

O mapeamento Declarativo consiste num estilo aonde as informações sobre cada coluna de uma tabela são lidas em dois lugares distintos e complementares. No canto esquerdo, através da annotation `Mapped` e no canto direto através da função `mapped_column()`. Essa abordagem, segundo a documentação, é inspirada nas `dataclasses` do Python, que também fazem o uso de `annotations` no canto esquerdo dos elementos da classe.

Em cada uma das três classes apresentadas aqui podemos ver esse padrão em uso, como no exemplo: 

`name: Mapped[str] = mapped_column(String(30), unique=True)`

Aqui, declaramos que a coluna `name` é do tipo `str` (string) e como atributos adicionais informamos que o limite de caracteres é 30 e seu valor tem que ser único na tabela.

A documentação oficial do SQL ALchemy, é claro, detalha todas as possibilidade de valores para os dois elementos.

Cada Classe também, como primeiro atributo, o `__tablename__`, que servirá para nomear a tabela no banco de dados.

O que nos interessa aqui, no entanto, é como o SQL Alchemy vai resolver os relacionamentos entre as entidades e como podemos trabalhar com isso no nosso código Python.

"PARTE RELEVANTE"

Olhando o modelo "Bills", podemos ver os relacionamentos entre Bares e Clientes declarados.

Como num "Many To Many" tradicional, esta é a nossa tabela associativa e vai portanto levar as chaves estrangeiras (FK) de Clients e Bars.

No SQL Alchemy o relacionamento é declarado usando `annotations` (ver)[https://peps.python.org/pep-0484/] em conjunto com a função `relationship`. 

O modelo/classe na qual estamos criando o relacionamento é o valor dentro `Mapped` (como string mesmo) e dentro de `relationship` podemos passar mais parâmetros. No caso estamos fazendo uso do `back_populates`, que vai nos ajudar mais pra frente.

`bars: Mapped["Bar"] = relationship(back_populates="clients")`
`clients: Mapped["Client"] = relationship(back_populates="bills")`

Não é necessário chaves estrangeiras nas outras duas classes/modelos, portanto essas duas linhas acima já servirão para nosso objetivo.

Podemos agora então criar as tabelas e começar a controlá-las através de nossas classes do Python!

Para este exercício você irá precisar - obviamente - ter um banco de dados instalado em seu sistema. Vamos usar o SQLite, que é uma opção mais leve e suficiente para fins de estudo. 

Para seguir o exercício eu recomendo a criação de um diretório com o nome do app, "pindurapp", e nesse diretório crie um arquivo chamado `sa_demo.py`

EM `sa_demo.py` cole o seguinte código:

```
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, create_engine

from typing import List

engine = create_engine("sqlite:///pindurapp.db")

class Base(DeclarativeBase):
    pass

class Bills(Base):
    __tablename__ = "bills"
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"), primary_key=True)
    bar_id: Mapped[int] = mapped_column(ForeignKey("bar.id"), primary_key=True)
    bill: Mapped[float]
    bars: Mapped["Bar"] = relationship(back_populates="clients")
    clients: Mapped["Client"] = relationship(back_populates="bills")


class Client(Base): 
    __tablename__ = "client"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    bills: Mapped[List["Bills"]] = relationship(back_populates="clients", cascade="all, delete")

 
class Bar(Base):
    __tablename__ = "bar"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    clients: Mapped[List["Bills"]] = relationship(back_populates="bars")

Base.metadata.create_all(engine)
```
Este código, além dos modelos que já foram mostrados, traz o `create_engine`, que no SQL Alchemy é quem é responsável pela conexão com o Banco. 

Repare que em `create_engine` estamos passando uma URL que traz informações sobre o tipo de banco que vamos usar, que no caso é SQLite. Veja mais sobre isso (aqui)[https://docs.sqlalchemy.org/en/20/tutorial/engine.html#establishing-connectivity-the-engine]

Em seguida vem a linha 

`Base.metadata.create_all(engine)` 

O `create_all()`, como o nome diz, é quem vai criar de fato nossas tabelas com todas as colunas e suas respectivas descrições.

Uma vez criadas as tabelas nós podemos interagir com elas via script, com nossas Classes e atributos.

Vamos então iniciar criando um Cliente que tem uma Conta num Bar.

Você pode criar outro arquivo ou colocar este script no Python REPL:

```
from sqlalchemy.orm import Session

with Session(engine) as session:
    cliente = Client(name="Amigo do Zé")
    conta = Bills(bill=20.5)
    conta.bars = Bar(name="Bar do Zé")
    cliente.bills.append(conta)

    for b in cliente.bills:
        print(b)
        print(b.bill)
        print(b.bars)
    
    session.add_all([cliente, conta])
    session.commit()
```























