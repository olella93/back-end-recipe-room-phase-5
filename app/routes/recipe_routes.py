from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from app.models.recipe import Recipe
from app.models.rating import Rating
from app.models.group_member import GroupMember
from app.extensions import db
from app.utils.cloudinary_upload import upload_recipe_image
# from app.schemas.recipe_schema import RecipeSchema

recipe_bp = Blueprint('recipe', __name__)

# ------------------ GET GROUP RECIPES ------------------ #
@recipe_bp.route('/groups/<int:group_id>/recipes', methods=['GET'])
@jwt_required()
def get_group_recipes(group_id):
    """Get all recipes shared in a specific group"""
    user_id = int(get_jwt_identity())
    
    # Verify user is a member of the group
    member = GroupMember.query.filter_by(user_id=user_id, group_id=group_id).first()
    if not member:
        return jsonify({"error": "You must be a member of this group to view its recipes"}), 403
    
    recipes = Recipe.query.filter_by(group_id=group_id).all()
    
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
            "user_id": recipe.user_id,
            "group_id": recipe.group_id
        })
    
    return jsonify({
        "group_id": group_id,
        "recipe_count": len(result),
        "recipes": result
    }), 200

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
            "user_id": recipe.user_id,
            "group_id": recipe.group_id
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
        # If group_id is provided, validate user is member of that group
        group_id = data.get('group_id')
        if group_id:
            member = GroupMember.query.filter_by(user_id=user_id, group_id=group_id).first()
            if not member:
                return jsonify({"error": "You must be a member of the group to share recipes there"}), 403

        new_recipe = Recipe(
            title=data['title'],
            description=data['description'],
            ingredients=data['ingredients'],
            instructions=data['instructions'],
            country=data.get('country'),
            image_url=data.get('image_url'),
            serving_size=data.get('serving_size'),
            group_id=group_id,
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

    # Get current user id if JWT is present
    user_id = None
    try:
        user_id = int(get_jwt_identity())
    except Exception:
        pass

    # Calculate average rating
    ratings = Rating.query.filter_by(recipe_id=recipe_id).all()
    average_rating = round(sum(r.value for r in ratings) / len(ratings), 2) if ratings else None

    # Get current user's rating
    user_rating = None
    if user_id:
        user_rating_obj = Rating.query.filter_by(recipe_id=recipe_id, user_id=user_id).first()
        if user_rating_obj:
            user_rating = user_rating_obj.value

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
        "user_id": recipe.user_id,
        "group_id": recipe.group_id,
        "average_rating": average_rating,
        "user_rating": user_rating
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
    
    # If updating group_id, validate user is member of that group
    new_group_id = data.get('group_id')
    if new_group_id is not None and new_group_id != recipe.group_id:
        if new_group_id != 0:  
            member = GroupMember.query.filter_by(user_id=user_id, group_id=new_group_id).first()
            if not member:
                return jsonify({"error": "You must be a member of the group to share recipes there"}), 403
    
    recipe.title = data.get('title', recipe.title)
    recipe.description = data.get('description', recipe.description)
    recipe.ingredients = data.get('ingredients', recipe.ingredients)
    recipe.instructions = data.get('instructions', recipe.instructions)
    recipe.country = data.get('country', recipe.country)
    recipe.image_url = data.get('image_url', recipe.image_url)
    recipe.serving_size = data.get('serving_size', recipe.serving_size)
    
    # Handle group_id update (including removal)
    if 'group_id' in data:
        recipe.group_id = data['group_id'] if data['group_id'] != 0 else None 

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

# ------------------ UPLOAD RECIPE IMAGE ------------------ #
@recipe_bp.route('/recipes/<int:recipe_id>/upload-image', methods=['POST'])
@jwt_required()
def upload_recipe_image_endpoint(recipe_id):
    """Upload an image for a recipe"""
    user_id = int(get_jwt_identity())
    recipe = Recipe.query.get_or_404(recipe_id)
    
    # Check if user owns this recipe
    if recipe.user_id != user_id:
        return jsonify({"error": "Unauthorized - You can only upload images to your own recipes"}), 403
    
    # Check if file is present in request
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    file = request.files['image']
    
    if not file or file.filename == '':
        return jsonify({"error": "No image file selected"}), 400
    
    try:
        # Upload to Cloudinary
        success, result = upload_recipe_image(file, user_id, recipe.title)
        
        if not success:
            return jsonify({"error": result}), 400
        
        # Update recipe's image URL
        recipe.image_url = result['url']
        db.session.commit()
        
        return jsonify({
            "message": "Recipe image uploaded successfully",
            "image_url": result['url'],
            "upload_details": {
                "width": result.get('width'),
                "height": result.get('height'),
                "format": result.get('format'),
                "size_bytes": result.get('bytes')
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

# ------------------ SEARCH RECIPES ------------------ #
@recipe_bp.route('/recipes/search', methods=['GET'])
def search_recipes():
    query_param = request.args.get('query', '').strip()

    if not query_param:
        return jsonify({"error": "Search query parameter is required"}), 400

    results = Recipe.query.filter(
        or_(
            Recipe.title.ilike(f"%{query_param}%"),
            Recipe.description.ilike(f"%{query_param}%"),
            Recipe.ingredients.ilike(f"%{query_param}%")
        )
    ).all()

    # Manual serialization to match other endpoints
    result = []
    for recipe in results:
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
            "user_id": recipe.user_id,
            "group_id": recipe.group_id
        })

    return jsonify({
        "query": query_param,
        "result_count": len(result),
        "recipes": result
    }), 200