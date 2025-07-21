from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.recipe import Recipe
from app.models.rating import Rating
from app.extensions import db

recipe_bp = Blueprint('recipe', __name__)

# ------------------ GET ALL RECIPES ------------------ #
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

# ------------------ CREATE RECIPE ------------------ #
@recipe_bp.route('/recipes', methods=['POST'])
@jwt_required()
def create_recipe():
    user_id = int(get_jwt_identity()) 
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

# ------------------ GET SINGLE RECIPE ------------------ #
@recipe_bp.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_single_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    return jsonify({
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
    }), 200

# ------------------ UPDATE RECIPE ------------------ #
@recipe_bp.route('/recipes/<int:recipe_id>', methods=['PUT'])
@jwt_required()
def update_recipe(recipe_id):
    user_id = int(get_jwt_identity())
    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    recipe.title = data.get('title', recipe.title)
    recipe.description = data.get('description', recipe.description)
    recipe.ingredients = data.get('ingredients', recipe.ingredients)
    recipe.instructions = data.get('instructions', recipe.instructions)
    recipe.country = data.get('country', recipe.country)
    recipe.image_url = data.get('image_url', recipe.image_url)
    recipe.serving_size = data.get('serving_size', recipe.serving_size)
    # recipe.group_id = data.get('group_id', recipe.group_id) 

    db.session.commit()
    return jsonify({"message": "Recipe updated successfully"}), 200

# ------------------ DELETE RECIPE ------------------ #
@recipe_bp.route('/recipes/<int:recipe_id>', methods=['DELETE'])
@jwt_required()
def delete_recipe(recipe_id):
    user_id = int(get_jwt_identity())
    recipe = Recipe.query.get_or_404(recipe_id)

    if recipe.user_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"message": "Recipe deleted successfully"}), 200
# ------------------ RATE RECIPE ------------------ #
@recipe_bp.route('/recipes/<int:recipe_id>/rate', methods=['POST'])
@jwt_required()
def rate_recipe(recipe_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()

    required_fields = ['value']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    recipe = Recipe.query.get_or_404(recipe_id)

    # Check if the user has already rated this recipe
    existing_rating = Rating.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if existing_rating:
        return jsonify({"error": "You have already rated this recipe"}), 400

    new_rating = Rating(
        user_id=user_id,
        recipe_id=recipe_id,
        value=data['value']
    )

    db.session.add(new_rating)
    db.session.commit()

    return jsonify({"message": "Recipe rated successfully"}), 201