# Love Konnect Backend

A production-ready backend for the Love Konnect dating application built with FastAPI, PostgreSQL, and SQLAlchemy.

## Tech Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT with Passlib bcrypt
- **Migration**: Alembic
- **Server**: Uvicorn

## Project Structure

```
backend/
├── app/
│   ├── api/           # API endpoints
│   │   ├── auth.py    # Authentication endpoints
│   │   ├── users.py   # User management endpoints
│   │   ├── likes.py   # Like system endpoints
│   │   ├── matches.py # Match system endpoints
│   │   └── messages.py # Messaging endpoints
│   ├── core/          # Core configurations
│   │   ├── config.py  # Environment settings
│   │   ├── security.py # JWT & password hashing
│   │   └── database.py # Database connection
│   ├── models/        # SQLAlchemy models
│   │   ├── user.py
│   │   ├── like.py
│   │   ├── match.py
│   │   └── message.py
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic
│   └── main.py        # Application entry point
├── alembic/           # Database migrations
├── requirements.txt   # Python dependencies
├── .env               # Environment variables
├── alembic.ini         # Alembic configuration
└── README.md          # This file
```

## Prerequisites

- Python 3.12+
- PostgreSQL 17+
- pgAdmin 4 (optional, for database management)

## Database Setup

### PostgreSQL Setup

1. **Install PostgreSQL** (if not already installed)
   - Download from: https://www.postgresql.org/download/windows/
   - Or use Chocolatey: `choco install postgresql`

2. **Start PostgreSQL Service**
   ```bash
   # Check if running
   pg_isready -h localhost -p 5432
   
   # If not running, start it
   pg_ctl -D "C:\Program Files\PostgreSQL\17\data" start
   ```

3. **Create Database**
   ```bash
   createdb love_konnect
   ```

### pgAdmin Setup (Optional)

1. Open pgAdmin 4
2. Right-click on "Servers" → "Create" → "Server"
3. Fill in the details:
   - **Name**: Love Konnect
   - **Host**: localhost
   - **Port**: 5432
   - **Username**: postgres
   - **Password**: Your PostgreSQL password
4. Click "Save"

## Virtual Environment Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Environment Configuration

The `.env` file has been created with default values:

```
DATABASE_URL=postgresql://postgres:200712@localhost:5432/love_konnect
SECRET_KEY=love_konnect_secret_key_change_in_production_jd8s7f6h5g4e3r2t1y0u9i8o7p6a5s4d3f2g1h0j
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

**Important**: Change the `SECRET_KEY` in production!

## Database Migrations

```bash
# Initialize Alembic (already done)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

## Running the Server

```bash
# Start the server
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

### Users
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update current user profile
- `GET /api/users/discover` - Discover other users
- `GET /api/users/{user_id}` - Get user by ID

### Likes
- `POST /api/likes/{user_id}` - Like a user

### Matches
- `GET /api/matches` - Get all matches
- `GET /api/matches/{match_id}` - Get specific match

### Messages
- `POST /api/messages/send` - Send a message
- `GET /api/messages/conversation/{user_id}` - Get conversation
- `GET /api/messages/inbox` - Get all messages

## Testing the API

1. Register a user:
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "username": "johndoe",
    "email": "john@example.com",
    "password": "password123",
    "gender": "male",
    "date_of_birth": "1995-05-15"
  }'
```

2. Login:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=password123"
```

3. Use the token to access protected endpoints:
```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Features

- ✅ User Registration & Authentication
- ✅ JWT Token-based Authentication
- ✅ Password Hashing with Bcrypt
- ✅ User Profile Management
- ✅ Like System with Automatic Matching
- ✅ Match Management
- ✅ Real-time Messaging (between matched users)
- ✅ OpenAPI Documentation
- ✅ Alembic Database Migrations

## License

MIT License