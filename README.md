## Run Flask app
flask --app app run

## DB Commands

flask create-db
flask seed

## Postgres Helper

## Docker run
docker run -v ./db:/var/lib/postgresql/data --env-file .env postgres

### Connect to container's psql
docker exec -it pindurapp-postgres-1 psql -U postgres

### Other useful commands

docker run -it pindurapp bash
docker exec pindurapp-app-1 flask create-db
docker exec pindurapp-app-1 flask seed
curl -i http://172.18.0.3:5000/api/clients

## Flask Helper

### Applications as Packages
https://flask.palletsprojects.com/en/3.0.x/patterns/packages/

### Application Factory
https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/

### Application Context
https://flask.palletsprojects.com/en/3.0.x/appcontext/
https://flask-sqlalchemy.readthedocs.io/en/3.1.x/contexts/

### Inicialização do SQL Alchemy no Flask
https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/

### Relationship no SQL Alchemy
https://docs.sqlalchemy.org/en/20/tutorial/orm_related_objects.html#tutorial-orm-related-objects

### SQL Alchemy Association Object
https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#association-object

### SQL Alchemy Cascade
https://docs.sqlalchemy.org/en/20/orm/cascades.html#cascade-delete-many-to-many

### Class-based Views
https://flask.palletsprojects.com/en/3.0.x/views/
https://flask.palletsprojects.com/en/stable/views/

### JWT com Python
https://pypi.org/project/python-jose/

### Usando Rotas com JWT
https://mateus-dev-me.medium.com/como-criar-uma-api-rest-com-flask-29b6845f1f1c

## Flask Jsonify
https://mateus-dev-me.medium.com/como-criar-uma-api-rest-com-flask-29b6845f1f1c

## Flask Restful
https://flask-restful.readthedocs.io/en/latest/quickstart.html

## Flask CLI
https://stackoverflow.com/questions/57202736/where-should-i-implement-flask-custom-commands-cli

### Padrões de projeto no Github
https://stackoverflow.com/questions/13284858/how-to-share-the-global-app-object-in-flask
https://github.com/tquach/talent-curator/blob/master/talent_curator/database.py
https://github.com/djeada/Flask-Minimal/tree/main
https://gist.github.com/cuibonobo/8696392