from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.bookmark import Bookmark
from app.models.recipe import Recipe
from app.schemas.bookmark_schema import BookmarkSchema

bookmark_bp = Blueprint('bookmarks', __name__)
bookmark_schema = BookmarkSchema()
bookmark_list_schema = BookmarkSchema(many=True)

@bookmark_bp.route('/bookmarks', methods=['POST'])
@jwt_required()
def create_bookmark():
    data = request.get_json()
    user_id = int(get_jwt_identity())
    recipe_id = data.get('recipe_id')

    if not recipe_id:
        return jsonify({"error": "Missing recipe_id"}), 400

    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    existing = Bookmark.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if existing:
        return jsonify({"error": "Recipe already bookmarked"}), 400

    bookmark = Bookmark(user_id=user_id, recipe_id=recipe_id)
    db.session.add(bookmark)
    db.session.commit()
    return bookmark_schema.jsonify(bookmark), 201


@bookmark_bp.route('/bookmarks', methods=['GET'])
@jwt_required()
def get_user_bookmarks():
    user_id = int(get_jwt_identity())
    bookmarks = Bookmark.query.filter_by(user_id=user_id).all()
    return bookmark_list_schema.jsonify(bookmarks), 200


@bookmark_bp.route('/bookmarks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_bookmark(id):
    user_id = int(get_jwt_identity())
    bookmark = Bookmark.query.get_or_404(id)

    if bookmark.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(bookmark)
    db.session.commit()
    return jsonify({"message": "Bookmark deleted"}), 200
