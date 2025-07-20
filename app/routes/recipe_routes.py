from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.recipe import Recipe
from app.models.rating import Rating
from app.db import db

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/recipes', methods=['GET'])
def get_recipes():
    country = request.args.get('country')
    min_rating = request.args.get('min_rating', type=float)
    serving_size = request.args.get('serving_size', type=int)

    query = Recipe.query

    if country:
        query = query.filter(Recipe.country == country)

    if min_rating:
        query = query.join(Rating).group_by(Recipe.id).having(db.func.avg(Rating.value) >= min_rating)

    if serving_size:
        query = query.filter(Recipe.serving_size == serving_size)

    recipes = query.all()

    result = []
    for recipe in recipes:
        result.append({
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "ingredients": recipe.ingredients,
            "instructions": recipe.instructions,
            "country": recipe.country,
            "serving_size": recipe.serving_size,
            "image_url": recipe.image_url,
            "created_at": recipe.created_at,
            "updated_at": recipe.updated_at,
            "user_id": recipe.user_id
            # "group_id": recipe.group_id  # Temporarily commented out
        })

    return jsonify(result), 200

@recipe_bp.route('/recipes', methods=['POST'])
@jwt_required()
def create_recipe():
    user_id = get_jwt_identity()
    data = request.get_json()

    required_fields = ['title', 'description', 'ingredients', 'instructions']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        new_recipe = Recipe(
            title=data['title'],
            description=data['description'],
            ingredients=data['ingredients'],
            instructions=data['instructions'],
            country=data.get('country'),
            image_url=data.get('image_url'),
            serving_size=data.get('serving_size'),
            # group_id=data.get('group_id'),  # Temporarily commented out
            user_id=user_id
        )

        db.session.add(new_recipe)
        db.session.commit()

        return jsonify({
            "message": "Recipe created successfully",
            "recipe_id": new_recipe.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
