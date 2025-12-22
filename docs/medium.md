## API REST básica com Flask, SQL Alchemy e Postgres

Para criar APIs com Python, Flask é uma ótima opção pelo seu conceito de "microframework". Basicamente isso significa que além da camada que lida com as requisições HTTP todo o resto é com você.

Isso, além de tornar seu projeto mais leve em termos de dependências, também nos obriga a aprender  mais sobre o ecossistema do Python. Que é aonde entra o SQL Alchemy, uma já antigo e popular pacote para comunicação com Bancos de Dados relacionais.

Para criar uma API bem simples utilizando essas duas librarias, tive a idéia de representar Bares, Clientes e Contas, daí vindo o nome Pindurapp.

Sem mais delongas, vamos às definições.

OBS: Desenvolvi todo este projeto em ambiente Linux/Debian e por esse motivo todas as explicações irão usar comandos do Bash, como `cd`, `ls`, etc

### Modelos

Antes de pensar em código, o primeiro passo foi definir as entidades do meu sistema. 

Como explicado acima, minha idéia foi representar Bares, Clientes e Contas. Meus modelos portanto ficaram assim.

*Clientes*
	- nome
	- bares

*Bares*
	- nome
	- clientes

*Contas*
	- cliente
	- bar
	- valor da conta

Isso, pra quem já entende algo sobre bancos de dados relacionais, é um exemplo clássico de um relacionamento do tipo `Many To Many`, o qual irá usar uma tabela associativa (ou pivô) para representar as Contas.

O diferencial aqui é que a tabela Contas, além de integrar Bares com Clientes também irá carregar uma informação nova, que é o valor da conta.

Em bom português, para tentar traduzir o relacionamento criado aqui, poderia tentar exprimir como:

Clientes podem ir a múltiplos Bares e terem Contas nesses bares.

Bares, por sua vez, também podem ter múltiplos Clientes com suas respectivas contas.

Partindo deste conceito bem simplista, vamos aos modelos do SQL Alchemy.

### SQL Alchemy

O SQL Alchemy é um projeto antigo que já conta com dez (verificar) anos de vida. Foi um dos pioneiros a possibilitar o uso de ORMs no Python e pode conectar com uma série de bancos como MySQL e Postgres.

Neste exemplo iremos utilizar o Postgres.

### Mapped Column

O conceito central no ORM (Object Relational Mapping) é o "mapeamento" entre banco de dados e Classes. 

O SQL Alchemy propõe para isso o uso de duas APIs, que são o Mapped e o mapped_column.

Vamos para o exemplo já montado para em seguida discutir os conceitos.

```
class Bills(db.Model):
    __tablename__ = "bills"
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id"), primary_key=True)
    bar_id: Mapped[int] = mapped_column(ForeignKey("bar.id"), primary_key=True)
    bill: Mapped[float]
    bars: Mapped["Bar"] = relationship(back_populates="clients")
    clients: Mapped["Client"] = relationship(back_populates="bills")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=time_now_utc)


class Client(db.Model): 
    __tablename__ = "client"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    bills: Mapped[List["Bills"]] = relationship(back_populates="clients", cascade="all, delete")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=time_now_utc)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=time_now_utc)
    
    def __repr__(self) -> str:
        return f"Client(id={self.id!r}, name={self.name!r})"

 
class Bar(db.Model):
    __tablename__ = "bar"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    clients: Mapped[List["Bills"]] = relationship(back_populates="bars")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=time_now_utc)
    
    def __repr__(self) -> str:
        return f"Bar(id={self.id!r}, name={self.name!r})"
```

OBS: Estou partindo do princípio que o leitor sabe realizar a devida importação da biblioteca e dos membros da sua API que estão sendo usados aqui.

Aqui vemos a definição de três classes distintas: Bills, Client e Bar. Contas, Clientes e Bares em inglês.

Todas essas classes são filhas da classe pai db.Model, que por hora não precisamos pensar muito a respeito, mas apenas saber que ela representa o classe do SQL Alchemy, que será responsável por trazer todos os recursos da biblioteca para as nossas classes-filhas.

