# Recipe Room - Backend API

A Flask-based REST API for a recipe sharing and community platform. This project allows users to create, share, and discover recipes while building cooking communities through groups and social features.

## Project Contributors

- **Richard Olella** - Lead Backend Developer
- **Andrew Bariu** - Database Design & API Development  
- **Bill Sebastian** - Database Design & API Development 

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Learning Outcomes](#learning-outcomes)
- [Future Enhancements](#future-enhancements)

## Overview

Recipe Room is a social platform where cooking enthusiasts can share their favorite recipes, rate and comment on others' recipes, and join cooking groups to discover new cuisines. The backend provides a comprehensive REST API that supports user authentication, recipe management, community features, and image uploads.

This project was developed as part of our web development coursework to demonstrate proficiency in:
- RESTful API design and implementation
- Database design and relationships
- User authentication and authorization
- File upload handling
- Testing and documentation

## Features

### Core Functionality
- **User Management**: Registration, login, profile management with JWT authentication
- **Recipe CRUD**: Create, read, update, and delete recipes with images
- **Rating System**: 5-star rating system for recipes
- **Search**: Search recipes by title, description, or ingredients
- **Image Upload**: Profile pictures and recipe images via Cloudinary

### Community Features
- **Groups**: Create and join cooking groups
- **Group Recipe Sharing**: Share recipes within specific groups
- **Comments**: Comment on recipes with full CRUD operations
- **Bookmarks**: Save favorite recipes for later

### Advanced Features
- **Authorization**: Role-based access control for groups (admin/member)
- **Membership Management**: Join/leave groups, promote/demote members
- **Data Validation**: Comprehensive input validation and error handling
- **Migration System**: Database versioning with Alembic

## Technology Stack

- **Backend Framework**: Flask (Python)
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens) with Flask-JWT-Extended
- **Password Security**: Werkzeug password hashing
- **Image Storage**: Cloudinary API
- **Database Migrations**: Alembic
- **Data Serialization**: Marshmallow
- **Environment Management**: python-dotenv
- **HTTP Client**: Requests (for testing)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/olella93/back-end-recipe-room-phase-5.git
   cd back-end-recipe-room-phase-5
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration (see Configuration section)
   ```

## Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///recipe_room.db

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key

# Cloudinary Configuration (for image uploads)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### Important Notes:
- Generate secure random keys for `SECRET_KEY` and `JWT_SECRET_KEY`
- Sign up for a free Cloudinary account for image upload functionality
- Never commit your `.env` file to version control

## Database Setup

1. **Initialize the database**
   ```bash
   flask db init  # Only needed for first-time setup
   ```

2. **Run migrations**
   ```bash
   flask db upgrade
   ```

3. **Create new migrations (when models change)**
   ```bash
   flask db migrate -m "Description of changes"
   flask db upgrade
   ```

## Running the Application

1. **Start the development server**
   ```bash
   python run.py
   ```

2. **The API will be available at:**
   ```
   http://localhost:5003/api
   ```

3. **Health check endpoint:**
   ```
   GET http://localhost:5003/api/health
   ```

## API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get current user profile
- `PUT /api/auth/profile` - Update user profile
- `POST /api/auth/upload-profile-image` - Upload profile image

### Recipe Endpoints
- `GET /api/recipes` - Get all recipes (with optional filters)
- `POST /api/recipes` - Create new recipe
- `GET /api/recipes/{id}` - Get specific recipe
- `PUT /api/recipes/{id}` - Update recipe
- `DELETE /api/recipes/{id}` - Delete recipe
- `POST /api/recipes/{id}/rate` - Rate a recipe
- `POST /api/recipes/{id}/upload-image` - Upload recipe image
- `GET /api/recipes/search?query={term}` - Search recipes

### Group Endpoints
- `GET /api/groups` - Get all groups
- `POST /api/groups` - Create new group
- `GET /api/groups/{id}` - Get group details
- `PUT /api/groups/{id}` - Update group (admin only)
- `DELETE /api/groups/{id}` - Delete group (admin only)
- `POST /api/groups/{id}/join` - Join a group
- `DELETE /api/groups/{id}/leave` - Leave a group
- `GET /api/groups/{id}/recipes` - Get group recipes
- `GET /api/my-groups` - Get current user's groups

### Comment Endpoints
- `POST /api/comments` - Create comment
- `GET /api/comments/{recipe_id}` - Get recipe comments
- `PUT /api/comments/{id}` - Update comment
- `DELETE /api/comments/{id}` - Delete comment

### Bookmark Endpoints
- `POST /api/bookmarks` - Bookmark a recipe
- `GET /api/bookmarks` - Get user's bookmarks
- `DELETE /api/bookmarks/{id}` - Remove bookmark

### Example API Usage

```bash
# Register a new user
curl -X POST http://localhost:5003/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "email": "john@example.com", "password": "password123"}'

# Login and get JWT token
curl -X POST http://localhost:5003/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "johndoe", "password": "password123"}'

# Create a recipe (requires authentication)
curl -X POST http://localhost:5003/api/recipes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"title": "Pasta Carbonara", "description": "Classic Italian pasta", "ingredients": "Pasta, eggs, cheese", "instructions": "Cook pasta, mix with eggs and cheese"}'
```

## Testing

We've implemented comprehensive testing to ensure all features work correctly:

### Running Tests

1. **Make sure the server is running**
   ```bash
   python run.py
   ```

2. **Run all tests**
   ```bash
   python run_tests.py
   ```

3. **Run individual tests**
   ```bash
   python tests/test_bookmarks.py
   python tests/test_comments.py
   python tests/test_groups.py
   ```

### Test Categories

- **Authentication Tests**: User registration, login, profile management
- **Recipe Tests**: CRUD operations, search functionality
- **Group Tests**: Group creation, membership, recipe sharing
- **Comment Tests**: Comment CRUD, authorization
- **Bookmark Tests**: Bookmark management, duplicate prevention
- **Integration Tests**: End-to-end workflow testing

### Test Coverage

Our test suite covers:
- All API endpoints
- Authentication and authorization
- Error handling and edge cases
- Database relationships
- Business logic validation

## Project Structure

```
back-end-recipe-room-phase-5/
├── app/
│   ├── __init__.py
│   ├── main.py              # Flask app factory
│   ├── config.py            # Configuration settings
│   ├── extensions.py        # Flask extensions
│   ├── db.py               # Database initialization
│   ├── models/             # Database models
│   │   ├── user.py
│   │   ├── recipe.py
│   │   ├── group.py
│   │   ├── rating.py
│   │   ├── comment.py
│   │   └── bookmark.py
│   ├── routes/             # API endpoints
│   │   ├── auth_routes.py
│   │   ├── recipe_routes.py
│   │   ├── group_routes.py
│   │   ├── comment_routes.py
│   │   └── bookmark_routes.py
│   ├── schemas/            # Data serialization
│   │   ├── user_schema.py
│   │   ├── recipe_schema.py
│   │   └── comment_schema.py
│   └── utils/              # Utility functions
│       ├── auth.py
│       ├── decorators.py
│       └── cloudinary_upload.py
├── migrations/             # Database migrations
├── tests/                  # Test files
│   ├── test_auth.py
│   ├── test_recipes.py
│   ├── test_groups.py
│   ├── test_comments.py
│   └── test_bookmarks.py
├── run.py                  # Application entry point
├── run_tests.py           # Test runner
├── requirements.txt        # Python dependencies
├── ERD_RecipeRoom.md      # Database design documentation
└── README.md              # This file
```

## Database Schema

Our application uses a relational database with the following entities:

### Core Tables
- **Users**: User accounts and authentication data
- **Recipes**: Recipe information and cooking instructions
- **Groups**: Cooking communities and groups
- **Ratings**: Recipe ratings (1-5 stars)
- **Comments**: User comments on recipes
- **Bookmarks**: User's saved favorite recipes

### Relationships
- Users can create multiple recipes (One-to-Many)
- Users can join multiple groups (Many-to-Many via GroupMembers)
- Recipes can belong to groups (Many-to-One)
- Users can rate and comment on recipes (One-to-Many)
- Users can bookmark multiple recipes (Many-to-Many)

For detailed database schema information, see [ERD_RecipeRoom.md](ERD_RecipeRoom.md).

## Learning Outcomes

Through this project, we demonstrated understanding of:

### Backend Development
- RESTful API design principles
- HTTP methods and status codes
- Request/response handling
- Error handling and validation

### Database Management
- Entity-Relationship modeling
- Database normalization
- Foreign key relationships
- Migration management

### Security
- Password hashing and storage
- JWT token authentication
- Authorization and access control
- Input sanitization

### Software Engineering
- Code organization and modularity
- Version control with Git
- Testing and quality assurance
- Documentation and README writing

### Tools and Technologies
- Flask framework ecosystem
- SQLAlchemy ORM
- Cloud services (Cloudinary)
- Environment configuration

## Future Enhancements

Potential improvements for future development:

### Features
- **Recipe Collections**: Themed recipe collections
- **Advanced Search**: Filters by cuisine, difficulty, cooking time
- **Social Features**: Follow other users, recipe feeds
- **Nutrition Information**: Calorie and nutrition tracking
- **Meal Planning**: Weekly meal planning features
- **Recipe Scaling**: Automatic ingredient scaling

### Technical Improvements
- **Caching**: Redis for improved performance
- **Pagination**: Large dataset handling
- **Rate Limiting**: API abuse prevention
- **Email Notifications**: User engagement features
- **Mobile API**: Optimized endpoints for mobile apps
- **Analytics**: Usage tracking and reporting

### DevOps
- **Docker**: Containerization for easy deployment
- **CI/CD**: Automated testing and deployment
- **Monitoring**: Application performance monitoring
- **Logging**: Comprehensive logging system

## Troubleshooting

### Common Issues

1. **Database connection errors**
   - Check your DATABASE_URL in .env
   - Ensure migrations are up to date: `flask db upgrade`

2. **Image upload failures**
   - Verify Cloudinary credentials in .env
   - Check internet connection

3. **JWT token errors**
   - Ensure JWT_SECRET_KEY is set in .env
   - Check token expiration (default 1 hour)

4. **Test failures**
   - Make sure the Flask server is running on port 5003
   - Check that all dependencies are installed

### Getting Help

If you encounter issues:
1. Check the error logs in the terminal
2. Verify your .env configuration
3. Ensure all dependencies are installed
4. Review the API documentation for correct usage

---

**Project Status**: ✅ Complete - All planned features implemented and tested

**Academic Year**: 2025

**Course**: Software Development / Backend Development

This project demonstrates our understanding of modern web development practices and serves as a foundation for building scalable web applications.
