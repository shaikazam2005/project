Smart Parking Management System

Project Overview

The Smart Parking Management System is a web application developed using Python, Django, SQL, HTML, CSS, and JavaScript. It manages vehicle registration, parking-slot allocation, vehicle exits, parking fees, and parking history.

Technologies Used

- Backend: Python, Django
- Database: SQLite (Django default database; update this if you configured another database)
- Frontend: HTML, CSS, JavaScript
- AJAX: Fetch API and JSON responses
- ORM: Django ORM

Main Features

1. User registration, login, and logout
2. Secure, user-specific vehicle and parking history
3. Vehicle registration and validation
4. Automatic allocation of available parking slots
5. Vehicle exit and parking-duration calculation
6. Automatic parking-fee calculation
7. Parking receipt generation
8. Vehicle search and filtering
9. AJAX vehicle search without a full-page reload
10. Dashboard with parking statistics and visit history
11. Django Admin management for vehicles, parking slots, and parking records

Parking Fee Calculation

- Up to 1 hour: ₹20
- Each additional hour or partial hour: ₹10
- Partial hours are rounded up.

Installation and Setup

1. Install Python and Django.

2. Open a terminal in the project directory.

3. Install Django if necessary:
   
   "pip install django"

4. Apply database migrations:
   
   "python manage.py migrate"

5. Create an administrator account:
   
   "python manage.py createsuperuser"

6. Start the development server:
   
   "python manage.py runserver"

7. Open "http://127.0.0.1:8000/parking/" in your browser.

Project Structure

- "parking/models.py" — database models
- "parking/views.py" — application logic
- "parking/forms.py" — forms and validation
- "parking/urls.py" — application routes
- "parking/admin.py" — Django Admin configuration
- "parking/templates/parking/" — HTML templates
- "parking/static/parking/" — CSS and static assets

Learning Outcomes

- Django models, views, templates, and URL routing
- Database relationships and Django ORM queries
- User authentication and access control
- Form validation and error handling
- JavaScript DOM manipulation
- AJAX requests and JSON responses
- Testing and debugging a full-stack web application