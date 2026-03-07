# API Usage Examples

Comprehensive examples demonstrating how to use the Songa API with various tools and languages.

---

## Prerequisites

- Base URL: `http://localhost:8000/api`
- Authentication Token: Obtain from `/auth/login/`

---

## cURL Examples

### Authentication

#### Register a New User

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_mover",
    "email": "john@example.com",
    "password": "SecurePass123",
    "password_confirm": "SecurePass123",
    "user_type": "mover",
    "first_name": "John",
    "last_name": "Smith"
  }'
```

#### Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_mover",
    "password": "SecurePass123"
  }'
```

**Response:**

```json
{
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9",
  "user": {
    "id": 42,
    "username": "john_mover",
    "email": "john@example.com",
    "user_type": "mover"
  },
  "expires_in": 86400
}
```

#### Logout

```bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Bearer a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9"
```

### Moving Requests

#### Create a Moving Request (Customer)

```bash
curl -X POST http://localhost:8000/api/jobs/requests/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "pickup_location": "123 Main St, New York, NY",
    "delivery_location": "456 Oak Ave, Brooklyn, NY",
    "pickup_date": "2026-03-15",
    "delivery_date": "2026-03-15",
    "description": "Moving 2-bedroom apartment. Need help with furniture, boxes, and fragile items."
  }'
```

#### List All Moving Requests

```bash
curl -X GET "http://localhost:8000/api/jobs/requests/?status=pending" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Get Specific Moving Request

```bash
curl -X GET http://localhost:8000/api/jobs/requests/5/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Update Moving Request

```bash
curl -X PUT http://localhost:8000/api/jobs/requests/5/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "pickup_location": "123 Main St, New York, NY",
    "delivery_location": "789 Pine St, Queens, NY",
    "pickup_date": "2026-03-20",
    "delivery_date": "2026-03-20",
    "description": "Updated moving details - need early morning pickup"
  }'
```

#### Delete Moving Request

```bash
curl -X DELETE http://localhost:8000/api/jobs/requests/5/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Bids

#### Place a Bid (Mover)

```bash
curl -X POST http://localhost:8000/api/jobs/bids/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "request": 5,
    "bid_amount": 450.00,
    "bid_message": "I have 10 years experience with apartment moves. Can provide 3 helpers and equipment."
  }'
```

#### List All Bids for a Request

```bash
curl -X GET "http://localhost:8000/api/jobs/bids/?request_id=5" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Accept a Bid (Customer)

```bash
curl -X PUT http://localhost:8000/api/jobs/bids/12/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "status": "accepted"
  }'
```

#### Reject a Bid (Customer)

```bash
curl -X PUT http://localhost:8000/api/jobs/bids/13/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "status": "rejected"
  }'
```

### Job Assignments

#### Create Job Assignment

```bash
curl -X POST http://localhost:8000/api/jobs/assignments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "bid": 12
  }'
```

#### List Active Jobs (Mover)

```bash
curl -X GET "http://localhost:8000/api/jobs/assignments/?status=in_progress" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Update Job Status to In Progress

```bash
curl -X PUT http://localhost:8000/api/jobs/assignments/8/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "status": "in_progress"
  }'
```

#### Mark Job as Completed

```bash
curl -X PUT http://localhost:8000/api/jobs/assignments/8/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "status": "completed"
  }'
```

### Profiles

#### Get Current User Profile

```bash
curl -X GET http://localhost:8000/api/profiles/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Update Profile (Mover)

```bash
curl -X PUT http://localhost:8000/api/profiles/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "phone": "+1-555-0123",
    "address": "456 Oak Ave, Apt 202",
    "city": "Brooklyn",
    "service_area": "New York, Brooklyn, Queens",
    "bio": "Professional mover with 10+ years experience. Fully insured and equipped."
  }'
```

#### Get Another User's Profile

```bash
curl -X GET http://localhost:8000/api/profiles/42/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Notifications

#### List All Notifications

```bash
curl -X GET http://localhost:8000/api/notifications/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### List Unread Notifications Only

```bash
curl -X GET "http://localhost:8000/api/notifications/?is_read=false" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Mark Notification as Read

```bash
curl -X PUT http://localhost:8000/api/notifications/15/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "is_read": true
  }'
