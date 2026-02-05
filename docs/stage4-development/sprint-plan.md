# HBnB - Sprint Plan (Stage 4)

## Sprint Overview

| Sprint | Duration | Focus Area |
|--------|----------|------------|
| Sprint 1 | Week 1-2 | Core Models & User Authentication |
| Sprint 2 | Week 3-4 | Places & Amenities CRUD |
| Sprint 3 | Week 5-6 | Reviews & API Completion |
| Sprint 4 | Week 7-8 | Frontend & Integration |

---

## Sprint 1: Core Models & User Authentication

### Sprint Goal
Implement user model with authentication and basic API structure.

### Tasks (MoSCoW Prioritized)

#### Must Have
| Task | Assignee | Status | Priority |
|------|----------|--------|----------|
| Set up Flask project structure | Dev | Done | M |
| Implement BaseClass model | Dev | Done | M |
| Implement User model with SQLAlchemy | Dev | Done | M |
| Add password hashing (bcrypt) | Dev | Done | M |
| Create /auth/login endpoint | Dev | Done | M |
| Implement JWT authentication | Dev | Done | M |
| User CRUD endpoints | Dev | Done | M |

#### Should Have
| Task | Assignee | Status | Priority |
|------|----------|--------|----------|
| Email validation | Dev | Done | S |
| Admin role implementation | Dev | Done | S |
| Unit tests for User model | QA | Done | S |

### Sprint 1 Deliverables
- [ ] User registration and login working
- [ ] JWT tokens generated correctly
- [ ] Password securely hashed
- [ ] API documentation available

---

## Sprint 2: Places & Amenities CRUD

### Sprint Goal
Implement place and amenity models with full CRUD operations.

### Tasks (MoSCoW Prioritized)

#### Must Have
| Task | Assignee | Status | Priority |
|------|----------|--------|----------|
| Implement Place model | Dev | Done | M |
| Place CRUD endpoints | Dev | Done | M |
| Owner authentication for places | Dev | Done | M |
| Implement Amenity model | Dev | Done | M |
| Amenity CRUD endpoints | Dev | Done | M |
| Place-Amenity relationship | Dev | Done | M |

#### Should Have
| Task | Assignee | Status | Priority |
|------|----------|--------|----------|
| GPS coordinate validation | Dev | Done | S |
| Price validation | Dev | Done | S |
| API tests for places | QA | Done | S |

### Sprint 2 Deliverables
- [ ] Places can be created, read, updated
- [ ] Amenities can be managed
- [ ] Places linked to amenities
- [ ] Only owners can modify their places

---

## Sprint 3: Reviews & API Completion

### Sprint Goal
Implement review system and complete all API endpoints.

### Tasks (MoSCoW Prioritized)

#### Must Have
| Task | Assignee | Status | Priority |
|------|----------|--------|----------|
| Implement Review model | Dev | Done | M |
| Review CRUD endpoints | Dev | Done | M |
| Rating validation (1-5) | Dev | Done | M |
| Prevent self-review | Dev | Done | M |
| Get reviews by place | Dev | Done | M |

#### Should Have
| Task | Assignee | Status | Priority |
|------|----------|--------|----------|
| Get reviews by user | Dev | Done | S |
| Delete review endpoint | Dev | Done | S |
| Integration tests | QA | Done | S |

### Sprint 3 Deliverables
- [ ] Reviews can be created and viewed
- [ ] Rating system working
- [ ] All API endpoints complete
- [ ] Swagger documentation updated

---

## Sprint 4: Frontend & Integration

### Sprint Goal
Implement web frontend and perform final integration testing.

### Tasks (MoSCoW Prioritized)

#### Must Have
| Task | Assignee | Status | Priority |
|------|----------|--------|----------|
| Login page HTML/CSS/JS | Dev | Done | M |
| Places listing page | Dev | Done | M |
| Place details page | Dev | Done | M |
| API integration (Fetch) | Dev | Done | M |
| JWT cookie storage | Dev | Done | M |

#### Should Have
| Task | Assignee | Status | Priority |
|------|----------|--------|----------|
| Add review form | Dev | Done | S |
| Price filter functionality | Dev | Done | S |
| Responsive design | Dev | Done | S |
| End-to-end testing | QA | Done | S |

#### Could Have
| Task | Assignee | Status | Priority |
|------|----------|--------|----------|
| UI polish and styling | Dev | Done | C |
| Error handling UI | Dev | Done | C |

### Sprint 4 Deliverables
- [ ] Functional web interface
- [ ] Users can login via UI
- [ ] Places displayed with filtering
- [ ] Reviews can be submitted
- [ ] All integration tests passing

---

## Team Responsibilities

| Role | Team Member | Responsibilities |
|------|-------------|------------------|
| Project Manager | TBD | Sprint planning, standups, progress tracking |
| SCM | TBD | Git workflow, code reviews, branch management |
| QA | TBD | Test planning, test execution, bug tracking |
| Developer | TBD | Feature implementation, bug fixes |

---

## Daily Standup Template

```
What did I do yesterday?
- [Completed tasks]

What will I do today?
- [Planned tasks]

Any blockers?
- [Issues/dependencies]
```

---

## Sprint Metrics

| Metric | Sprint 1 | Sprint 2 | Sprint 3 | Sprint 4 |
|--------|----------|----------|----------|----------|
| Planned Tasks | 10 | 9 | 8 | 10 |
| Completed Tasks | - | - | - | - |
| Velocity | - | - | - | - |
| Bugs Found | - | - | - | - |
| Bugs Fixed | - | - | - | - |

---

## Sprint Review Template

### What was completed?
- List of completed features

### What was not completed?
- List of incomplete items and reasons

### Demo
- Live demonstration of features

### Feedback
- Stakeholder feedback and suggestions

---

## Sprint Retrospective Template

### What went well?
- Positive outcomes

### What could be improved?
- Areas for improvement

### Action items for next sprint
- Specific improvements to implement
