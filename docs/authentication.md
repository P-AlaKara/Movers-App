# Authentication

## Overview

The Songa API uses token-based authentication (OAuth 2.0 Bearer Token). All protected endpoints require a valid authentication token in the request headers.

## Authentication Methods

### Bearer Token Authentication

All API requests to protected endpoints must include an `Authorization` header with a bearer token:

```
Authorization: Bearer <token>
```

## Authentication Endpoints

### Register User

Creates a new user account (Customer or Mover).

```
POST /api/auth/register/
Content-Type: application/json
```

**Request Body:**

```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "password_confirm": "string",
  "user_type": "customer|mover",
  "first_name": "string",
  "last_name": "string"
}
```

**Response (201 Created):**

```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "user_type": "string",
  "created_at": "2026-03-07T10:30:00Z"
}
```

### Login

Authenticate user and receive authentication token.

```
POST /api/auth/login/
Content-Type: application/json
```

**Request Body:**

```json
{
  "username": "string",
  "password": "string"
}
```

**Response (200 OK):**

```json
{
  "token": "string",
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string",
    "user_type": "string"
  },
  "expires_in": "integer"
}
```

### Logout

Invalidate the current authentication token.

```
POST /api/auth/logout/
Authorization: Bearer <token>
```

**Response (204 No Content):**

Empty response body

## Token Details

- **Token Type:** Django REST Framework Token
- **Token Format:** 40-character hexadecimal string
- **Expiration:** Tokens do not expire by default (configurable)
- **Storage:** Client should store token securely (localStorage, secure cookies, etc.)

## Security Considerations

- Always send tokens over HTTPS in production
- Never expose tokens in URLs or logs
- Regenerate tokens if compromised
- Use secure storage mechanisms on client applications
- Include token in Authorization header, not query parameters
- Tokens are user-specific and should be treated as sensitive credentials

## Error Responses

### 401 Unauthorized

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden

```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 400 Bad Request (Invalid Credentials)

```json
{
  "detail": "Invalid username or password."
}
```

## Example Usage

### Register

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securePassword123",
    "password_confirm": "securePassword123",
    "user_type": "customer",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securePassword123"
  }'
```

### Authenticated Request

```bash
curl -X GET http://localhost:8000/api/profiles/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Logout

```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```
