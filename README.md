
```markdown
# TruckLogger Backend

Welcome to the backend of **TruckLogger**, a full-stack application built with Django and React. This backend processes trip details (current location, pickup location, dropoff location, and current cycle hours) to generate route instructions and Electronic Logging Device (ELD) logs compliant with Hours of Service (HOS) regulations.

This README guides you from initial setup to deployment, covering all steps to get the backend running locally and hosted live.

## Project Overview
The backend uses **Django** and **Django REST Framework** to provide APIs that:
- Accept trip inputs via POST requests.
- Use Nominatim for geocoding and OSRM for route calculation.
- Generate ELD logs based on HOS rules (70hr/8day cycle, property-carrying driver).
- Return structured JSON responses for the frontend.

### Features
- **Trip Processing**: Calculates distances, driving times, and required stops (fuel every 1,000 miles, rest per HOS rules).
- **ELD Log Generation**: Produces daily logs with driving, on-duty, and off-duty periods.
- **API-Driven**: RESTful endpoints for seamless frontend integration.

## Tech Stack
- **Django**: Web framework for rapid development.
- **Django REST Framework (DRF)**: For building RESTful APIs.
- **Nominatim**: Free geocoding API (OpenStreetMap).
- **OSRM**: Open-source routing service.
- **Python**: Core language (v3.8+ recommended).

## Prerequisites
Before starting, ensure you have:
- **Python**: v3.8 or higher (`python --version` to check).
- **pip**: Python package manager (`pip --version` to check).
- **Git**: For cloning the repository (`git --version` to check).
- **Virtualenv**: Recommended for isolated environments (`pip install virtualenv`).
- **Vercel CLI**: For deployment (`npm i -g vercel` if using Vercel).

---

## Setup Instructions (Start to End)

### 1. Clone the Repository
Clone the backend code from GitHub:
```bash
git clone https://github.com/kennedy-273/ELD-BACK.git
cd ELD-BACK
```

Replace your-username with your GitHub username.

2. Set Up a Virtual Environment

Create and activate a virtual environment to isolate dependencies:

bash

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

You’ll see (venv) in your terminal prompt when activated.

3. Install Dependencies

Install the required Python packages:

bash

```bash
pip install -r requirements.txt
```

If requirements.txt doesn’t exist yet, create it with:

```text
django==4.2
djangorestframework==3.14
python-decouple==3.8
requests==2.31
```

Then run pip install -r requirements.txt.

4. Configure Environment Variables

Create a .env file in the root directory to store sensitive settings:






    

5. Initialize the Django Project

If starting from scratch, set up the Django project structure:

bash

```bash
django-admin startproject trucklogger .
cd ELD-BACK
django-admin startapp trips
```

Update trucklogger/settings.py:

python

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'api',
]
```

6. Define Models, Serializers, and Views

Create the backend logic in api/:

-   models.py: Define a Trip model (optional for persistence).
    
-   serializers.py: Create a TripSerializer for input/output.
    
-   views.py: Implement API logic for trip processing.
    


Update api/urls.py and trucklogger/urls.py to include the endpoint.

7. Apply Migrations

Set up the database:

bash

```bash
python manage.py makemigrations
python manage.py migrate
```

8. Run the Development Server

Start the backend locally:

bash

```bash
python manage.py runserver
```

Visit http://localhost:8000/api/trip/ to test with a POST request (use Postman or curl):

json

```json
{
    "current_location": "Nairobi",
    "pickup_location": "Machakso",
    "dropoff_location": "Mombasa",
    "current_cycle": 5
}
```

9. Test the API

Ensure the API returns accurate route data and ELD logs based on:

-   70hr/8day HOS cycle.
    
-   Fueling every 1,000 miles.
    
-   1-hour pickup/dropoff stops.
    

    
-   Update trucklogger/settings.py:
    
    python
    
    ```python
    from decouple import config
    DEBUG = config('DEBUG', default=False, cast=bool)
    SECRET_KEY = config('SECRET_KEY')
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
    ```
    



Deploy the backend:

bash

```bash
vercel --prod
```

-   Follow prompts to link the project.
    
-   Update .env with the production domain in ALLOWED_HOSTS.
    
-   Test the deployed API (e.g., https://your-app.vercel.app/api/trip/).
    

----------

Project Structure

```text
trucklogger-backend/
├── trucklogger/        # Django project
│   ├── __init__.py
│   ├── settings.py     # Configuration
│   ├── urls.py         # Main URL routing
│   └── wsgi.py         # WSGI entry point
├── api/                # API app
│   ├── migrations/     # Database migrations
│   ├── __init__.py
│   ├── models.py       # Models (e.g., Trip)
│   ├── serializers.py  # DRF serializers
│   ├── views.py        # API logic
│   └── urls.py         # API routes
├── manage.py           # Django CLI
├── requirements.txt    # Dependencies
├── .env                # Environment variables
├── vercel.json         # Vercel config
└── README.md           # This file
```

API Endpoints

-   POST /api/trip/
    
    -   Request: { "current_location": "string", "pickup_location": "string", "dropoff_location": "string", "current_cycle": float }
        
    -   Response: { "distance": float, "duration": float, "fuel_stops": int, "rest_stops": int, "logs": [{ "day": int, "driving": float }] }