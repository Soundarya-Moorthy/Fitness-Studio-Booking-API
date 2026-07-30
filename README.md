# Fitness Studio Booking API

A simple RESTful Booking API for a fictional fitness studio (Yoga, Zumba, HIIT, and more), built with **FastAPI** and **SQLite**. Users can sign up, log in, create classes, book available slots, and view their own bookings — all protected by JWT authentication.

## 📋 Project Overview

This API supports the following core workflows:

- **User authentication** — sign up and log in using JWT-based tokens
- **Class management** — authenticated users can create new fitness classes
- **Browsing** — anyone can view all upcoming classes
- **Booking** — authenticated users can book a slot in a class, with built-in overbooking protection
- **Personal bookings** — authenticated users can view a list of their own bookings

All class times are stored internally in UTC and converted to/from **IST (Indian Standard Time)** at the API boundary, so clients always send and receive times in IST with proper timezone offsets.

## 🛠️ Tech Stack

- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Authentication:** JWT (via `python-jose`), password hashing via `bcrypt`
- **Validation:** Pydantic v2
- **Timezone handling:** `pytz`

## 📁 Project Structure

```
fitness-booking-api/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── config.py
│   └── routers/
│       ├── auth_routes.py
│       ├── classes.py
│       └── bookings.py
├── tests/
├── seed_data.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/fitness-booking-api.git
cd fitness-booking-api
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy the example file and fill in your own secret key:

```bash
cp .env.example .env        # macOS/Linux
copy .env.example .env      # Windows
```

Generate a secure secret key:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Paste the generated value into `.env` as `SECRET_KEY`.

### 5. Seed sample data (optional but recommended)

```bash
python seed_data.py
```

This populates the database with 5 sample fitness classes (Yoga, Zumba, HIIT, Pilates, Spin) so you can test `GET /classes` and `POST /book` immediately.

## 🚀 Running Locally

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **Base URL:** http://127.0.0.1:8000
- **Interactive docs (Swagger UI):** http://127.0.0.1:8000/docs
- **Alternative docs (ReDoc):** http://127.0.0.1:8000/redoc

## 📡 API Usage

All authenticated endpoints require an `Authorization: Bearer <token>` header, obtained from `/login`.

### 1. Sign up

```bash
curl -X POST "http://127.0.0.1:8000/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice",
    "email": "alice@example.com",
    "password": "securepass123"
  }'
```

**Response (201):**
```json
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com"
}
```

### 2. Log in

```bash
curl -X POST "http://127.0.0.1:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@example.com",
    "password": "securepass123"
  }'
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Save the `access_token` — you'll need it for all protected endpoints below.

### 3. Create a class (requires authentication)

```bash
curl -X POST "http://127.0.0.1:8000/classes" \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Yoga Flow",
    "dateTime": "2026-08-15T10:00:00+05:30",
    "instructor": "John Doe",
    "availableSlots": 20
  }'
```

**Response (201):**
```json
{
  "id": 1,
  "name": "Yoga Flow",
  "dateTime": "2026-08-15T10:00:00+05:30",
  "instructor": "John Doe",
  "availableSlots": 20
}
```

> **Note:** `dateTime` must include a timezone offset (e.g. `+05:30` for IST). The API stores it internally as UTC and returns it converted back to IST.

### 4. View all upcoming classes (public)

```bash
curl -X GET "http://127.0.0.1:8000/classes"
```

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Yoga Flow",
    "dateTime": "2026-08-15T10:00:00+05:30",
    "instructor": "John Doe",
    "availableSlots": 20
  }
]
```

### 5. Book a class (requires authentication)

```bash
curl -X POST "http://127.0.0.1:8000/book" \
  -H "Authorization: Bearer <your_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "class_id": 1,
    "client_name": "Alice",
    "client_email": "alice@example.com"
  }'
```

**Response (201):**
```json
{
  "id": 1,
  "class_id": 1,
  "class_name": "Yoga Flow",
  "instructor": "John Doe",
  "dateTime": "2026-08-15T10:00:00+05:30",
  "client_name": "Alice",
  "client_email": "alice@example.com",
  "booked_at": "2026-07-30T09:15:00+00:00"
}
```

**If the class is fully booked (400):**
```json
{
  "detail": "No available slots for this class"
}
```

**If the class doesn't exist (404):**
```json
{
  "detail": "Class not found"
}
```

### 6. View your own bookings (requires authentication)

```bash
curl -X GET "http://127.0.0.1:8000/bookings" \
  -H "Authorization: Bearer <your_access_token>"
```

**Response (200):**
```json
[
  {
    "id": 1,
    "class_id": 1,
    "class_name": "Yoga Flow",
    "instructor": "John Doe",
    "dateTime": "2026-08-15T10:00:00+05:30",
    "client_name": "Alice",
    "client_email": "alice@example.com",
    "booked_at": "2026-07-30T09:15:00+00:00"
  }
]
```

## 🔒 Authentication & Error Handling

| Scenario | Status Code |
|---|---|
| Missing/invalid request fields | `422 Unprocessable Entity` |
| Duplicate email on signup | `400 Bad Request` |
| Wrong email/password on login | `401 Unauthorized` |
| Missing or invalid JWT token | `401 Unauthorized` |
| Booking a non-existent class | `404 Not Found` |
| Booking a fully-booked class | `400 Bad Request` |

## 🕐 Timezone Handling

- All class `dateTime` values are stored in the database as **UTC**.
- Clients must send `dateTime` with an explicit timezone offset when creating a class (e.g. `+05:30` for IST).
- All `dateTime` values returned by the API are converted back to **IST** before being sent to the client.

## 🧪 Running Tests

```bash
pytest tests/
```

## 📝 Design Notes

- **Public class browsing:** `GET /classes` does not require authentication, allowing anyone to browse upcoming classes. Only creating classes, booking, and viewing personal bookings require authentication.
- **Overbooking protection:** Slot availability is checked and decremented within the same database transaction as the booking creation, preventing race conditions from causing overbooking under normal SQLite usage.
- **Password security:** Passwords are hashed using `bcrypt` before storage — plaintext passwords are never persisted.
- **Token expiration:** JWT access tokens expire after 60 minutes by default (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES` in `.env`).
