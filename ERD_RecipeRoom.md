# Recipe Room - Entity Relationship Diagram (ERD)

## Database Schema Overview

This document describes the database schema for the Recipe Room application, including all entities, attributes, and relationships.

## Current Implementation Status
- ✅ **Implemented and Active**: Users, Recipes, Ratings, Groups, GroupMembers, Comments, Bookmarks
- ✅ **New Feature**: Group Recipe Sharing (recipes can be shared in groups via group_id)
- ✅ **New Feature**: Comments System (users can comment on recipes)
- ✅ **New Feature**: Bookmarks System (users can bookmark/favorite recipes)

---

## Entities and Relationships

### 1. **Users** Table
**Purpose**: Store user account information and authentication data

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier |
| username | VARCHAR(80) | UNIQUE, NOT NULL | User's display name |
| email | VARCHAR(100) | UNIQUE, NOT NULL | User's email address |
| password_hash | TEXT | NOT NULL | Hashed password for security |
| profile_image | VARCHAR(255) | NULLABLE | URL to user's profile image (Cloudinary) |
| created_at | DATETIME | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |

**Relationships**:
- One-to-Many with Recipes (users.id → recipes.user_id)
- One-to-Many with Ratings (users.id → ratings.user_id)
- One-to-Many with GroupMembers (users.id → group_members.user_id)
- One-to-Many with Comments (users.id → comments.user_id)

---

### 2. **Recipes** Table ✅ ACTIVE
**Purpose**: Store recipe information and cooking instructions

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique recipe identifier |
| title | VARCHAR(100) | NOT NULL | Recipe name/title |
| description | TEXT | NOT NULL | Brief recipe description |
| ingredients | TEXT | NOT NULL | List of required ingredients |
| instructions | TEXT | NOT NULL | Step-by-step cooking instructions |
| country | VARCHAR(50) | NULLABLE | Country/cuisine origin |
| image_url | VARCHAR(255) | NULLABLE | URL to recipe image (Cloudinary) |
| serving_size | INTEGER | NULLABLE | Number of servings |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Recipe creation timestamp |
| updated_at | DATETIME | DEFAULT CURRENT_TIMESTAMP, ON UPDATE | Last modification timestamp |
| user_id | INTEGER | FOREIGN KEY (users.id), NOT NULL | Recipe creator |
| group_id | INTEGER | FOREIGN KEY (groups.id), NULLABLE | Group where recipe is shared (optional) |

**Relationships**:
- Many-to-One with Users (recipes.user_id → users.id)
- Many-to-One with Groups (recipes.group_id → groups.id) - OPTIONAL
- One-to-Many with Ratings (recipes.id → ratings.recipe_id)
- One-to-Many with Comments (recipes.id → comments.recipe_id)

---

### 3. **Ratings** Table ✅ ACTIVE
**Purpose**: Store user ratings for recipes (1-5 stars)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique rating identifier |
| value | INTEGER | NOT NULL | Rating value (1-5) |
| user_id | INTEGER | FOREIGN KEY (users.id), NOT NULL | User who gave the rating |
| recipe_id | INTEGER | FOREIGN KEY (recipes.id), NOT NULL | Recipe being rated |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Rating creation timestamp |

**Relationships**:
- Many-to-One with Users (ratings.user_id → users.id)
- Many-to-One with Recipes (ratings.recipe_id → recipes.id)

**Business Rules**:
- One rating per user per recipe (unique constraint on user_id + recipe_id)
- Rating values must be between 1-5

---

### 4. **Groups** Table ✅ ACTIVE
**Purpose**: Store cooking/recipe groups for community features

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique group identifier |
| name | VARCHAR(100) | NOT NULL | Group name |
| description | TEXT | NULLABLE | Group description/purpose |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Group creation timestamp |

**Relationships**:
- One-to-Many with GroupMembers (groups.id → group_members.group_id)
- One-to-Many with Recipes (groups.id → recipes.group_id) - OPTIONAL

---

