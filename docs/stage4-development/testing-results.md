# HBnB - Testing Evidence and Results

## Testing Strategy Overview

| Test Type | Tool | Coverage |
|-----------|------|----------|
| Unit Tests | pytest | Models, Validation |
| API Tests | Postman | All endpoints |
| Integration Tests | Manual | Frontend-Backend |
| End-to-End Tests | Browser | User flows |

---

## 1. API Testing Results (Postman)

### Authentication Endpoints

| Test Case | Endpoint | Method | Expected | Result |
|-----------|----------|--------|----------|--------|
| Valid login | /auth/login | POST | 200 + token | ✅ PASS |
| Invalid password | /auth/login | POST | 401 | ✅ PASS |
| Invalid email | /auth/login | POST | 401 | ✅ PASS |
| Missing fields | /auth/login | POST | 400 | ✅ PASS |
| Get admin token | /auth/admin-token | GET | 200 + token | ✅ PASS |
| Protected endpoint (valid) | /auth/protected | GET | 200 | ✅ PASS |
| Protected endpoint (no token) | /auth/protected | GET | 401 | ✅ PASS |

### User Endpoints

| Test Case | Endpoint | Method | Expected | Result |
|-----------|----------|--------|----------|--------|
| Get all users | /users/ | GET | 200 + list | ✅ PASS |
| Get user by ID | /users/{id} | GET | 200 + user | ✅ PASS |
| Get invalid user | /users/invalid | GET | 404 | ✅ PASS |
| Create user (admin) | /users/ | POST | 201 | ✅ PASS |
| Create user (duplicate email) | /users/ | POST | 409 | ✅ PASS |
| Update user | /users/{id} | PUT | 200 | ✅ PASS |

### Place Endpoints

| Test Case | Endpoint | Method | Expected | Result |
|-----------|----------|--------|----------|--------|
| Get all places | /places/ | GET | 200 + list | ✅ PASS |
| Get place by ID | /places/{id} | GET | 200 + place | ✅ PASS |
| Get invalid place | /places/invalid | GET | 404 | ✅ PASS |
| Create place (auth) | /places/ | POST | 201 | ✅ PASS |
| Create place (no auth) | /places/ | POST | 401 | ✅ PASS |
| Create place (invalid price) | /places/ | POST | 400 | ✅ PASS |
| Update place (owner) | /places/{id} | PUT | 200 | ✅ PASS |
| Update place (not owner) | /places/{id} | PUT | 403 | ✅ PASS |

### Review Endpoints

| Test Case | Endpoint | Method | Expected | Result |
|-----------|----------|--------|----------|--------|
| Get all reviews | /reviews/ | GET | 200 + list | ✅ PASS |
| Get review by ID | /reviews/{id} | GET | 200 + review | ✅ PASS |
| Create review (auth) | /reviews/ | POST | 201 | ✅ PASS |
| Create review (no auth) | /reviews/ | POST | 401 | ✅ PASS |
| Create review (rating > 5) | /reviews/ | POST | 400 | ✅ PASS |
| Create review (rating < 1) | /reviews/ | POST | 400 | ✅ PASS |
| Create review (own place) | /reviews/ | POST | 400 | ✅ PASS |
| Delete review (author) | /reviews/{id} | DELETE | 200 | ✅ PASS |
| Delete review (not author) | /reviews/{id} | DELETE | 403 | ✅ PASS |

### Amenity Endpoints

| Test Case | Endpoint | Method | Expected | Result |
|-----------|----------|--------|----------|--------|
| Get all amenities | /amenities/ | GET | 200 + list | ✅ PASS |
| Get amenity by ID | /amenities/{id} | GET | 200 + amenity | ✅ PASS |
| Create amenity | /amenities/ | POST | 201 | ✅ PASS |
| Create amenity (empty name) | /amenities/ | POST | 400 | ✅ PASS |
| Update amenity | /amenities/{id} | PUT | 200 | ✅ PASS |

---

## 2. Unit Test Results

### Model Validation Tests

```
tests/test_models.py

test_user_creation .......................... PASSED
test_user_email_validation .................. PASSED
test_user_password_hashing .................. PASSED
test_user_password_verification ............. PASSED
test_place_creation ......................... PASSED
test_place_price_validation ................. PASSED
test_place_coordinates_validation ........... PASSED
test_review_creation ........................ PASSED
test_review_rating_validation ............... PASSED
test_amenity_creation ....................... PASSED

================================
10 passed in 0.45s
```

### Business Logic Tests

```
tests/test_facade.py

test_create_user ............................ PASSED
test_duplicate_email ........................ PASSED
test_user_authentication .................... PASSED
test_create_place ........................... PASSED
test_place_owner_assignment ................. PASSED
test_create_review .......................... PASSED
test_review_rating_bounds ................... PASSED
test_self_review_prevention ................. PASSED

================================
8 passed in 0.32s
```

---

## 3. End-to-End Test Results

### User Flow: Login → Browse → View → Review

| Step | Action | Expected Result | Actual Result |
|------|--------|-----------------|---------------|
| 1 | Open login.html | Login form displayed | ✅ PASS |
| 2 | Enter valid credentials | Redirect to index.html | ✅ PASS |
| 3 | View places list | All places displayed | ✅ PASS |
| 4 | Apply price filter | Filtered places shown | ✅ PASS |
| 5 | Click "View Details" | Place details page loads | ✅ PASS |
| 6 | View reviews section | Reviews displayed | ✅ PASS |
| 7 | Add review (logged in) | Form visible | ✅ PASS |
| 8 | Submit review | Review added, redirect | ✅ PASS |
| 9 | Refresh page | New review visible | ✅ PASS |

### Security Tests

| Test | Description | Result |
|------|-------------|--------|
| XSS Prevention | Inject script in review text | ✅ Escaped |
| SQL Injection | Inject SQL in login form | ✅ Blocked |
| JWT Tampering | Modify token payload | ✅ Rejected |
| CORS Check | Cross-origin request | ✅ Allowed for API |
| Password Storage | Check database | ✅ Hashed with bcrypt |

---

## 4. Test Summary

### Overall Results

| Category | Total | Passed | Failed | Pass Rate |
|----------|-------|--------|--------|-----------|
| API Tests | 35 | 35 | 0 | 100% |
| Unit Tests | 18 | 18 | 0 | 100% |
| E2E Tests | 9 | 9 | 0 | 100% |
| Security Tests | 5 | 5 | 0 | 100% |
| **Total** | **67** | **67** | **0** | **100%** |

### Known Issues
- None (all bugs fixed during development)

### Test Environment
- **Backend**: Python 3.11, Flask 2.3
- **Database**: SQLite (development)
- **Browser**: Chrome 120, Firefox 121
- **OS**: Windows 11

---

## 5. How to Run Tests

### API Tests (Postman)
```bash
# Import collection from docs/postman/
# Set environment variable: base_url = http://localhost:5001/api/v1
# Run collection
```

### Unit Tests (pytest)
```bash
cd part3
python -m pytest tests/ -v
```

### Manual Testing
```bash
# Start backend
cd part3
python run.py

# Open frontend
# Open part4/index.html in browser
```
