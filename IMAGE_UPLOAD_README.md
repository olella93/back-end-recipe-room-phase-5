# Recipe Room - Image Upload Feature

## Overview

Recipe Room now supports image uploads for both user profiles and recipes using Cloudinary for secure, optimized image storage and delivery.

## Features

### ✅ Profile Image Upload
- Upload and update user profile pictures
- Automatic image optimization and resizing (400x400px)
- Face-detection cropping for profile images
- Format optimization (WebP, auto quality)

### ✅ Recipe Image Upload
- Upload images for recipes
- Automatic resizing (800x600px) and optimization
- Support for multiple image formats
- Owner-only upload restrictions

### 🔧 Image Management
- Cloudinary integration for cloud storage
- Automatic format conversion for web optimization
- Image validation (file type, size limits)
- Secure upload with authentication

## Setup Instructions

### 1. Cloudinary Account Setup

1. **Create a Cloudinary account** at [cloudinary.com](https://cloudinary.com)
2. **Get your credentials** from the Dashboard:
   - Cloud Name
   - API Key  
   - API Secret

### 2. Environment Configuration

Add your Cloudinary credentials to the `.env` file:

```env
# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name_here
CLOUDINARY_API_KEY=your_api_key_here
CLOUDINARY_API_SECRET=your_api_secret_here
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The following packages are required:
- `cloudinary` - Cloudinary Python SDK
- `requests` - For testing (optional)

## API Endpoints

### Profile Image Upload

**Upload Profile Image**
```http
POST /api/auth/upload-profile-image
Authorization: Bearer <jwt_token>
Content-Type: multipart/form-data

Body: 
- image: <image_file>
```

**Response:**
```json
{
  "message": "Profile image uploaded successfully",
  "profile_image": "https://res.cloudinary.com/...",
  "upload_details": {
    "width": 400,
    "height": 400,
    "format": "jpg",
    "size_bytes": 25648
  }
}
```

### Recipe Image Upload

**Upload Recipe Image**
```http
POST /api/recipes/{recipe_id}/upload-image
Authorization: Bearer <jwt_token>
Content-Type: multipart/form-data

Body:
- image: <image_file>
```

**Response:**
```json
{
  "message": "Recipe image uploaded successfully",
  "image_url": "https://res.cloudinary.com/...",
  "upload_details": {
    "width": 800,
    "height": 600,
    "format": "jpg",
    "size_bytes": 87432
  }
}
```

### Profile Management

**Get User Profile**
```http
GET /api/auth/profile
Authorization: Bearer <jwt_token>
```

**Update User Profile**
```http
PUT /api/auth/profile
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "username": "new_username",
  "email": "new_email@example.com"
}
```

## File Requirements

### Supported Formats
- **Images**: PNG, JPG, JPEG, GIF, WebP
- **Max File Size**: 5MB per image
- **Max Request Size**: 16MB total

### Automatic Processing

**Profile Images:**
- Resized to 400x400 pixels
- Cropped with face detection when possible
- Optimized quality and format

**Recipe Images:**
- Resized to 800x600 pixels
- Maintained aspect ratio with crop fill
- Optimized for web delivery

## Testing

### Using the Test Script

1. **Add a test image** to the project root (name it `test_image.jpg`)
2. **Set up Cloudinary credentials** in `.env`
3. **Start the Flask server**:
   ```bash
   python run.py
   ```
4. **Run the test script**:
   ```bash
   python test_image_uploads.py
   ```

### Manual Testing with curl

**Upload Profile Image:**
```bash
# First, login to get token
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# Upload profile image
curl -X POST http://localhost:5001/api/auth/upload-profile-image \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "image=@path/to/your/image.jpg"
```

**Upload Recipe Image:**
```bash
# Upload recipe image (replace {recipe_id} with actual ID)
curl -X POST http://localhost:5001/api/recipes/{recipe_id}/upload-image \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "image=@path/to/your/recipe_image.jpg"
```

## Error Handling

### Common Errors

**File Validation Errors:**
```json
{
  "error": "File type not allowed. Allowed types: png, jpg, jpeg, gif, webp"
}
```

**Size Limit Errors:**
```json
{
  "error": "File size too large. Maximum size is 5MB"
}
```

**Authentication Errors:**
```json
{
  "error": "Unauthorized - You can only upload images to your own recipes"
}
```

**Upload Errors:**
```json
{
  "error": "Upload failed: Invalid file format"
}
```

## Security Features

1. **JWT Authentication** - All upload endpoints require valid JWT tokens
2. **File Validation** - Strict file type and size validation
3. **Owner Authorization** - Users can only upload to their own recipes
4. **Secure Naming** - Unique filenames prevent conflicts and exposure
5. **Cloud Storage** - Images stored securely on Cloudinary, not local server

## Database Schema

The image URLs are stored in the existing database fields:

**Users Table:**
- `profile_image` (VARCHAR(255)) - Cloudinary URL for profile image

**Recipes Table:**
- `image_url` (VARCHAR(255)) - Cloudinary URL for recipe image

## Integration Notes

- **Frontend Integration**: The API returns direct Cloudinary URLs that can be used immediately in `<img>` tags
- **Image Optimization**: All images are automatically optimized for web delivery
- **CDN Delivery**: Images are served via Cloudinary's global CDN for fast loading
- **Responsive Images**: Cloudinary URLs support on-the-fly transformations for responsive design

## Future Enhancements

- [ ] Multiple images per recipe
- [ ] Image galleries and carousels
- [ ] Bulk image upload
- [ ] Image deletion/replacement
- [ ] Advanced image transformations
- [ ] Image moderation and content filtering
