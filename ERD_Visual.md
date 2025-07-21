```mermaid
erDiagram
    USERS {
        int id PK
        varchar username UK "UNIQUE, NOT NULL"
        varchar email UK "UNIQUE, NOT NULL"
        text password_hash "NOT NULL"
        varchar profile_image "NULLABLE"
        datetime created_at "DEFAULT CURRENT_TIMESTAMP"
    }

    RECIPES {
        int id PK
        varchar title "NOT NULL"
        text description "NOT NULL"
        text ingredients "NOT NULL"
        text instructions "NOT NULL"
        varchar country "NULLABLE"
        varchar image_url "NULLABLE"
        int serving_size "NULLABLE"
        datetime created_at "DEFAULT CURRENT_TIMESTAMP"
        datetime updated_at "ON UPDATE CURRENT_TIMESTAMP"
        int user_id FK "NOT NULL"
    }

    RATINGS {
        int id PK
        int value "NOT NULL, 1-5"
        int user_id FK "NOT NULL"
        int recipe_id FK "NOT NULL"
        datetime created_at "DEFAULT CURRENT_TIMESTAMP"
    }

    GROUPS {
        int id PK
        varchar name "NOT NULL"
        text description "NULLABLE"
        datetime created_at "DEFAULT CURRENT_TIMESTAMP"
    }

    GROUP_MEMBERS {
        int id PK
        int user_id FK "NOT NULL"
        int group_id FK "NOT NULL"
        boolean is_admin "DEFAULT FALSE"
        datetime joined_at "DEFAULT CURRENT_TIMESTAMP"
    }

    COMMENTS {
        int id PK
        text content "NOT NULL"
        int user_id FK "NOT NULL"
        int recipe_id FK "NOT NULL"
        datetime created_at "DEFAULT CURRENT_TIMESTAMP"
        datetime updated_at "ON UPDATE CURRENT_TIMESTAMP"
    }

    BOOKMARKS {
        int id PK
        int user_id FK "NOT NULL"
        int recipe_id FK "NOT NULL"
        datetime created_at "DEFAULT CURRENT_TIMESTAMP"
    }

    %% Active Relationships (Implemented)
    USERS ||--o{ RECIPES : "creates"
    USERS ||--o{ RATINGS : "gives"
    RECIPES ||--o{ RATINGS : "receives"
    
    %% Partial Relationships (Models exist)
    USERS ||--o{ GROUP_MEMBERS : "joins"
    GROUPS ||--o{ GROUP_MEMBERS : "has_members"
    
    %% Planned Relationships (Not yet implemented)
    USERS ||--o{ COMMENTS : "writes"
    RECIPES ||--o{ COMMENTS : "has"
    USERS ||--o{ BOOKMARKS : "saves"
    RECIPES ||--o{ BOOKMARKS : "bookmarked_by"

    %% Unique Constraints
    RATINGS ||--|| USERS : "unique_per_user_recipe"
    RATINGS ||--|| RECIPES : "unique_per_user_recipe"
    GROUP_MEMBERS ||--|| USERS : "unique_membership"
    GROUP_MEMBERS ||--|| GROUPS : "unique_membership"
    BOOKMARKS ||--|| USERS : "unique_bookmark"
    BOOKMARKS ||--|| RECIPES : "unique_bookmark"
```

## Implementation Status Legend

| Symbol | Status | Description |
|--------|---------|-------------|
| ✅ | **Active** | Fully implemented and tested |
| 🟡 | **Partial** | Models exist but not fully utilized |
| ❌ | **Planned** | Not yet implemented |

## Current Database Tables

### ✅ Active Tables
- **users** - User accounts and authentication
- **recipes** - Recipe storage and management  
- **ratings** - Recipe rating system
- **groups** - Group/community structure and management
- **group_members** - Group membership management

### 🟡 Partial Tables  
- (none)

### ❌ Planned Tables
- **comments** - Recipe comments (empty file exists)
- **bookmarks** - Recipe favorites (empty file exists)

## Business Rules

1. **Rating Constraints**:
   - One rating per user per recipe
   - Rating values: 1-5 stars only
   - Users cannot rate their own recipes (not enforced yet)

2. **Recipe Ownership**:
   - Only recipe creators can update/delete their recipes
   - All users can view all recipes
   - All authenticated users can rate recipes

3. **Group Management**:
   - Users can join multiple groups
   - Groups can have multiple admin users
   - Unique membership per user per group
   - Only group admins can update group details
   - Only group admins can remove members
   - Only group admins can promote/demote other members
   - Group creators are automatically admins

4. **Authentication**:
   - Unique usernames and emails required
   - Password hashing with PBKDF2-SHA256
   - JWT tokens for API authentication

## API Coverage

### ✅ Implemented Endpoints
- User registration and login
- Full Recipe CRUD operations
- Recipe rating system  
- Recipe filtering (country, rating, serving size)
- Full Group CRUD operations
- Group membership management (join, leave, admin promotion/demotion)
- Group member management (remove members)

### 🟡 Partially Available
- (none)

### ❌ Not Yet Implemented  
- Comments API
- Bookmarks API
- User profile management