### 5. **GroupMembers** Table ✅ ACTIVE
**Purpose**: Junction table for Users and Groups (many-to-many relationship)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique membership identifier |
| user_id | INTEGER | FOREIGN KEY (users.id), NOT NULL | Member user |
| group_id | INTEGER | FOREIGN KEY (groups.id), NOT NULL | Group being joined |
| is_admin | BOOLEAN | DEFAULT FALSE | Admin privileges flag |
| joined_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Membership creation timestamp |

**Relationships**:
- Many-to-One with Users (group_members.user_id → users.id)
- Many-to-One with Groups (group_members.group_id → groups.id)

**Business Rules**:
- One membership per user per group (unique constraint on user_id + group_id)

---

### 6. **Comments** Table ✅ ACTIVE
**Purpose**: Store user comments on recipes

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique comment identifier |
| text | TEXT | NOT NULL | Comment content/message |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Comment creation timestamp |
| user_id | INTEGER | FOREIGN KEY (users.id), NOT NULL | User who wrote the comment |
| recipe_id | INTEGER | FOREIGN KEY (recipes.id), NOT NULL | Recipe being commented on |

**Relationships**:
- Many-to-One with Users (comments.user_id → users.id)
- Many-to-One with Recipes (comments.recipe_id → recipes.id)

**Business Rules**:
- Users can comment multiple times on the same recipe
- Comments can be updated and deleted by their owner
- JWT authentication required for create/update/delete operations

---

### 7. **Bookmarks** Table ✅ ACTIVE
**Purpose**: Store user bookmarks/favorites for recipes

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique bookmark identifier |
| user_id | INTEGER | FOREIGN KEY (users.id), NOT NULL | User who bookmarked the recipe |
| recipe_id | INTEGER | FOREIGN KEY (recipes.id), NOT NULL | Recipe being bookmarked |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Bookmark creation timestamp |

**Relationships**:
- Many-to-One with Users (bookmarks.user_id → users.id)
- Many-to-One with Recipes (bookmarks.recipe_id → recipes.id)

**Business Rules**:
- One bookmark per user per recipe (unique constraint on user_id + recipe_id)
- Users can bookmark multiple recipes
- Users can only bookmark each recipe once (duplicate prevention)

---

## Visual ERD Representation

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     USERS       │       │    RECIPES      │       │    RATINGS      │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ 🔑 id (PK)       │───┐   │ 🔑 id (PK)       │───┐   │ 🔑 id (PK)       │
│ username        │   │   │ title           │   │   │ value           │
│ email           │   │   │ description     │   │   │ 🔗 user_id (FK)  │
│ password_hash   │   │   │ ingredients     │   │   │ 🔗 recipe_id (FK)│
│ profile_image   │   │   │ instructions    │   │   │ created_at      │
│ created_at      │   │   │ country         │   │   └─────────────────┘
└─────────────────┘   │   │ image_url       │   │            │
                      │   │ serving_size    │   │            │
                      │   │ created_at      │   │            │
                      │   │ updated_at      │   │            │
                      └──▶│ 🔗 user_id (FK)  │   └────────────┘
                          │ 🔗 group_id (FK) │
                          └─────────────────┘
                                    │
                          ┌─────────▼─────────┐
                          │    COMMENTS      │
                          ├─────────────────┤
                          │ 🔑 id (PK)       │
                          │ text            │
                          │ 🔗 user_id (FK)  │──┐
                          │ 🔗 recipe_id (FK)│  │
                          │ created_at      │  │
                          └─────────────────┘  │
                                               │
┌─────────────────┐       ┌─────────────────┐  │
│     GROUPS      │       │ GROUP_MEMBERS   │  │
├─────────────────┤       ├─────────────────┤  │
│ 🔑 id (PK)       │───┐   │ 🔑 id (PK)       │  │
│ name            │   │   │ 🔗 user_id (FK)  │──┼──┘
│ description     │   │   │ 🔗 group_id (FK) │  │
│ created_at      │   │   │ is_admin        │  │
└─────────────────┘   └──▶│ joined_at       │  │
        │                 └─────────────────┘  │
        │                                      │
        └──────────────────────────────────────┘

📝 ALL CORE FEATURES IMPLEMENTED ✅

