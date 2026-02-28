# Songa

## Overview

Songa is a web-based platform that connects customers who need moving services with verified movers in their service area. Customers create moving requests and movers place competitive bids. Customers can then review bids, select a mover, and track the job through its lifecycle.

## Features

### Customer Features

* Create moving requests with pickup and delivery details
* View all submitted requests
* Review bids from movers
* Accept a bid and assign the job
* Track job status (Pending → Accepted → In Progress → Completed)
* View notifications

### Mover Features

* View all available jobs within their service area
* Place bids on open requests
* Track assigned jobs
* Update job status
* Filter jobs (including completed jobs)
* View notifications

### Core System Features

* Role-based authentication (Customer / Mover)
* Secure login/logout using Django authentication
* Bidding system
* Notification system 

## Tech Stack

* **Backend:** Django 
* **Database:** SQLite 
* **Frontend:** Django Templates (HTML), Bulma 

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

Open your browser and go to:

```
http://127.0.0.1:8000/
```

## Future Improvements

* Real-time notifications (WebSockets or HTMX)
* Payment integration
* Rating and review system
* Geolocation filtering
* Email/SMS notifications
* Production deployment
