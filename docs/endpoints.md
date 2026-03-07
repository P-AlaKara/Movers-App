# API Endpoints

## OpenAPI 3.0 Specification

This document outlines all available endpoints in the Songa API.

## Base URL

```
http://localhost:8000/api
```

## Authentication

All endpoints except `/auth/register/` and `/auth/login/` require authentication.

**Header:**
```
Authorization: Bearer <token>
```

---

## Moving Requests

### List Moving Requests

Retrieve all moving requests with optional filtering.

```
GET /jobs/requests/
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | string | Filter by status: `pending`, `accepted`, `in_progress`, `completed` |
| `customer_id` | integer | Filter by customer ID |
| `page` | integer | Pagination page number |
| `page_size` | integer | Number of results per page |

**Response (200 OK):**

```json
{
  "count": "integer",
  "next": "string or null",
  "previous": "string or null",
  "results": [
    {
      "id": "integer",
      "customer": "integer",
      "pickup_location": "string",
      "delivery_location": "string",
      "pickup_date": "2026-03-07",
      "delivery_date": "2026-03-08",
      "description": "string",
      "status": "pending|accepted|in_progress|completed",
      "created_at": "2026-03-07T10:30:00Z",
      "updated_at": "2026-03-07T10:30:00Z"
    }
  ]
}
```

### Create Moving Request

Create a new moving request.

```
POST /jobs/requests/
Content-Type: application/json
Authorization: Bearer <token>
```

**Request Body:**

```json
{
  "pickup_location": "string",
  "delivery_location": "string",
  "pickup_date": "2026-03-07",
  "delivery_date": "2026-03-08",
  "description": "string",
  "estimated_distance": "integer"
}
```

**Response (201 Created):**

```json
{
  "id": "integer",
  "customer": "integer",
  "pickup_location": "string",
  "delivery_location": "string",
  "pickup_date": "2026-03-07",
  "delivery_date": "2026-03-08",
  "description": "string",
  "estimated_distance": "integer",
  "status": "pending",
  "created_at": "2026-03-07T10:30:00Z",
  "updated_at": "2026-03-07T10:30:00Z"
}
```

### Get Moving Request Details

Retrieve a specific moving request.

```
GET /jobs/requests/{id}/
Authorization: Bearer <token>
```

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | integer | Moving request ID |

**Response (200 OK):**

```json
{
  "id": "integer",
  "customer": "integer",
  "pickup_location": "string",
  "delivery_location": "string",
  "pickup_date": "2026-03-07",
  "delivery_date": "2026-03-08",
  "description": "string",
  "estimated_distance": "integer",
  "status": "string",
  "bids_count": "integer",
  "created_at": "2026-03-07T10:30:00Z",
  "updated_at": "2026-03-07T10:30:00Z"
}
```

### Update Moving Request

Update a moving request (customer only).

```
PUT /jobs/requests/{id}/
Content-Type: application/json
Authorization: Bearer <token>
```

**Request Body:**

```json
{
  "pickup_location": "string",
  "delivery_location": "string",
  "pickup_date": "2026-03-07",
  "delivery_date": "2026-03-08",
  "description": "string"
}
```

**Response (200 OK):**

```json
{
  "id": "integer",
  "customer": "integer",
  "pickup_location": "string",
  "delivery_location": "string",
  "pickup_date": "2026-03-07",
  "delivery_date": "2026-03-08",
  "description": "string",
  "status": "string",
  "created_at": "2026-03-07T10:30:00Z",
  "updated_at": "2026-03-07T10:30:00Z"
}
```

### Delete Moving Request

Delete a moving request (customer only, only if status is pending).

```
DELETE /jobs/requests/{id}/
Authorization: Bearer <token>
```

**Response (204 No Content):**

Empty response body

---

## Bids

### List Bids

Retrieve all bids with optional filtering.

```
GET /jobs/bids/
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `request_id` | integer | Filter by moving request ID |
| `mover_id` | integer | Filter by mover ID |
| `status` | string | Filter by status: `pending`, `accepted`, `rejected` |

**Response (200 OK):**

```json
{
  "count": "integer",
  "next": "string or null",
  "previous": "string or null",
  "results": [
    {
      "id": "integer",
      "request": "integer",
      "mover": "integer",
      "mover_name": "string",
      "bid_amount": "number",
      "bid_message": "string",
      "status": "pending|accepted|rejected",
      "created_at": "2026-03-07T10:30:00Z",
      "updated_at": "2026-03-07T10:30:00Z"
    }
  ]
}
```

### Create Bid

Place a bid on a moving request (mover only).

```
POST /jobs/bids/
Content-Type: application/json
Authorization: Bearer <token>
```

**Request Body:**

```json
{
  "request": "integer",
  "bid_amount": "number",
  "bid_message": "string"
}
```

**Response (201 Created):**

```json
{
  "id": "integer",
  "request": "integer",
  "mover": "integer",
  "bid_amount": "number",
  "bid_message": "string",
  "status": "pending",
  "created_at": "2026-03-07T10:30:00Z"
}
```

### Get Bid Details

