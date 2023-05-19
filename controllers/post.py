from pydantic import BaseModel
import math
import json

from flask import Blueprint, jsonify
from flask.globals import request
from spectree import Response
from flask_jwt_extended import jwt_required, current_user

from factory import db, api
from models import Post, PostCreate, PostResponse, PostResponseList
from utils.responses import DefaultResponse



post_controller = Blueprint("posts_controller", __name__, url_prefix="/posts")


@post_controller.post("/")
@api.validate(json=PostCreate, resp=Response(
    HTTP_201=DefaultResponse, 
    HTTP_500=DefaultResponse), tags=["posts"])
@jwt_required()
def create_post():
    """
    Create a new post
    """
    try:
        data = request.json

        post = Post(
            text=data["text"],
            author_id=current_user.id,
        )

        db.session.add(post)
        db.session.commit()

        return {"msg": f"Post with id {post.id} created."}, 201
    except Exception as error:
        db.session.rollback()
        print(f"<{type(error)} - {error}>")
        return {"msg": "Ops! Something went wrong."}, 500
    

@post_controller.put("/<int:post_id>")
@api.validate(json=PostCreate, resp=Response(
    HTTP_200=DefaultResponse, 
    HTTP_403=DefaultResponse, 
    HTTP_500=DefaultResponse), tags=["posts"])
@jwt_required()
def update(post_id):
    """
    Update a post
    """
    try:
        post = db.session.get(Post, post_id)

        
        if post is None:
            return {"msg": "This post does not exists."}, 404
        
        if post.author_id != current_user.id:
            return {"msg": "You can only change your own posts."}, 403
        
        data = request.json

        post.text = data["text"]

        db.session.commit()

        return {"msg": "The post was updated."}, 200

    except Exception as error:
        db.session.rollback()
        print(f"<{type(error)} - {error}>")
        return {"msg": "Ops! Something went wrong."}, 500
    

@post_controller.delete("/<int:post_id>")
@api.validate(resp=Response(
    HTTP_200=DefaultResponse, 
    HTTP_403=DefaultResponse, 
    HTTP_500=DefaultResponse), tags=["posts"])
@jwt_required()
def delete(post_id):
    """
    Delete a post
    """
    try:
        post = db.session.get(Post, post_id)

        if post is None:
            return {"msg": "This post does not exists."}, 404
        
        if post.author_id != current_user.id:
            return {"msg": "You can only delete your own posts."}, 403
        
        db.session.delete(post)
        db.session.commit()

        return {"msg": "The post was deleted."}, 200

    except Exception as error:
            db.session.rollback()
            print(f"<{type(error)} - {error}>")
            return {"msg": "Ops! Something went wrong."}, 500
    


@post_controller.get("/<int:post_id>")
@api.validate(resp=Response(
    HTTP_200=PostResponse, 
    HTTP_404=DefaultResponse, 
    HTTP_500=DefaultResponse), tags=["posts"])
@jwt_required()
def get_one(post_id):
    """
    Get a post
    """
    try:
        post = db.session.get(Post, post_id)

        if post is None:
            return {"msg": "This post does not exists."}, 404
        
        response = PostResponse.from_orm(post).json()

        return json.loads(response), 200

    except Exception as error:
        print(f"<{type(error)} - {error}>")
        return {"msg": "Ops! Something went wrong."}, 500
    

class SearchModel(BaseModel):
    search: str = ""
    page: int = 1
    reversed: bool = False

POSTS_PER_PAGE = 5    

@post_controller.get("/")
@api.validate(query=SearchModel, resp=Response(HTTP_200=PostResponseList, HTTP_500=DefaultResponse), tags=["posts"])
@jwt_required()
def get_all():
    """
    Get all posts
    """
    try:
        search = request.args.get("search", "")
        page = request.args.get("page", 1)
        reversed = True if request.args.get("reversed", "false") == "true" else False

        posts_query = Post.query.filter(Post.text.ilike(f"%{search}%"))

        if reversed:
            posts_query = posts_query.order_by(Post.created_at.desc())


        posts_paginate = posts_query.paginate(page=page, per_page=POSTS_PER_PAGE)
        total, posts = posts_paginate.total, posts_paginate.item

        response = PostResponseList(
            page=page,
            pages=math.ceil(total / POSTS_PER_PAGE),
            total=total,
            posts=[PostResponse.from_orm(post).dict() for post in posts]
        ).json()

        return jsonify(json.loads(response)), 200
    except Exception as error:
        print(f"<{type(error)} - {error}>")
        return {"msg": "Ops! Something went wrong."}, 500