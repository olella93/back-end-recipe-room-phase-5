# Recipe Room - Entity Relationship Diagram (ERD)

## Database Schema Overview

This document describes the database schema for the Recipe Room application, including all entities, attributes, and relationships.

## Current Implementation Status
- ✅ **Implemented and Active**: Users, Recipes, Ratings, Groups, GroupMembers
- ✅ **New Feature**: Group Recipe Sharing (recipes can be shared in groups via group_id)
- ❌ **Planned/Empty**: Comments, Bookmarks

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

### 6. **Comments** Table ❌ PLANNED
**Purpose**: Store user comments on recipes

*Note: This table is planned but not yet implemented*

**Proposed Schema**:
```sql
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    content TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);
```

---

### 7. **Bookmarks** Table ❌ PLANNED
**Purpose**: Store user bookmarks/favorites for recipes

*Note: This table is planned but not yet implemented*

**Proposed Schema**:
```sql
CREATE TABLE bookmarks (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(id),
    UNIQUE KEY unique_bookmark (user_id, recipe_id)
);
```

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
                          └─────────────────┘

┌─────────────────┐       ┌─────────────────┐
│     GROUPS      │       │ GROUP_MEMBERS   │
├─────────────────┤       ├─────────────────┤
│ 🔑 id (PK)       │───┐   │ 🔑 id (PK)       │
│ name            │   │   │ 🔗 user_id (FK)  │──┐
│ description     │   │   │ 🔗 group_id (FK) │  │
│ created_at      │   │   │ is_admin        │  │
└─────────────────┘   └──▶│ joined_at       │  │
                          └─────────────────┘  │
                                               │
                          ┌─────────────────┐  │
                          │     USERS       │◀─┘
                          │ (same as above) │
                          └─────────────────┘

📝 PLANNED TABLES (Not Yet Implemented):
┌─────────────────┐       ┌─────────────────┐
│    COMMENTS     │       │   BOOKMARKS     │
├─────────────────┤       ├─────────────────┤
│ 🔑 id (PK)       │       │ 🔑 id (PK)       │
│ content         │       │ 🔗 user_id (FK)  │
│ 🔗 user_id (FK)  │       │ 🔗 recipe_id (FK)│
│ 🔗 recipe_id (FK)│       │ created_at      │
│ created_at      │       └─────────────────┘
│ updated_at      │
└─────────────────┘
```

## Key Relationships Summary

1. **Users → Recipes**: One-to-Many (A user can create multiple recipes)
2. **Users → Ratings**: One-to-Many (A user can rate multiple recipes)
3. **Recipes → Ratings**: One-to-Many (A recipe can have multiple ratings)
4. **Users ↔ Groups**: Many-to-Many via GroupMembers (Users can join multiple groups)
5. **Groups → Recipes**: One-to-Many (Groups can have multiple shared recipes) ✅ NEW
6. **Users → Comments**: One-to-Many (Planned - A user can comment on multiple recipes)
7. **Recipes → Comments**: One-to-Many (Planned - A recipe can have multiple comments)
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

## Future Development

### Planned Features:
1. **Comments System** - Users can comment on recipes
2. **Bookmark/Favorites** - Users can save favorite recipes
3. **Group Functionality** - Recipe sharing within groups
4. **Advanced Search** - Full-text search across recipes
5. **Recipe Collections** - Users can create themed recipe collections
6. **Image Management** - Bulk image operations and gallery views

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
