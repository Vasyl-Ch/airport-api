# ✈️ Airport Service API

A comprehensive RESTful API service for airport and flight management built with Django REST Framework. This system enables complete management of airports, routes, flights, airplanes, crew members, and ticket orders with JWT authentication.

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python Version](https://img.shields.io/badge/python-3.12-blue)
![Django Version](https://img.shields.io/badge/django-6.0-green)
![DRF](https://img.shields.io/badge/DRF-3.x-red)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
  - [Installing using GitHub](#installing-using-github)
  - [Run with Docker](#run-with-docker)
- [Getting Access](#-getting-access)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- **🔐 JWT Authentication**: Secure token-based authentication system
- **👤 User Management**: User registration, login, and profile management
- **🛫 Airport Management**: Create and manage airports with location information
- **🗺️ Route Management**: Define routes between airports with distance tracking
- **✈️ Flight Operations**: Schedule flights with airplane and crew assignments
- **🛩️ Airplane Management**: Track different airplane types, capacities, and configurations
- **👨‍✈️ Crew Management**: Manage flight crew members and assignments
- **🎫 Ticket Booking**: Book tickets with specific seat selection
- **📦 Order Management**: Track user orders and ticket purchases
- **🔍 Advanced Filtering**: Filter flights by source, destination, and date
- **📊 Admin Panel**: Full-featured Django admin interface at `/admin/`
- **📖 Interactive API Documentation**: 
  - Swagger UI available at `/api/doc/swagger/`
  - ReDoc available at `/api/doc/redoc/`
- **🚦 Rate Limiting**: Built-in API throttling for stability
- **🔄 Database Optimization**: Efficient queries with prefetch and select_related

---

## 🛠️ Tech Stack

**Backend Framework:**
- Django 6.0
- Django REST Framework
- Django REST Framework SimpleJWT

**Database:**
- PostgreSQL 15

**API Documentation:**
- drf-spectacular (OpenAPI 3.0)
- Swagger UI
- ReDoc

**Development Tools:**
- Django Debug Toolbar
- Python dotenv

**Containerization:**
- Docker
- Docker Compose

**Programming Language:**
- Python 3.12

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12+** - [Download Python](https://www.python.org/downloads/)
- **PostgreSQL 15+** - [Download PostgreSQL](https://www.postgresql.org/download/)
- **Docker & Docker Compose** (optional, for containerized deployment) - [Download Docker](https://www.docker.com/get-started)
- **Git** - [Download Git](https://git-scm.com/downloads)

---

## 🚀 Installation

### Installing using GitHub

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Y-Havryliv/cinema-API.git
   cd cinema_API
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   ```
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   
   Create a `.env` file in the root directory based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file and configure your database settings:
   ```env
   POSTGRES_DB=your_db_name
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   SECRET_KEY=your_secret_key
   ```

5. **Install and configure PostgreSQL:**
   
   Create a new PostgreSQL database with the credentials from your `.env` file.

6. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Load initial data (optional):**
   ```bash
   python manage.py loaddata exported_data.json
   ```

8. **Create a superuser for admin access:**
   ```bash
   python manage.py createsuperuser
   ```

9. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

---

### Run with Docker

Docker Hub: link for image
https://hub.docker.com/r/kukuruza07/airport_api-app

Docker provides the easiest way to get the application up and running.

1. **Ensure Docker is installed:**
   ```bash
   docker --version
   docker-compose --version
   ```

2. **Clone the repository:**
   ```bash
   git clone https://github.com/Y-Havryliv/cinema-API.git
   cd cinema_API
   ```

3. **Create environment file:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your settings (for Docker, use `POSTGRES_HOST=db`):
   ```env
   POSTGRES_DB=airport_db
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   SECRET_KEY=your-secret-key-here
   ```

4. **Build and start containers:**
   ```bash
   docker-compose build
   docker-compose up
   ```

The API will be available at `http://localhost:8000/`

**Docker Commands:**
- Stop containers: `docker-compose down`
- View logs: `docker-compose logs -f`
- Rebuild containers: `docker-compose up --build`
- Run migrations: `docker-compose exec app python manage.py migrate`
- Create superuser: `docker-compose exec app python manage.py createsuperuser`

---

## 🔑 Getting Access

User
```json
{
  "email": "user@airport.com",
  "password": "user123"
}
```

Admin
```json
{
  "email": "admin@airport.com",
  "password": "admin123"
}
```
To access the API functionality, you need to authenticate:

### 1. Register a new user

**Endpoint:** `POST /api/user/register/`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

### 2. Obtain access token

**Endpoint:** `POST /api/user/token/`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 3. Use the access token

Include the token in the Authorization header for all subsequent requests:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 4. Access admin panel (for staff users)

Navigate to `http://localhost:8000/admin/` and login with superuser credentials.

**Note:** Some endpoints require admin privileges. Regular authenticated users have read-only access to most endpoints, while creating, updating, and deleting resources requires admin rights.

---

## 📖 API Documentation

Once the server is running, you can access the interactive API documentation:

- **Swagger UI:** [http://localhost:8000/api/doc/swagger/](http://localhost:8000/api/doc/swagger/)
- **ReDoc:** [http://localhost:8000/api/doc/redoc/](http://localhost:8000/api/doc/redoc/)
- **OpenAPI Schema:** [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

### Main API Endpoints

**Authentication:**
- `POST /api/user/register/` - Register new user
- `POST /api/user/token/` - Obtain JWT token
- `POST /api/user/token/refresh/` - Refresh JWT token
- `POST /api/user/token/verify/` - Verify JWT token
- `GET/PUT/PATCH /api/user/me/` - Manage current user profile

**Airports:**
- `GET /api/airports/airports/` - List all airports
- `POST /api/airports/airports/` - Create airport (admin only)
- `GET /api/airports/airports/{id}/` - Retrieve airport details
- `PUT/PATCH /api/airports/airports/{id}/` - Update airport (admin only)
- `DELETE /api/airports/airports/{id}/` - Delete airport (admin only)

**Routes:**
- `GET /api/airports/routes/` - List all routes
- `POST /api/airports/routes/` - Create route (admin only)
- `GET /api/airports/routes/{id}/` - Retrieve route details
- `PUT/PATCH /api/airports/routes/{id}/` - Update route (admin only)
- `DELETE /api/airports/routes/{id}/` - Delete route (admin only)

**Flights:**
- `GET /api/flights/list-flights/` - List flights (supports filtering)
- `POST /api/flights/list-flights/` - Create flight (admin only)
- `GET /api/flights/list-flights/{id}/` - Retrieve flight details
- `PUT/PATCH /api/flights/list-flights/{id}/` - Update flight (admin only)
- `DELETE /api/flights/list-flights/{id}/` - Delete flight (admin only)

**Query Parameters for Flights:**
- `?source=city` - Filter by source airport
- `?destination=city` - Filter by destination airport
- `?date=YYYY-MM-DD` - Filter by departure date

**Airplanes:**
- `GET /api/flights/list-airplanes/` - List all airplanes
- `POST /api/flights/list-airplanes/` - Create airplane (admin only)
- `GET /api/flights/list-airplanes/{id}/` - Retrieve airplane details

**Crew:**
- `GET /api/flights/list-crew/` - List crew members (admin only)
- `POST /api/flights/list-crew/` - Create crew member (admin only)

**Orders:**
- `GET /api/orders/orders/` - List user's orders
- `POST /api/orders/orders/` - Create new order with tickets
- `GET /api/orders/orders/{id}/` - Retrieve order details

---

## 📁 Project Structure

```
cinema_API/
│
├── airports/              # Airport and route management
│   ├── models.py         # Airport, Route models
│   ├── serializers.py    # API serializers
│   ├── views.py          # ViewSets for airports and routes
│   └── admin.py          # Admin configuration
│
├── flights/              # Flight and airplane management
│   ├── models.py         # Airplane, AirplaneType, Crew, Flight models
│   ├── serializers.py    # API serializers
│   ├── views.py          # ViewSets for flights
│   └── admin.py          # Admin configuration
│
├── orders/               # Order and ticket management
│   ├── models.py         # Order, Ticket models
│   ├── serializers.py    # API serializers
│   ├── views.py          # ViewSets for orders
│   └── admin.py          # Admin configuration
│
├── users/                # User authentication and management
│   ├── models.py         # Custom User model
│   ├── serializers.py    # User serializers
│   ├── views.py          # User views
│   └── admin.py          # User admin
│
├── config/               # Project configuration
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL configuration
│   ├── permissions.py    # Custom permissions
│   └── wsgi.py           # WSGI configuration
│
├── manage.py             # Django management script
├── requirements.txt      # Project dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yaml   # Docker Compose configuration
├── .env.example          # Environment variables template
└── .gitignore           # Git ignore file
```

---

## 🤝 Contributing

Contributions are welcome! If you'd like to contribute to this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please see `CONTRIBUTING.md` for detailed contribution guidelines.

---

## 📄 License

This project is distributed under the **MIT License**. See `LICENSE` file for more information.

---

## 📧 Contact

For questions or support, please open an issue on GitHub or contact the maintainer.

**Project Link:** [https://github.com/Vasyl-Ch/airport-api](https://github.com/Vasyl-Ch/airport-api)

---

**Made with ❤️ using Django REST Framework**