```

#### Delete Notification

```bash
curl -X DELETE http://localhost:8000/api/notifications/15/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## JavaScript/Fetch API Examples

### Helper Function

```javascript
const API_BASE_URL = 'http://localhost:8000/api';

async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = localStorage.getItem('authToken');

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(url, {
    ...options,
    headers
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'API request failed');
  }

  return response.status === 204 ? null : response.json();
}
```

### Authentication Example

```javascript
// Register
async function register(userData) {
  return apiRequest('/auth/register/', {
    method: 'POST',
    body: JSON.stringify(userData)
  });
}

// Login
async function login(username, password) {
  const data = await apiRequest('/auth/login/', {
    method: 'POST',
    body: JSON.stringify({ username, password })
  });
  
  // Store token
  localStorage.setItem('authToken', data.token);
  localStorage.setItem('user', JSON.stringify(data.user));
  
  return data;
}

// Logout
async function logout() {
  await apiRequest('/auth/logout/', { method: 'POST' });
  localStorage.removeItem('authToken');
  localStorage.removeItem('user');
}
```

### Moving Requests Example

```javascript
// Create moving request
async function createRequest(requestData) {
  return apiRequest('/jobs/requests/', {
    method: 'POST',
    body: JSON.stringify(requestData)
  });
}

// Example usage
const newRequest = await createRequest({
  pickup_location: '123 Main St, New York, NY',
  delivery_location: '456 Oak Ave, Brooklyn, NY',
  pickup_date: '2026-03-15',
  delivery_date: '2026-03-15',
  description: 'Moving apartment'
});

// Get all requests
async function getRequests(status = null) {
  const query = status ? `?status=${status}` : '';
  return apiRequest(`/jobs/requests/${query}`);
}

// Update request
async function updateRequest(id, updates) {
  return apiRequest(`/jobs/requests/${id}/`, {
    method: 'PUT',
    body: JSON.stringify(updates)
  });
}

// Delete request
async function deleteRequest(id) {
  return apiRequest(`/jobs/requests/${id}/`, {
    method: 'DELETE'
  });
}
```

### Bidding Example

```javascript
// Place a bid
async function placeBid(requestId, bidAmount, message) {
  return apiRequest('/jobs/bids/', {
    method: 'POST',
    body: JSON.stringify({
      request: requestId,
      bid_amount: bidAmount,
      bid_message: message
    })
  });
}

// Get bids for a request
async function getRequestBids(requestId) {
  return apiRequest(`/jobs/bids/?request_id=${requestId}`);
}

// Accept bid
async function acceptBid(bidId) {
  return apiRequest(`/jobs/bids/${bidId}/`, {
    method: 'PUT',
    body: JSON.stringify({ status: 'accepted' })
  });
}
```

### Job Assignment Example

```javascript
// Create assignment (accept bid)
async function acceptBidAssignment(bidId) {
  return apiRequest('/jobs/assignments/', {
    method: 'POST',
    body: JSON.stringify({ bid: bidId })
  });
}

// Update job status
async function updateJobStatus(assignmentId, status) {
  return apiRequest(`/jobs/assignments/${assignmentId}/`, {
    method: 'PUT',
    body: JSON.stringify({ status })
  });
}

// Get my active jobs
async function getMyJobs() {
  return apiRequest('/jobs/assignments/?status=in_progress');
}
```

### Profile Example

```javascript
// Get current profile
async function getProfile() {
  return apiRequest('/profiles/');
}

// Update profile
async function updateProfile(profileData) {
  return apiRequest('/profiles/', {
    method: 'PUT',
    body: JSON.stringify(profileData)
  });
}

// Get another user's profile
async function getUserProfile(userId) {
  return apiRequest(`/profiles/${userId}/`);
}
```

---

## Python Examples

### Using `requests` Library

