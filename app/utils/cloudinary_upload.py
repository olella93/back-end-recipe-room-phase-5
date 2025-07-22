import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.utils import cloudinary_url
import os
from werkzeug.utils import secure_filename
import uuid

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image_file(file):
    """Validate the uploaded image file"""
    if not file or file.filename == '':
        return False, "No file selected"
    
    if not allowed_file(file.filename):
        return False, f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
    
    # Check file size 
    file.seek(0, 2) 
    file_length = file.tell()
    file.seek(0)  
    
    if file_length > MAX_FILE_SIZE:
        return False, "File size too large. Maximum size is 5MB"
    
    return True, "Valid file"

def upload_profile_image(file, user_id):
    """Upload a profile image to Cloudinary"""
    try:
        # Validate file
        is_valid, message = validate_image_file(file)
        if not is_valid:
            return False, message
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"profile_{user_id}_{uuid.uuid4().hex}_{filename}"
        
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            file,
            public_id=f"recipe_room/profiles/{unique_filename}",
            folder="recipe_room/profiles",
            transformation=[
                {'width': 400, 'height': 400, 'crop': 'fill', 'gravity': 'face'},
                {'quality': 'auto', 'fetch_format': 'auto'}
            ],
            allowed_formats=['jpg', 'png', 'jpeg', 'gif', 'webp']
        )
        
        return True, {
            'url': upload_result['secure_url'],
            'public_id': upload_result['public_id'],
            'width': upload_result.get('width'),
            'height': upload_result.get('height'),
            'format': upload_result.get('format'),
            'bytes': upload_result.get('bytes')
        }
        
    except Exception as e:
        return False, f"Upload failed: {str(e)}"

def upload_recipe_image(file, user_id, recipe_title=""):
    """Upload a recipe image to Cloudinary"""
    try:
        # Validate file
        is_valid, message = validate_image_file(file)
        if not is_valid:
            return False, message
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        safe_title = secure_filename(recipe_title[:30]) if recipe_title else "recipe"
        unique_filename = f"recipe_{user_id}_{safe_title}_{uuid.uuid4().hex}_{filename}"
        
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            file,
            public_id=f"recipe_room/recipes/{unique_filename}",
            folder="recipe_room/recipes",
            transformation=[
                {'width': 800, 'height': 600, 'crop': 'fill'},
                {'quality': 'auto', 'fetch_format': 'auto'}
            ],
            allowed_formats=['jpg', 'png', 'jpeg', 'gif', 'webp']
        )
        
        return True, {
            'url': upload_result['secure_url'],
            'public_id': upload_result['public_id'],
            'width': upload_result.get('width'),
            'height': upload_result.get('height'),
            'format': upload_result.get('format'),
            'bytes': upload_result.get('bytes')
        }
        
    except Exception as e:
        return False, f"Upload failed: {str(e)}"

def delete_image(public_id):
    """Delete an image from Cloudinary"""
    try:
        result = cloudinary.uploader.destroy(public_id)
        if result.get('result') == 'ok':
            return True, "Image deleted successfully"
        else:
            return False, f"Failed to delete image: {result.get('result')}"
    except Exception as e:
        return False, f"Delete failed: {str(e)}"

def get_optimized_url(public_id, transformation=None):
   
    try:
        if transformation:
            url, _ = cloudinary_url(public_id, **transformation)
        else:
            url, _ = cloudinary_url(public_id, quality="auto", fetch_format="auto")
        return url
    except Exception as e:
        return None
