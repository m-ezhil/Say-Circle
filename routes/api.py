from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models import get_all_posts, add_post, update_post_by_id, delete_post_by_id, get_comments_by_post_id, add_comment, update_comment_by_id, delete_comment_by_id

api = Blueprint('api',__name__)

@api.route('/posts', methods=['GET', 'POST'])
@jwt_required()
def posts():
    posts = get_all_posts()
    return jsonify(posts=posts), 200

@api.route('/post', methods=['POST','PATCH','DELETE'])
@jwt_required()
def post():
    post_id = request.json.get('post_id')
    user_id = request.json.get('user_id')
    title = request.json.get('title')
    content = request.json.get('content')

    if request.method == 'POST':
        if not user_id or not title or not content:
            return jsonify(massage='All fields are required: user id, title and content'), 400
        
        post = add_post(title, content, user_id)
        return jsonify(massage='Post successfully added.', post=post), 200

    if request.method == 'PATCH':
        if not post_id or (not title and not content): 
            return jsonify(massage='All fields are required: post id, title or content'), 400
        
        post = update_post_by_id(post_id, title, content)
        return jsonify(massage='Post successfully updated.', post=post), 200
    
    if request.method == 'DELETE':
        if not post_id: 
            return jsonify(massage='All fields are required: post id'), 400
        post = delete_post_by_id(post_id)
        return jsonify(massage='Post successfully deleted.', post=post), 200

@api.route('/comments')
@jwt_required()
def comments():
    post_id = request.json.get('post_id')
    if not post_id:
        return jsonify(massage='All fields are required: post id'), 400
    comments = get_comments_by_post_id(post_id)
    return jsonify(comments=comments), 200

@api.route('/comment', methods=['POST', 'PATCH', 'DELETE'])
@jwt_required()
def comment():
    post_id = request.json.get('post_id')
    user_id = request.json.get('user_id')
    comment = request.json.get('comment')
    comment_id = request.json.get('comment_id')

    if request.method == 'POST':
        if not post_id or not user_id or not comment:
            return jsonify(massage='All fields are required: content, user id, post id'), 400
        
        new_comment = add_comment(comment, post_id, user_id)
        return jsonify(massage='Comment successfully added.', comment=new_comment), 200
    
    if request.method == 'PATCH':
        if not comment_id or not comment:
            return jsonify(massage='All fields are required: content id, comment'), 400

        updated_comment = update_comment_by_id(comment_id, comment)
        massage = 'Comment successfully updated.' if updated_comment else 'Comment is not available.'
        return jsonify(massage=massage, comment=updated_comment), 200
    
    if request.method == 'DELETE':
        if not comment_id:
            return jsonify(massage='All fields are required: content id'), 400

        deleted_comment = delete_comment_by_id(comment_id)
        massage = 'Comment successfully deleted.' if deleted_comment else 'Comment is not available.'
        return jsonify(massage=massage, comment=deleted_comment), 200
    