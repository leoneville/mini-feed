from datetime import datetime

from factory import db
from main import app
from models import User

with app.app_context():

    ## CRIAR UM USUARIO
    # Criamos um objeto da classe User e passamos as informações que queremos
    user = User(
        username="drumsticks",
        email="drumsticks@gmail.com",
        birthdate=datetime.fromisoformat("1998-01-22"),
    )

    # Adicionamos user em uma sessão com o banco de dados
    db.session.add(user)

    # Enviamos as informações ao banco de dados
    db.session.commit()
###############################################################


    ## LER DADOS   
    user = User.query.first()

    print(user)

    users = User.query.all()
    print(users)

    user = User.query.filter_by(username="leoneville").first()
    print(user)

    user = db.session.get(User, 1)
    print(user)

    users = User.query.order_by(User.birthdate).first()
    print(users)

    users = User.query.order_by(User.birthdate.desc()).first()
    print(users)
###############################################################


    ## MODIFICAR UM USUARIO
    # Obtemos o usuário que queremos modificar
    user = db.session.get(User, 1)

    # Atualizamos seu email
    user.email = "leonardo.guimaraes@gmail.com"

    # Atualizamos sua data de nascimento
    user.birthdate = datetime.fromisoformat("1997-04-24")

    # Enviamos as mudanças ao banco de dados
    db.session.commit()
###############################################################   

    # DELETANDO O USUARIO
    # Obtendo o usuário que queremos deletar
    user = db.session.get(User, 2)

    # Adicionamos a remoção em uma sessão
    db.session.delete(user)

    # Enviamos as mudanças ao banco de dados
    db.session.commit()
