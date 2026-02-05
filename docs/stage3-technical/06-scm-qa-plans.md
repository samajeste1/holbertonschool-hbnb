# HBnB - SCM and QA Plans (Stage 3)

## Source Control Management (SCM) Strategy

### Version Control Tool
**Git** with **GitHub** for remote repository hosting.

### Branching Strategy

```
main (production-ready)
  │
  └── develop (integration branch)
        │
        ├── feature/user-authentication
        ├── feature/place-crud
        ├── feature/review-system
        ├── feature/frontend-login
        └── bugfix/review-validation
```

### Branch Naming Convention

| Branch Type | Format | Example |
|-------------|--------|---------|
| Feature | `feature/<description>` | `feature/jwt-authentication` |
| Bug Fix | `bugfix/<description>` | `bugfix/password-validation` |
| Hotfix | `hotfix/<description>` | `hotfix/login-error` |

### Git Workflow

1. **Create feature branch** from `develop`
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/new-feature
   ```

2. **Develop and commit** with meaningful messages
   ```bash
   git add .
   git commit -m "Add user registration endpoint"
   ```

3. **Push and create Pull Request**
   ```bash
   git push origin feature/new-feature
   ```

4. **Code Review** by SCM/team member

5. **Merge to develop** after approval

6. **Merge to main** for releases

### Commit Message Convention

```
<type>: <short description>

[optional body]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code formatting
- `refactor`: Code refactoring
- `test`: Adding tests

Examples:
```
feat: Add JWT authentication to login endpoint
fix: Correct password validation for special characters
docs: Update API documentation for reviews
```

### Code Review Checklist

- [ ] Code follows project style guide
- [ ] All tests pass
- [ ] No security vulnerabilities
- [ ] Documentation updated if needed
- [ ] No unnecessary commented code
- [ ] Proper error handling

---

## Quality Assurance (QA) Strategy

### Testing Levels

| Level | Description | Tools |
|-------|-------------|-------|
| Unit Testing | Test individual functions/methods | pytest |
| Integration Testing | Test API endpoints | pytest, Postman |
| End-to-End Testing | Test complete user flows | Manual, Browser |

### Testing Tools

| Tool | Purpose |
|------|---------|
| **pytest** | Python unit and integration tests |
| **Postman** | API endpoint testing |
| **Browser DevTools** | Frontend debugging |

### Unit Test Examples

```python
# test_user.py
def test_user_creation():
    user = User(
        first_name="John",
        last_name="Doe",
        email="john@example.com"
    )
    user.hash_password("password123")
    assert user.first_name == "John"
    assert user.verify_password("password123") == True

def test_user_email_validation():
    with pytest.raises(ValueError):
        User(first_name="John", last_name="Doe", email="invalid-email")

# test_place.py
def test_place_price_validation():
    with pytest.raises(ValueError):
        Place(title="Test", price=-100, latitude=0, longitude=0)

def test_place_coordinates_validation():
    with pytest.raises(ValueError):
        Place(title="Test", price=100, latitude=100, longitude=0)  # Invalid latitude
```

### API Testing with Postman

#### Test Collection Structure
```
HBnB API Tests
├── Authentication
│   ├── Login - Valid credentials
│   ├── Login - Invalid credentials
│   └── Login - Missing fields
├── Users
│   ├── Get all users
│   ├── Get user by ID
│   ├── Create user (admin)
│   └── Update user
├── Places
│   ├── Get all places
│   ├── Get place by ID
│   ├── Create place (authenticated)
│   └── Update place (owner)
├── Reviews
│   ├── Create review
│   ├── Get reviews for place
│   └── Delete review
└── Amenities
    ├── Get all amenities
    └── Create amenity (admin)
```

#### Test Scenarios

| Endpoint | Test Case | Expected Result |
|----------|-----------|-----------------|
| POST /auth/login | Valid credentials | 200 + JWT token |
| POST /auth/login | Invalid password | 401 Unauthorized |
| POST /places | No token | 401 Unauthorized |
| POST /places | Valid token + data | 201 Created |
| POST /reviews | Rating = 6 | 400 Bad Request |
| POST /reviews | Own place | 400 Forbidden |

### End-to-End Test Scenarios

| Scenario | Steps | Expected Outcome |
|----------|-------|------------------|
| User Registration & Login | 1. Register user 2. Login | JWT token received |
| Create and View Place | 1. Login 2. Create place 3. View place | Place displayed with details |
| Leave Review | 1. Login 2. Select place 3. Submit review | Review appears on place |
| Filter Places | 1. View places 2. Apply price filter | Filtered results displayed |

### Bug Tracking

**Tool:** GitHub Issues

**Bug Report Template:**
```markdown
## Bug Description
Brief description of the issue

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Browser/OS:
- API Version:

## Screenshots
If applicable
```

### Test Execution Schedule

| Phase | Testing Activities |
|-------|-------------------|
| Sprint Development | Unit tests for new features |
| Sprint End | Integration tests for completed features |
| Pre-Release | Full regression testing |
| Post-Deployment | Smoke testing in production |

### Quality Metrics

| Metric | Target |
|--------|--------|
| Unit Test Coverage | > 70% |
| API Tests Passing | 100% |
| Critical Bugs | 0 |
| Bug Resolution Time | < 48 hours |

### Deployment Pipeline

```
Development → Testing → Staging → Production

1. Developer pushes to feature branch
2. Automated tests run
3. Code review required
4. Merge to develop
5. Integration tests
6. Merge to main
7. Deploy to production
```
