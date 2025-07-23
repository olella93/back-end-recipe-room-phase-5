from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.comment import Comment
from app.schemas.comment_schema import CommentSchema

comment_bp = Blueprint('comments', __name__, url_prefix='/api/comments')

comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)

@comment_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment():
    data = request.get_json()
    user_id = int(get_jwt_identity())

    if not data or not data.get('text') or not data.get('recipe_id'):
        return jsonify({
            "error": "Both 'text' and 'recipe_id' are required"
        }), 400

    new_comment = Comment(
        text=data['text'],
        user_id=user_id,
        recipe_id=data['recipe_id']
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify(comment_schema.dump(new_comment)), 201

@comment_bp.route('/<int:recipe_id>', methods=['GET'])
def get_comments_for_recipe(recipe_id):
    comments = Comment.query.filter_by(recipe_id=recipe_id).all()
    return jsonify(comments_schema.dump(comments)), 200

@comment_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    user_id = int(get_jwt_identity())
    comment = Comment.query.get_or_404(comment_id)

    if comment.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted'}), 200

@comment_bp.route('/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    data = request.get_json()
    user_id = int(get_jwt_identity())
    comment = Comment.query.get_or_404(comment_id)

    if comment.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    if not data or not data.get('text'):
        return jsonify({'error': "'text' field is required for update"}), 400

    comment.text = data['text']
    db.session.commit()

    return jsonify(comment_schema.dump(comment)), 200