```python
import requests
import json

API_BASE_URL = 'http://localhost:8000/api'

class SongaAPIClient:
    def __init__(self):
        self.token = None
        self.base_url = API_BASE_URL
    
    def _request(self, method, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        
        response = requests.request(
            method=method,
            url=url,
            json=data,
            headers=headers
        )
        
        response.raise_for_status()
        return response.json() if response.status_code != 204 else None
    
    def register(self, username, email, password, user_type, first_name, last_name):
        data = {
            'username': username,
            'email': email,
            'password': password,
            'password_confirm': password,
            'user_type': user_type,
            'first_name': first_name,
            'last_name': last_name
        }
        return self._request('POST', '/auth/register/', data)
    
    def login(self, username, password):
        data = {'username': username, 'password': password}
        result = self._request('POST', '/auth/login/', data)
        self.token = result['token']
        return result
    
    def logout(self):
        self._request('POST', '/auth/logout/')
        self.token = None
    
    def create_request(self, pickup_location, delivery_location, 
                      pickup_date, delivery_date, description):
        data = {
            'pickup_location': pickup_location,
            'delivery_location': delivery_location,
            'pickup_date': pickup_date,
            'delivery_date': delivery_date,
            'description': description
        }
        return self._request('POST', '/jobs/requests/', data)
    
    def get_requests(self, status=None):
        endpoint = '/jobs/requests/'
        if status:
            endpoint += f'?status={status}'
        return self._request('GET', endpoint)
    
    def place_bid(self, request_id, bid_amount, bid_message):
        data = {
            'request': request_id,
            'bid_amount': bid_amount,
            'bid_message': bid_message
        }
        return self._request('POST', '/jobs/bids/', data)
    
    def get_profile(self):
        return self._request('GET', '/profiles/')
    
    def update_profile(self, phone, address, city, service_area, bio):
        data = {
            'phone': phone,
            'address': address,
            'city': city,
            'service_area': service_area,
            'bio': bio
        }
        return self._request('PUT', '/profiles/', data)

# Usage
client = SongaAPIClient()
client.login('john_mover', 'SecurePass123')

# Create a moving request
request = client.create_request(
    pickup_location='123 Main St, New York, NY',
    delivery_location='456 Oak Ave, Brooklyn, NY',
    pickup_date='2026-03-15',
    delivery_date='2026-03-15',
    description='Moving apartment'
)

# Get all requests
requests = client.get_requests(status='pending')

# Place a bid
bid = client.place_bid(request['id'], 450.00, 'Professional service')

client.logout()
```

---

## Complete Workflow Example

### Customer Workflow (JavaScript)

```javascript
// 1. Register as customer
await register({
  username: 'jane_customer',
  email: 'jane@example.com',
  password: 'SecurePass123',
  password_confirm: 'SecurePass123',
  user_type: 'customer',
  first_name: 'Jane',
  last_name: 'Doe'
});

// 2. Login
await login('jane_customer', 'SecurePass123');

// 3. Create a moving request
const movingRequest = await createRequest({
  pickup_location: '123 Main St, New York, NY',
  delivery_location: '456 Oak Ave, Brooklyn, NY',
  pickup_date: '2026-03-20',
  delivery_date: '2026-03-20',
  description: '2-bedroom apartment move'
});

// 4. Review bids
const bids = await getRequestBids(movingRequest.id);
console.log(`Received ${bids.results.length} bids`);

// 5. Accept best bid
const bestBid = bids.results[0];
await acceptBid(bestBid.id);

// 6. Create job assignment
const assignment = await acceptBidAssignment(bestBid.id);

// 7. Track notifications
const notifications = await apiRequest('/notifications/');
console.log('Unread notifications:', notifications.results.length);
```

### Mover Workflow (JavaScript)

```javascript
// 1. Register as mover
await register({
  username: 'john_mover',
  email: 'john@example.com',
  password: 'SecurePass123',
  password_confirm: 'SecurePass123',
  user_type: 'mover',
  first_name: 'John',
  last_name: 'Smith'
});

// 2. Login
await login('john_mover', 'SecurePass123');

// 3. Update profile with service area
await updateProfile({
  phone: '+1-555-0123',
  address: '789 Pine St, Queens, NY',
  city: 'Queens',
  service_area: 'NYC, Brooklyn, Queens',
  bio: '10+ years moving experience'
});

// 4. View available jobs
const jobs = await getRequests('pending');

// 5. Place bids on interesting jobs
for (const job of jobs.results) {
  if (job.pickup_location.includes('Brooklyn')) {
    await placeBid(job.id, 450.00, 'Available and ready!');
  }
}

// 6. View accepted jobs
const myJobs = await getMyJobs();

// 7. Update job status
const job = myJobs.results[0];
await updateJobStatus(job.id, 'in_progress');

// Later...
await updateJobStatus(job.id, 'completed');
```
