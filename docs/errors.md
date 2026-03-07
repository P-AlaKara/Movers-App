# Error Handling

## Error Response Format

All error responses follow a consistent JSON format:

```json
{
  "detail": "Error message",
  "error_code": "string",
  "status_code": "integer"
}
```

For field validation errors:

```json
{
  "field_name": ["Error message 1", "Error message 2"]
}
```

---

## HTTP Status Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Request successful, no content to return |
| 400 | Bad Request | Invalid request parameters or body |
| 401 | Unauthorized | Authentication required or invalid token |
| 403 | Forbidden | Authenticated but not authorized for this action |
| 404 | Not Found | Resource not found |
| 405 | Method Not Allowed | HTTP method not allowed for this endpoint |
| 409 | Conflict | Request conflicts with current state |
| 422 | Unprocessable Entity | Validation failed |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Server temporarily unavailable |

---

## Common Error Responses

### 400 Bad Request

**Scenario:** Invalid request parameters or body

```json
{
  "detail": "Invalid request body",
  "error_code": "INVALID_REQUEST",
  "status_code": 400
}
```

**Field Validation Error:**

```json
{
  "pickup_location": ["This field may not be blank."],
  "delivery_date": ["Ensure this field has no more than 100 characters."],
  "bid_amount": ["A valid number is required."]
}
```

### 401 Unauthorized

**Scenario:** Missing or invalid authentication token

```json
{
  "detail": "Authentication credentials were not provided.",
  "error_code": "NOT_AUTHENTICATED",
  "status_code": 401
}
```

**Invalid Token:**

```json
{
  "detail": "Invalid token.",
  "error_code": "INVALID_TOKEN",
  "status_code": 401
}
```

**Expired Token:**

```json
{
  "detail": "Token has expired.",
  "error_code": "TOKEN_EXPIRED",
  "status_code": 401
}
```

### 403 Forbidden

**Scenario:** User lacks permission to access resource

```json
{
  "detail": "You do not have permission to perform this action.",
  "error_code": "PERMISSION_DENIED",
  "status_code": 403
}
```

**Role-Based Access:**

```json
{
  "detail": "Only movers can perform this action.",
  "error_code": "INVALID_USER_TYPE",
  "status_code": 403
}
```

### 404 Not Found

**Scenario:** Requested resource does not exist

```json
{
  "detail": "Not found.",
  "error_code": "NOT_FOUND",
  "status_code": 404
}
```

---

## Authentication Errors

### Invalid Credentials

```
POST /api/auth/login/
```

**Response (400 Bad Request):**

```json
{
  "detail": "Invalid username or password.",
  "error_code": "INVALID_CREDENTIALS",
  "status_code": 400
}
```

### User Already Exists

```
POST /api/auth/register/
```

**Response (409 Conflict):**

```json
{
  "username": ["A user with that username already exists."],
  "email": ["A user with that email already exists."]
}
```

### Password Validation Failed

```
POST /api/auth/register/
```

**Response (400 Bad Request):**

```json
{
  "password": ["Password must be at least 8 characters long."],
  "password_confirm": ["Passwords do not match."]
}
```

---

## Business Logic Errors

### Cannot Accept Bid on Assigned Request

```
POST /jobs/assignments/
```

**Response (409 Conflict):**

```json
{
  "detail": "This request already has an accepted bid.",
  "error_code": "ALREADY_ASSIGNED",
  "status_code": 409
}
```

### Cannot Bid on Own Request

```
POST /jobs/bids/
```

**Response (403 Forbidden):**

```json
{
  "detail": "You cannot bid on your own moving request.",
  "error_code": "INVALID_BID",
  "status_code": 403
}
```

### Cannot Update Completed Job

```
PUT /jobs/assignments/{id}/
```

**Response (409 Conflict):**

```json
{
  "detail": "Cannot update a completed job.",
  "error_code": "JOB_ALREADY_COMPLETED",
  "status_code": 409
}
```

### Invalid Date Range

```
POST /jobs/requests/
```

**Response (400 Bad Request):**

```json
{
  "detail": "Delivery date must be after pickup date.",
  "error_code": "INVALID_DATE_RANGE",
  "status_code": 400
}
```

### Pickup Date in the Past

```
POST /jobs/requests/
```

**Response (400 Bad Request):**

```json
{
  "detail": "Pickup date cannot be in the past.",
  "error_code": "PAST_DATE",
  "status_code": 400
}
```

---

## Rate Limiting Errors

### 429 Too Many Requests

```json
{
  "detail": "Request throttled. Expected available in 60 seconds.",
  "error_code": "THROTTLED",
  "status_code": 429,
  "retry_after": "60"
}
```

---

## Server Errors

### 500 Internal Server Error

```json
{
  "detail": "Internal server error.",
  "error_code": "INTERNAL_ERROR",
  "status_code": 500
}
```

### 503 Service Unavailable

```json
{
  "detail": "Service temporarily unavailable.",
  "error_code": "SERVICE_UNAVAILABLE",
  "status_code": 503
}
```

---

## Error Codes Reference

| Error Code | HTTP Status | Description |
|----------|-------------|-------------|
| INVALID_REQUEST | 400 | Invalid request parameters |
| INVALID_CREDENTIALS | 400 | Invalid login credentials |
| INVALID_DATE_RANGE | 400 | Invalid date range provided |
| PAST_DATE | 400 | Date cannot be in the past |
| NOT_AUTHENTICATED | 401 | No authentication credentials |
| INVALID_TOKEN | 401 | Invalid or malformed token |
| TOKEN_EXPIRED | 401 | Token has expired |
| PERMISSION_DENIED | 403 | User lacks required permissions |
| INVALID_USER_TYPE | 403 | User type not allowed for action |
| NOT_FOUND | 404 | Resource not found |
| ALREADY_ASSIGNED | 409 | Request already assigned |
| INVALID_BID | 409 | Invalid bid operation |
| JOB_ALREADY_COMPLETED | 409 | Job already completed |
| THROTTLED | 429 | Too many requests |
| INTERNAL_ERROR | 500 | Internal server error |
| SERVICE_UNAVAILABLE | 503 | Service temporarily unavailable |

---

## Handling Errors

### Best Practices

1. **Always check status codes** before processing the response
2. **Use error_code** for programmatic error handling
3. **Display detail message** to users
4. **Implement retry logic** for 5xx errors with exponential backoff
5. **Handle 401 Unauthorized** by refreshing token or redirecting to login
6. **Validate input** before sending requests to reduce 400 errors

### Example Error Handling (JavaScript)

```javascript
async function makeAPIRequest(url, options = {}) {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Authorization': `Bearer ${getToken()}`,
        ...options.headers
      }
    });

    if (!response.ok) {
      const error = await response.json();
      
      switch (response.status) {
        case 401:
          // Handle token expiry - refresh or redirect to login
          refreshToken();
          break;
        case 403:
          // Handle permission denied
          console.error('Permission denied:', error.detail);
          break;
        case 404:
          // Handle resource not found
          console.error('Resource not found:', error.detail);
          break;
        default:
          console.error(`Error ${response.status}:`, error.detail);
      }
      throw error;
    }

    return await response.json();
  } catch (err) {
    console.error('Request failed:', err);
    throw err;
  }
}
```
