from datetime import datetime

from factory import db
from main import app

from models import Post, User

def cria_postagem():
    # Carrega usuário
    user = User.query.filter_by(username="leoneville.dev").first()

    # Cria postagem
    post = Post(
        text="To aprendendo a criar apis com python e flask",
        author_id = user.id
    )

    db.session.add(post)
    db.session.commit()


def cria_postagem_backref_author():
    user = User.query.filter_by(username="leoneville.dev").first()

    post = Post(
        text="também estou aprendendo banco de dados com sqlalchemy :D",
        author = user
    )

    db.session.add(post)
    db.session.commit()


def carregando_postagens():
    # Retorna a primeira postagem
    post = Post.query.first()

    # Imprime nome campo "username" do objeto "author"
    print(f"Author: {post.author.username}")

    # Imprime texto do objeto Post
    print(f"Text: {post.text}")

    # Imprime data de criação
    print(f"Created at: {post.created_at}")


def get_postagem_por_usuario():
    user = User.query.filter_by(username="leoneville.dev").first()

    # Without lazy="dynamic" in user.db.relationship
    # for post in user.posts:
    #     print(post.text)

    # With lazy="dynamic" in user.db.relationship
    print(user.posts)
    print(user.posts.all())
    print(user.posts.first())
    print(user.posts.order_by(Post.id.desc()).all())


def filter_by_ilike():
    posts = Post.query.filter(Post.text.ilike(f"%apre%"))
    print(posts.all())


def get_paginate():
    posts_pagination = Post.query.paginate(page=1, per_page=5)
    print(posts_pagination)
    print(posts_pagination.items) # retorna a lista de objetos Post da página consultada
    print(posts_pagination.total) # retorna o total de postagens de todas as páginas


def post_order_by_desc():
    posts = Post.query.order_by(Post.created_at.desc())
    print(posts)
    print(posts.all())
    print(posts.first())


with app.app_context():
    # cria_postagem()
    # cria_postagem_backref_author()
    # carregando_postagens()
    # get_postagem_por_usuario()
    # filter_by_ilike()
    # get_paginate()
    post_order_by_desc()


