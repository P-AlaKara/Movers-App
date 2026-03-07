# Songa API

## Overview

Songa API is a REST API backend for a movers platform that connects customers needing moving services with verified movers. The API handles user authentication, moving request management, bidding systems, job tracking, and notifications. It's designed to serve web and mobile clients.

## API Features

* **Authentication:** Role-based authentication (Customer / Mover) with token-based auth
* **Moving Requests:** CRUD operations for moving requests with location and date details
* **Bidding System:** Movers can place and manage bids on open requests
* **Job Management:** Track job lifecycle (Pending → Accepted → In Progress → Completed)
* **User Profiles:** Manage customer and mover profiles with service area information
* **Notifications:** Real-time notification system for job updates and bid activities

## Tech Stack

* **Backend:** Django with Django REST Framework
* **Database:** SQLite
* **Authentication:** Token-based authentication
* **API Format:** JSON REST API

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Create and Activate a Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Optional but Recommended)

```bash
python manage.py createsuperuser
```

Follow the prompts to create admin credentials.

### 6. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at:

```
http://127.0.0.1:8000/api/
```

## API Endpoints

### Authentication
* `POST /api/auth/register/` - Register a new user
* `POST /api/auth/login/` - Authenticate and receive token
* `POST /api/auth/logout/` - Logout (invalidate token)

### Moving Requests
* `GET /api/jobs/requests/` - List all moving requests
* `POST /api/jobs/requests/` - Create a new moving request
* `GET /api/jobs/requests/<id>/` - Get request details
* `PUT /api/jobs/requests/<id>/` - Update request
* `DELETE /api/jobs/requests/<id>/` - Delete request

### Bids
* `GET /api/jobs/bids/` - List all bids
* `POST /api/jobs/bids/` - Place a bid on a request
* `GET /api/jobs/bids/<id>/` - Get bid details
* `PUT /api/jobs/bids/<id>/` - Update bid status

### Job Assignments
* `GET /api/jobs/assignments/` - List assigned jobs
* `POST /api/jobs/assignments/` - Accept a bid and create job assignment
* `PUT /api/jobs/assignments/<id>/` - Update job status
* `GET /api/jobs/assignments/<id>/` - Get assignment details

### User Profiles
* `GET /api/profiles/` - Get current user profile
* `PUT /api/profiles/` - Update user profile
* `GET /api/profiles/<id>/` - Get specific profile

### Notifications
* `GET /api/notifications/` - List user notifications
* `PUT /api/notifications/<id>/` - Mark notification as read
* `DELETE /api/notifications/<id>/` - Delete notification

## Authentication

All endpoints except authentication endpoints require a bearer token in the Authorization header:

```
Authorization: Token <your-token>
```

## Future Improvements

* WebSocket support for real-time notifications
* Payment integration
* Rating and review endpoints
* Geolocation-based job filtering
* Email/SMS notification endpoints
* Advanced search and filtering
* API rate limiting
* Production deployment (Gunicorn/uWSGI)