Logo em seguida, vemos que a primeira linha de cada classe é uma variável especial chamada "__tablename__". Esta variável vem de db.Model é ela irá definir o nome de nossas tabelas, quando as mesmas forem criadas no banco (afinal é para isso que estamos definindo essas classes/modelos).

Nos demais atributos podemos ver que se repete o padrão `nome do atributo: Mapped[] = mapped_column()`. 

O Mapped é um "tipo" especial do SQL Alchemy que irá ajudar a definir o tipo da sua coluna no banco de dados. O exemplo mais óbvio é para "id", que é um inteiro, e por isso vai levar um `Mapped[int]`.

O uso de tipos no Python já é bem comum e possui inclusive uma biblioteca dedicada a isso, que é o Typing (link aqui).

Vale salientar que esses tipos não tem poder de controlar o código, já que o Python é uma linguagem dinâmica e não-tipada. Mas eles ajudam na organização dos projetos e na legibilidade do código. Além de usos como o SQL Alchemy, que vamos discutir aqui.

O `Mapped` pode conter os tipos mais elementares do Python, como `int` e `str`, mas também tipos como `List["Bills"]`. Este no caso é uma lista de instâncias de classe Bill.

Para conhecer todos os tipos suportados pelo SQL Alchemy visite: ----

O que vale a pena entender aqui é que o SQL Alchemy propõe uma integração entre tipos e a função `mapped_column` para definir todos os atributos de uma coluna no banco de dados. As colunas podem ter diversos atributos para além do tipo em si. O `mapped_column` é o local onde você deve declarar em dealhes todos esses atributos.

Uma vez criados esses "modelos", vamos precisar que os mesmos se transforme em tabelas dentro de um banco de dados Postgres. Mas para fazer essa mágica toda acontecer vamos precisar dar uns passos para trás e abordar a instalação do nosso projeto com o Flask e demais dependências.

### Instalando Flask e dependências

O primeiro passo é definir um diretório de sua preferência aonde será montado todo o projeto. Como o nome deste projeto é Pindurapp vamos chamar esse diretório também de "pindurapp".

Dentro dele iremos criar um ambiente virtual para isolarmos nossas dependências do resto do nosso sistema.

```
makedir pindurapp
cd pindurapp
python -m venv venv
```
Criado o diretório vamos instalar o Flask e as demais dependências. Lembrando que para trabalhar com o Postgres no Python será necessária a biblioteca `psycog`

```
pip install Flask, SQLAlchemy, psycog, outras
```

Caso você tenha problemas ao instalar o psycog examine a mensagem de erro do PIP. Normalmente isso acontece porque seu sistema não possui os pacotes tal e tal.

Se a mensagem de erro indicar isso simplemente instale essas bibliotecas:

```
apt install bibliotecas
```

##### Configurando o Flask

O Flask além de se autodenominar um "microframework" tem uma filosofia mais livre em relação a como você deve montar seu projeto.

Isso é bem diferente de outros frameworks como Django, onde toda a estrutura já é pré-definida pelo framework.

Neste projeto em especial eu adotei o conceito de aplicação como pacote, ou Package. Isto simplesmente significa que nosso app será considerado para o Python um pacote. Vamos entender isso melhor mais à frente.

Dentro da pasta do projeto, vamos criar a seguinte estrutura de diretórios.

```
pindurapp
	- pindurapp
		__init__.py
		- helpers
		- views
		models.py
		settings.py
	requirements.tx0t
```

Dentro da pasta temos uma pasta com o mesmo nome, que é onde irão ficar todos os módulos python relativos ao código de nossa API. 

Além disso, na raiz dessa pasta podemos ter arquivos como o `requirements.txt` , do PIP, entre outros.

### Módulos e pacotes

Se você tem experiência com o Python saberá que Módulos e Pacotes são formas distintas e fundamentais para a organização do código. Módulos são análogos a arquivos e Pacotes representam os diretórios onde ficam esses arquivos.

