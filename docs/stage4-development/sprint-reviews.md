# HBnB - Sprint Reviews

## Sprint 1 Review: Core Models & User Authentication

### Date: Week 2

### Sprint Goal
Implement user model with authentication and basic API structure.

### Completed Features

| Feature | Status | Demo |
|---------|--------|------|
| Flask project structure | ✅ Done | Project runs with `python run.py` |
| BaseClass model | ✅ Done | All models inherit id, timestamps |
| User model with SQLAlchemy | ✅ Done | Users persist in database |
| Password hashing (bcrypt) | ✅ Done | Passwords securely stored |
| JWT authentication | ✅ Done | Login returns token |
| User CRUD endpoints | ✅ Done | GET/POST /users working |

### Demo Notes
- Demonstrated user registration via Postman
- Showed JWT token generation on login
- Verified password is hashed in database (not plain text)
- Tested protected endpoint with valid/invalid tokens

### Stakeholder Feedback
- Authentication flow works as expected
- Request to add email validation ✅ Added
- Consider adding admin role ✅ Implemented

---

## Sprint 2 Review: Places & Amenities CRUD

### Date: Week 4

### Sprint Goal
Implement place and amenity models with full CRUD operations.

### Completed Features

| Feature | Status | Demo |
|---------|--------|------|
| Place model | ✅ Done | Places stored with all attributes |
| Place CRUD endpoints | ✅ Done | Create, Read, Update working |
| Owner authentication | ✅ Done | Only owners can modify places |
| Amenity model | ✅ Done | Amenities persist in database |
| Amenity CRUD endpoints | ✅ Done | Full CRUD working |
| Place-Amenity relationship | ✅ Done | Many-to-Many working |

### Demo Notes
- Created a place with authenticated user
- Showed place appears in GET /places list
- Demonstrated adding amenities to a place
- Verified only owner can update their place

### Stakeholder Feedback
- GPS validation appreciated
- Price filtering would be useful ✅ Added in Sprint 4
- Consider image upload for places (future feature)

---

## Sprint 3 Review: Reviews & API Completion

### Date: Week 6

### Sprint Goal
Implement review system and complete all API endpoints.

### Completed Features

| Feature | Status | Demo |
|---------|--------|------|
| Review model | ✅ Done | Reviews persist with ratings |
| Review CRUD endpoints | ✅ Done | Create, Read, Update, Delete |
| Rating validation (1-5) | ✅ Done | Invalid ratings rejected |
| Prevent self-review | ✅ Done | Owners cannot review own place |
| Get reviews by place | ✅ Done | /places/{id}/reviews working |
| Get reviews by user | ✅ Done | Filter by user_id working |

### Demo Notes
- Created review for a place
- Showed rating validation (rejected rating of 6)
- Demonstrated self-review prevention
- Verified reviews appear on place details

### Stakeholder Feedback
- Review system works well
- Average rating calculation would be nice ✅ Added
- Consider review moderation (future feature)

---

## Sprint 4 Review: Frontend & Integration

### Date: Week 8

### Sprint Goal
Implement web frontend and perform final integration testing.

### Completed Features

| Feature | Status | Demo |
|---------|--------|------|
| Login page | ✅ Done | Users can login via UI |
| Places listing page | ✅ Done | All places displayed |
| Place details page | ✅ Done | Full info with reviews |
| Add review form | ✅ Done | Authenticated users can review |
| Price filter | ✅ Done | Filter by max price |
| JWT cookie storage | ✅ Done | Token persists in browser |
| Responsive design | ✅ Done | Works on mobile |

### Demo Notes
- Full user flow demonstrated: Login → Browse → View → Review
- Showed price filtering in action
- Verified login state persists across page navigation
- Tested on desktop and mobile views

### Final Stakeholder Feedback
- MVP is complete and functional
- UI is clean and usable
- All core features working as expected
- Ready for deployment

---

## Summary of All Sprints

| Sprint | Planned Tasks | Completed | Velocity |
|--------|---------------|-----------|----------|
| Sprint 1 | 10 | 10 | 100% |
| Sprint 2 | 9 | 9 | 100% |
| Sprint 3 | 8 | 8 | 100% |
| Sprint 4 | 10 | 10 | 100% |
| **Total** | **37** | **37** | **100%** |
