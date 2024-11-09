Django Ticketing System
A robust ticketing system built with Django to manage support requests, bug reports, and feature requests efficiently.

Features

User authentication and role-based access control (Admin, Agent, Customer)
Ticket creation with priority levels 
Dashboard with ticket statistics and analytics
Custom ticket workflows

Prerequisites

Python 3.8+
Django 4.2+
PostgreSQL 12+


Installation

Clone the repository

git clone https://github.com/yourusername/django-ticketing.git

cd Televate

Create and activate virtual environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

Configure environment variables

cp .env.example .env
# Edit .env file with your settings

Run migrations

python manage.py migrate

Create superuser

python manage.py createsuperuser

Start development server

python manage.py runserver
Project Structure
Televate/
├── manage.py
├── requirements.txt
├── dashboard/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/
├── Employeees/
│   ├── models.py
│   └── views.py
├── Technicians/
│   ├── serializers.py
│   └── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/
└── static/
    ├── css/
    └── js/
    
Configuration

Database Settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}


Testing
Run the test suite:
python manage.py test


Fork the repository
Create your feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request


Acknowledgments

Django Documentation
Django REST Framework
Bootstrap Templates
Font Awesome Icons