Retrieve a specific bid.

```
GET /jobs/bids/{id}/
Authorization: Bearer <token>
```

**Response (200 OK):**

```json
{
  "id": "integer",
  "request": "integer",
  "mover": "integer",
  "mover_name": "string",
  "bid_amount": "number",
  "bid_message": "string",
  "status": "string",
  "created_at": "2026-03-07T10:30:00Z"
}
```

### Update Bid Status

Update bid status (customer only).

```
PUT /jobs/bids/{id}/
Content-Type: application/json
Authorization: Bearer <token>
```

**Request Body:**

```json
{
  "status": "accepted|rejected"
}
```

**Response (200 OK):**

```json
{
  "id": "integer",
  "request": "integer",
  "mover": "integer",
  "bid_amount": "number",
  "status": "string",
  "updated_at": "2026-03-07T10:30:00Z"
}
```

---

## Job Assignments

### List Job Assignments

Retrieve assigned jobs for the current user.

```
GET /jobs/assignments/
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | string | Filter by status: `accepted`, `in_progress`, `completed` |

**Response (200 OK):**

```json
{
  "count": "integer",
  "results": [
    {
      "id": "integer",
      "bid": "integer",
      "request": "integer",
      "customer": "integer",
      "mover": "integer",
      "status": "accepted|in_progress|completed",
      "assigned_date": "2026-03-07T10:30:00Z",
      "completion_date": "2026-03-08T15:45:00Z"
    }
  ]
}
```

### Create Job Assignment

Accept a bid and create a job assignment (customer only).

```
POST /jobs/assignments/
Content-Type: application/json
Authorization: Bearer <token>
```

**Request Body:**

```json
{
  "bid": "integer"
}
```

**Response (201 Created):**

```json
{
  "id": "integer",
  "bid": "integer",
  "request": "integer",
  "customer": "integer",
  "mover": "integer",
  "status": "accepted",
  "assigned_date": "2026-03-07T10:30:00Z"
}
```

### Update Job Assignment Status

Update the status of an assigned job (mover only).

```
PUT /jobs/assignments/{id}/
Content-Type: application/json
Authorization: Bearer <token>
```

**Request Body:**

```json
{
  "status": "in_progress|completed"
}
```

**Response (200 OK):**

```json
{
  "id": "integer",
  "bid": "integer",
  "request": "integer",
  "status": "string",
  "updated_at": "2026-03-07T10:30:00Z"
}
```

---

## User Profiles

### Get Current User Profile

Retrieve the authenticated user's profile.

```
GET /profiles/
Authorization: Bearer <token>
```

**Response (200 OK):**

```json
{
  "id": "integer",
  "user": "integer",
  "user_type": "customer|mover",
  "phone": "string",
  "address": "string",
  "city": "string",
  "service_area": "string",
  "rating": "number",
  "total_jobs": "integer",
  "bio": "string",
  "created_at": "2026-03-07T10:30:00Z",
  "updated_at": "2026-03-07T10:30:00Z"
}
```

### Update User Profile

Update the authenticated user's profile.

```
PUT /profiles/
Content-Type: application/json
Authorization: Bearer <token>
```

**Request Body:**

```json
{
  "phone": "string",
  "address": "string",
  "city": "string",
  "service_area": "string",
  "bio": "string"
}
```

**Response (200 OK):**

```json
{
  "id": "integer",
  "user": "integer",
  "user_type": "string",
  "phone": "string",
  "address": "string",
  "city": "string",
  "service_area": "string",
  "rating": "number",
  "bio": "string",
  "updated_at": "2026-03-07T10:30:00Z"
}
```

### Get Specific User Profile

Retrieve another user's profile.

```
GET /profiles/{id}/
Authorization: Bearer <token>
```

**Response (200 OK):**

```json
{
  "id": "integer",
  "user": "integer",
  "user_type": "string",
  "phone": "string",
  "city": "string",
  "rating": "number",
  "total_jobs": "integer",
  "bio": "string"
}
```

---

## Notifications

### List Notifications

Retrieve all notifications for the authenticated user.

```
GET /notifications/
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `is_read` | boolean | Filter by read status |
| `page` | integer | Pagination page number |

**Response (200 OK):**

```json
{
  "count": "integer",
  "results": [
    {
      "id": "integer",
      "user": "integer",
      "title": "string",
      "message": "string",
      "notification_type": "string",
      "is_read": "boolean",
      "created_at": "2026-03-07T10:30:00Z",
      "data": {}
    }
  ]
}
```

### Mark Notification as Read

Mark a specific notification as read.

```
PUT /notifications/{id}/
Content-Type: application/json
Authorization: Bearer <token>
```

**Request Body:**

```json
{
  "is_read": true
}
```

**Response (200 OK):**

```json
{
  "id": "integer",
  "user": "integer",
  "title": "string",
  "message": "string",
  "is_read": true,
  "updated_at": "2026-03-07T10:30:00Z"
}
```

### Delete Notification

Delete a specific notification.

```
DELETE /notifications/{id}/
Authorization: Bearer <token>
```

**Response (204 No Content):**

Empty response body