Current Status: All planned core features are now implemented and active:
- Users with profile management ✅
- Recipes with CRUD operations ✅  
- Ratings system ✅
- Groups with membership management ✅
- Comments system ✅
- Bookmarks/favorites system ✅
- Image uploads (Cloudinary) ✅
- Search functionality ✅
```

## Key Relationships Summary

1. **Users → Recipes**: One-to-Many (A user can create multiple recipes)
2. **Users → Ratings**: One-to-Many (A user can rate multiple recipes)
3. **Recipes → Ratings**: One-to-Many (A recipe can have multiple ratings)
4. **Users ↔ Groups**: Many-to-Many via GroupMembers (Users can join multiple groups)
5. **Groups → Recipes**: One-to-Many (Groups can have multiple shared recipes)
6. **Users → Comments**: One-to-Many (A user can comment on multiple recipes)
7. **Recipes → Comments**: One-to-Many (A recipe can have multiple comments) 
8. **Users ↔ Recipes**: Many-to-Many via Bookmarks (Planned - Users can bookmark multiple recipes)

## API Endpoints Currently Implemented

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/upload-profile-image` - Upload profile image (requires authentication)
- `PUT /api/auth/profile` - Update user profile (requires authentication)
- `GET /api/auth/profile` - Get current user profile (requires authentication)

### Recipes
- `GET /api/recipes` - Get all recipes (with filtering, includes group_id)
- `POST /api/recipes` - Create new recipe (supports group_id for sharing in groups)
- `GET /api/recipes/<id>` - Get single recipe (includes group_id)
- `PUT /api/recipes/<id>` - Update recipe (supports moving between groups)
- `DELETE /api/recipes/<id>` - Delete recipe
- `POST /api/recipes/<id>/upload-image` - Upload recipe image (requires authentication)
- `GET /api/groups/<id>/recipes` - Get recipes shared in a specific group (requires group membership)

### Ratings
- `POST /api/recipes/<id>/rate` - Rate a recipe

### Groups
- `GET /api/groups` - Get all groups
- `POST /api/groups` - Create new group
- `GET /api/groups/<id>` - Get single group with members
- `PUT /api/groups/<id>` - Update group (admin only)
- `DELETE /api/groups/<id>` - Delete group (admin only)
- `POST /api/groups/<id>/join` - Join a group
- `DELETE /api/groups/<id>/leave` - Leave a group
- `PUT /api/groups/<id>/members/<user_id>/admin` - Promote/demote member (admin only)
- `DELETE /api/groups/<id>/members/<user_id>` - Remove member (admin only)
- `GET /api/my-groups` - Get current user's groups

### Comments
- `POST /api/comments/` - Create new comment (requires authentication)
- `GET /api/comments/<recipe_id>` - Get all comments for a recipe
- `PUT /api/comments/<comment_id>` - Update comment (owner only)
- `DELETE /api/comments/<comment_id>` - Delete comment (owner only)

### Bookmarks
- `POST /api/bookmarks` - Create new bookmark (requires authentication)
- `GET /api/bookmarks` - Get current user's bookmarks (requires authentication)
- `DELETE /api/bookmarks/<id>` - Delete bookmark (owner only)

### Search
- `GET /api/recipes/search?query=<term>` - Search recipes by title, description, or ingredients

## Future Development

### Optional Enhancement Ideas:
1. **Advanced Search** - Full-text search with filters (cuisine, difficulty, time)
2. **Recipe Collections** - Users can create themed recipe collections
3. **Enhanced Comments** - Reply to comments, comment threading
4. **Recipe Rating Analytics** - Average ratings, rating distributions
5. **Recipe Sharing** - Direct recipe sharing via links
6. **Nutrition Information** - Add nutritional data to recipes
7. **Recipe Timing** - Add prep time, cook time, total time fields

### Database Improvements:
1. Add indexes for performance optimization
2. Implement soft deletes for data retention
3. Add audit trails for data changes
4. Implement recipe versioning

### Image Management Features:
1. **Cloudinary Integration** - Profile and recipe image uploads
2. **Image Optimization** - Automatic resizing and format optimization
3. **Image Deletion** - Clean up unused images
4. **Image Galleries** - Display multiple images per recipe
