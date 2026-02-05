# HBnB - User Stories (Stage 3)

## User Stories - MoSCoW Prioritization

### Must Have (M)

| ID | User Story | Acceptance Criteria |
|----|------------|---------------------|
| US-01 | As a visitor, I want to register an account, so that I can access the platform | Email validation, password hashing, unique email |
| US-02 | As a user, I want to login with my credentials, so that I can access my account | JWT token generation, secure authentication |
| US-03 | As a user, I want to view all available places, so that I can find rentals | List all places with details |
| US-04 | As a user, I want to view place details, so that I can see full information | Display title, description, price, amenities, reviews |
| US-05 | As an owner, I want to create a new place listing, so that I can rent my property | Authenticated, title/description/price required |
| US-06 | As a user, I want to leave a review on a place, so that I can share my experience | Rating 1-5, text review, authenticated |
| US-07 | As an admin, I want to manage users, so that I can maintain the platform | Create/update users, admin-only access |

### Should Have (S)

| ID | User Story | Acceptance Criteria |
|----|------------|---------------------|
| US-08 | As an owner, I want to update my place listing, so that I can modify information | Only owner can update their places |
| US-09 | As a user, I want to filter places by price, so that I can find affordable options | Price filter on listing page |
| US-10 | As a user, I want to see place amenities, so that I can check available features | Display amenities list per place |
| US-11 | As an admin, I want to manage amenities, so that I can add new options | CRUD operations on amenities |

### Could Have (C)

| ID | User Story | Acceptance Criteria |
|----|------------|---------------------|
| US-12 | As a user, I want to update my review, so that I can modify my feedback | Only review author can update |
| US-13 | As a user, I want to delete my review, so that I can remove my feedback | Only review author can delete |
| US-14 | As a user, I want to see average rating, so that I can quickly assess places | Calculate and display average |

### Won't Have (W) - Future Features

| ID | User Story |
|----|------------|
| US-15 | As a user, I want to book a place for specific dates |
| US-16 | As a user, I want to pay online for my booking |
| US-17 | As a user, I want to receive email notifications |

---

## Detailed User Stories

### US-01: User Registration

**As a** visitor
**I want to** register an account
**So that** I can access the platform features

**Acceptance Criteria:**
- User provides first_name, last_name, email, password
- Email must be valid format and unique
- Password must be minimum 6 characters
- Password is hashed before storage
- System returns user details (without password)

---

### US-02: User Login

**As a** registered user
**I want to** login with my credentials
**So that** I can access my account

**Acceptance Criteria:**
- User provides email and password
- System verifies credentials
- On success, JWT token is returned
- Token expires after 1 hour
- Invalid credentials return 401 error

---

### US-03: View All Places

**As a** user (authenticated or not)
**I want to** view all available places
**So that** I can browse rental options

**Acceptance Criteria:**
- Display list of all places
- Show title, price, location for each
- No authentication required

---

### US-04: View Place Details

**As a** user
**I want to** view complete place details
**So that** I can make an informed decision

**Acceptance Criteria:**
- Display all place information
- Show owner details
- List all amenities
- Display all reviews with ratings

---

### US-05: Create Place Listing

**As an** authenticated owner
**I want to** create a new place listing
**So that** I can rent my property

**Acceptance Criteria:**
- User must be authenticated
- Required: title, description, price, latitude, longitude
- Price must be positive
- Coordinates must be valid GPS values
- Owner is set to current user

---

### US-06: Leave Review

**As an** authenticated user
**I want to** leave a review on a place
**So that** I can share my experience

**Acceptance Criteria:**
- User must be authenticated
- Rating must be between 1 and 5
- Text review is required
- User cannot review their own place
- Review is linked to user and place
