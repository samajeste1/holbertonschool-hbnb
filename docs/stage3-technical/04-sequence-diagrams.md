# HBnB - Sequence Diagrams (Stage 3)

## 1. User Login Sequence

```
┌──────┐          ┌─────────┐          ┌─────────┐          ┌──────────┐          ┌──────────┐
│Client│          │  API    │          │ Facade  │          │UserModel │          │ Database │
└──┬───┘          └────┬────┘          └────┬────┘          └────┬─────┘          └────┬─────┘
   │                   │                    │                    │                     │
   │ POST /auth/login  │                    │                    │                     │
   │ {email, password} │                    │                    │                     │
   │──────────────────▶│                    │                    │                     │
   │                   │                    │                    │                     │
   │                   │ get_user_by_email()│                    │                     │
   │                   │───────────────────▶│                    │                     │
   │                   │                    │                    │                     │
   │                   │                    │ query(email)       │                     │
   │                   │                    │───────────────────▶│                     │
   │                   │                    │                    │                     │
   │                   │                    │                    │  SELECT * FROM users│
   │                   │                    │                    │────────────────────▶│
   │                   │                    │                    │                     │
   │                   │                    │                    │◀────user data───────│
   │                   │                    │◀───────────────────│                     │
   │                   │◀───────────────────│                    │                     │
   │                   │                    │                    │                     │
   │                   │ verify_password()  │                    │                     │
   │                   │───────────────────▶│                    │                     │
   │                   │                    │                    │                     │
   │                   │                    │ bcrypt.check()     │                     │
   │                   │                    │───────────────────▶│                     │
   │                   │                    │◀───True/False──────│                     │
   │                   │◀───────────────────│                    │                     │
   │                   │                    │                    │                     │
   │                   │ create_access_token│                    │                     │
   │                   │ (user_id)          │                    │                     │
   │                   │                    │                    │                     │
   │◀──JWT Token───────│                    │                    │                     │
   │                   │                    │                    │                     │
```

## 2. Create Place Sequence

```
┌──────┐          ┌─────────┐          ┌───────────┐          ┌─────────┐          ┌──────────┐
│Client│          │  API    │          │JWT Verify │          │ Facade  │          │ Database │
└──┬───┘          └────┬────┘          └─────┬─────┘          └────┬────┘          └────┬─────┘
   │                   │                     │                     │                    │
   │ POST /places      │                     │                     │                    │
   │ + JWT Header      │                     │                     │                    │
   │ {title, desc...}  │                     │                     │                    │
   │──────────────────▶│                     │                     │                    │
   │                   │                     │                     │                    │
   │                   │ validate_token()    │                     │                    │
   │                   │────────────────────▶│                     │                    │
   │                   │                     │                     │                    │
   │                   │◀──user_id───────────│                     │                    │
   │                   │                     │                     │                    │
   │                   │ create_place(data, owner_id)              │                    │
   │                   │──────────────────────────────────────────▶│                    │
   │                   │                     │                     │                    │
   │                   │                     │                     │ validate_data()    │
   │                   │                     │                     │────────┐           │
   │                   │                     │                     │◀───────┘           │
   │                   │                     │                     │                    │
   │                   │                     │                     │ INSERT INTO places │
   │                   │                     │                     │───────────────────▶│
   │                   │                     │                     │                    │
   │                   │                     │                     │◀──success──────────│
   │                   │◀──────────────────────────────────────────│                    │
   │                   │                     │                     │                    │
   │◀──201 Created─────│                     │                     │                    │
   │   {place data}    │                     │                     │                    │
   │                   │                     │                     │                    │
```

## 3. Get Place Details with Reviews Sequence

```
┌──────┐          ┌─────────┐          ┌─────────┐          ┌──────────┐
│Client│          │  API    │          │ Facade  │          │ Database │
└──┬───┘          └────┬────┘          └────┬────┘          └────┬─────┘
   │                   │                    │                    │
   │ GET /places/{id}  │                    │                    │
   │──────────────────▶│                    │                    │
   │                   │                    │                    │
   │                   │ get_place(id)      │                    │
   │                   │───────────────────▶│                    │
   │                   │                    │                    │
   │                   │                    │ SELECT * FROM places
   │                   │                    │ WHERE id = ?       │
   │                   │                    │───────────────────▶│
   │                   │                    │◀──place data───────│
   │                   │                    │                    │
   │                   │                    │ SELECT * FROM reviews
   │                   │                    │ WHERE place_id = ? │
   │                   │                    │───────────────────▶│
   │                   │                    │◀──reviews list─────│
   │                   │                    │                    │
   │                   │                    │ SELECT * FROM amenities
   │                   │                    │ JOIN place_amenity │
   │                   │                    │───────────────────▶│
   │                   │                    │◀──amenities list───│
   │                   │                    │                    │
   │                   │◀──place + reviews──│                    │
   │                   │   + amenities      │                    │
   │                   │                    │                    │
   │◀──200 OK──────────│                    │                    │
   │  {complete data}  │                    │                    │
   │                   │                    │                    │
```

## 4. Create Review Sequence

```
┌──────┐          ┌─────────┐          ┌───────────┐          ┌─────────┐          ┌──────────┐
│Client│          │  API    │          │JWT Verify │          │ Facade  │          │ Database │
└──┬───┘          └────┬────┘          └─────┬─────┘          └────┬────┘          └────┬─────┘
   │                   │                     │                     │                    │
   │POST /reviews      │                     │                     │                    │
   │+ JWT Header       │                     │                     │                    │
   │{text,rating,      │                     │                     │                    │
   │ place_id}         │                     │                     │                    │
   │──────────────────▶│                     │                     │                    │
   │                   │                     │                     │                    │
   │                   │ validate_token()    │                     │                    │
   │                   │────────────────────▶│                     │                    │
   │                   │◀──user_id───────────│                     │                    │
   │                   │                     │                     │                    │
   │                   │ create_review(data, user_id)              │                    │
   │                   │──────────────────────────────────────────▶│                    │
   │                   │                     │                     │                    │
   │                   │                     │                     │ get_place(place_id)│
   │                   │                     │                     │───────────────────▶│
   │                   │                     │                     │◀──place exists─────│
   │                   │                     │                     │                    │
   │                   │                     │                     │ check_not_owner()  │
   │                   │                     │                     │────────┐           │
   │                   │                     │                     │◀───────┘           │
   │                   │                     │                     │                    │
   │                   │                     │                     │ validate_rating()  │
   │                   │                     │                     │ (1-5)              │
   │                   │                     │                     │────────┐           │
   │                   │                     │                     │◀───────┘           │
   │                   │                     │                     │                    │
   │                   │                     │                     │INSERT INTO reviews │
   │                   │                     │                     │───────────────────▶│
   │                   │                     │                     │◀──success──────────│
   │                   │◀──────────────────────────────────────────│                    │
   │                   │                     │                     │                    │
   │◀──201 Created─────│                     │                     │                    │
   │   {review data}   │                     │                     │                    │
   │                   │                     │                     │                    │
```

## Summary of Key Interactions

| Use Case | Components Involved | Key Steps |
|----------|--------------------|-----------|
| User Login | Client → API → Facade → User Model → DB | Verify credentials, generate JWT |
| Create Place | Client → API → JWT → Facade → DB | Validate token, validate data, insert |
| Get Place | Client → API → Facade → DB | Fetch place + reviews + amenities |
| Create Review | Client → API → JWT → Facade → DB | Validate token, check ownership, insert |