Dentro de seu código ambos são importáveis pelos seus respectivos nomes, com a ressalva de que Pacotes e módulos são separados por um ponto "."

Para que um diretório seja reconhecido como Pacote no Python, podendo ser importado, precisamos criar um arquivo chamado `__init__.py` dentro dele.

Essa explicação bem superficial foi necessária para que possamos entender a maneira como estamos montando este aplicação. 

Dentro do arquivo `__init__.py` iremos "criar" nosso app, o que no Flask consiste na instanciação da classe Flask.

### Flask App

A criação do nosso app está descrita nas linhas abaixo:

```
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('pindurapp.settings.DefaultSettings')
app.config.from_pyfile('instance_settings.py')

db = SQLAlchemy(app)

@app.route("/")
def home():
    return render_template("index.html")
```

Nessas linhas já acontece o básico necessário para o Pindurapp existir. 

Primeiramente importamos tudo que é necessário, como o SQLAlchemy, aqui vindo do pacote `flask_sqlalchemy` que traz algumas facilidades para a integração do SQL Alchemy com o Flask.

Logo em seguida instanciamos a classe Flask na variável "app", que passará a representar nossa aplicação, lidando com os requests, criando rotas e tudo mais.

Para mais detalhes sobre o classe Flask, recomendo a documentação oficial: ___

Em seguida, e também de igual importância, é a instanciação da mencionada classe SQLAlchemy na variável "db". Note como essa classe necessita do objeto Flask.

A variável "db" será nossa ponte de comunicação com o SQLAlchemy, para toda e qualquer transação com o nosso banco de dados, que ainda não foi criado.

#### Criando o banco de dados

Como já temos o "db" e os modelos, não é preciso mais nada para criar o banco de dados. 

Ah sim, claro, precisamos instalar o Postgres em nosso sistema :-)

Nesse projeto eu utilizei uma imagem do Docker para isso, e executo o container com a ajuda do docker-compose.

`docker compose postgres up -d`

Você irá precisar informar a sua aplicação aonde encontrar o banco de dados e o modo como fiz isso foi através da variável de ambiente SQLALCHEMY_DATABASE_URI. Essa variável é usada pelo pacote flask_sqlalchemy. Basta atribuir um valor a ela que esse valor será lido automaticamente pelo SQLAlchemy.

`SQLALCHEMY_DATABASE_URI = `

Somente inclua a variável e o valor nas configurações do Flask, definidas na linha abaixo:

```
app.config.from_object('pindurapp.settings.DefaultSettings')
```

Com o banco rodando e a conexão configurada aí sim podemos criar nosso banco.

Para isso, tudo que você precisa é da variável "db" que contém todos os métodos e propriedades do SQLAlchemy e executar o método `db.create_all()`

Isto pode ser feito de várias formas, uma delas é usar o comando `flask shell`, que lhe dará uma shell com todas as variáveis do seu app já carregadas. Experimente!

No meu caso, eu preferi usar o método "cli" do próprio Flask, que cria comandos prontos pra serem executados no terminal, de uma forma muito simples.

```
@app.cli.command("create-db")
def create_db():
  db.create_all()
```

Para executar então, basta:

`flask --app pindurapp create_db` 

#### Populando

As tabelas foram então criadas, e você pode inspecionar tudo de várias formas. Eu sugiro instalar o PgAdmin, que traz uma interface bacana e permite várias operações de uma maneira facilitada.

Ou você pode usar o shell do Postgres diretamente em seu container:

`docker exec -it pindurapp-postgres-1 psql -U postgres`

Aqui eu vou partir do princíṕio que você já seja familiarizado com contâineres. Se não for o caso, mande um comentário ;-)

Ainda temos um pequeno problema que é o fato das tabelas estarem vazias. Ou seja um Banco sem Dados. O objeto do SQLAlchemy que criamos oferece todas as operações possíveis no nosso banco, e entre elas claro que está o insert.





