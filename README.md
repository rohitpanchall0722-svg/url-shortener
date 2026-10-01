# URL Shortener API

A modern URL shortening service built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, and **Pydantic**.

The application allows users to create automatically generated short URLs or custom aliases, redirect users to the original destination, track click counts, retrieve stored URLs, and delete shortened URLs.

---

## Features

* **Automatic URL Shortening**

  * Generates a unique 6-character alphanumeric short code.
  * Handles short-code collisions before storing a new URL.

* **Custom Short URLs**

  * Allows users to create custom aliases.
  * Supports alphanumeric characters, `_`, and `-`.
  * Custom aliases are validated using Pydantic.

* **URL Redirection**

  * Redirects short URLs to their original destination.
  * Uses HTTP `302 Found` redirection.

* **Click Tracking**

  * Automatically increments the click counter whenever a shortened URL is accessed.

* **URL Management**

  * Retrieve all stored shortened URLs.
  * View click statistics.
  * Delete shortened URLs using their database ID.

* **Layered Architecture**

  * Router
  * Service
  * Repository
  * Database
  * Models
  * Schemas

* **Request Validation**

  * Request and response validation using Pydantic.

* **Execution Time Monitoring**

  * Middleware measures request execution time.

* **Security Middleware**

  * `TrustedHostMiddleware`
  * `CORSMiddleware`

* **Global Exception Handling**

  * Centralized handling of HTTP and unexpected application errors.

---

## Tech Stack

| Technology        | Purpose                    |
| ----------------- | -------------------------- |
| Python            | Programming language       |
| FastAPI           | REST API framework         |
| Uvicorn           | ASGI server                |
| SQLAlchemy        | ORM                        |
| PostgreSQL        | Relational database        |
| Psycopg2          | PostgreSQL database driver |
| Pydantic          | Data validation            |
| Pydantic Settings | Environment configuration  |

---

## Architecture

The application follows a layered architecture to separate API handling, business logic, and database operations.

```text
Client
  │
  ▼
FastAPI Router
  │
  ▼
Service Layer
  │
  ▼
Repository Layer
  │
  ▼
SQLAlchemy ORM
  │
  ▼
PostgreSQL
```

### Responsibilities

**Router**

* Receives HTTP requests.
* Validates request data through schemas.
* Sends responses to the client.

**Service**

* Contains business logic.
* Generates short codes.
* Checks short-code collisions.
* Handles click tracking.
* Coordinates repository operations.

**Repository**

* Handles database queries.
* Creates, retrieves, updates, and deletes URL records.

**Model**

* Defines the PostgreSQL database structure through SQLAlchemy.

**Schema**

* Defines request and response validation using Pydantic.

---

## Project Flow

### Creating a Short URL

```text
POST /short_url/create
        │
        ▼
Validate original URL
        │
        ▼
Generate 6-character code
        │
        ▼
Check code uniqueness
        │
        ▼
Store URL in PostgreSQL
        │
        ▼
Return shortened URL
```

### Redirecting a Short URL

```text
GET /short_url/{short_url}
        │
        ▼
Find short URL in database
        │
        ▼
URL found?
   ┌────┴────┐
   │         │
  No        Yes
   │         │
   ▼         ▼
  404    Increment clicks
             │
             ▼
          Commit
             │
             ▼
       HTTP 302 Redirect
             │
             ▼
       Original URL
```

---

## Project Structure

```text
url_shortner/
│
├── app/
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   └── __init__.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── database.py
│   │   └── __init__.py
│   │
│   ├── models/
│   │   ├── url.py
│   │   └── __init__.py
│   │
│   ├── repositories/
│   │   ├── url_repo.py
│   │   └── __init__.py
│   │
│   ├── routers/
│   │   ├── url.py
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   ├── url.py
│   │   └── __init__.py
│   │
│   ├── services/
│   │   ├── url_short.py
│   │   └── __init__.py
│   │
│   └── main.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Database Schema

The application uses a PostgreSQL table named `url_data`.

| Column         | Type      | Constraints           | Description                |
| -------------- | --------- | --------------------- | -------------------------- |
| `id`           | Integer   | Primary Key           | Unique database identifier |
| `original_url` | VARCHAR   | Not Null              | Original destination URL   |
| `short_url`    | VARCHAR   | Unique, Not Null      | Short URL slug             |
| `click_count`  | Integer   | Not Null, Default `0` | Number of redirects        |
| `created_at`   | Timestamp | Not Null              | URL creation timestamp     |

### Example Record

```text
id:           1
original_url: https://fastapi.tiangolo.com/
short_url:    k9A2xL
click_count:  5
created_at:   2026-10-01 22:00:00
```

---

## Environment Configuration

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql+psycopg2://<username>:<password>@<host>:<port>/<database_name>
BASE_URL=http://127.0.0.1:8000
```

### Example

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/urlshorter
BASE_URL=http://127.0.0.1:8000
```

> Do not commit your `.env` file or database credentials to GitHub.

---

# Installation & Setup

## 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd url_shortner
```

---

## 2. Create a Virtual Environment

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create PostgreSQL Database

Make sure PostgreSQL is running.

Create the database:

```sql
CREATE DATABASE urlshorter;
```

Then configure the connection in `.env`.

---

# Running the Application

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

# API Documentation

All URL shortener endpoints use the `/short_url` prefix.

---

## 1. Create Short URL

Generates a random 6-character short code.

### Endpoint

```http
POST /short_url/create
```

### Request

```json
{
  "original_url": "https://fastapi.tiangolo.com/tutorial/"
}
```

### Response

```json
{
  "original_url": "https://fastapi.tiangolo.com/tutorial/",
  "new_url": "http://127.0.0.1:8000/short_url/k9A2xL"
}
```

The generated short code is checked for uniqueness before the record is stored.

---

## 2. Create Custom Short URL

Creates a shortened URL using a user-provided alias.

### Endpoint

```http
POST /short_url/custom_url
```

### Request

```json
{
  "original_url": "https://docs.python.org/3/",
  "custom_url": "python-docs"
}
```

### Response

```json
{
  "original_url": "https://docs.python.org/3/",
  "custom_url": "http://127.0.0.1:8000/short_url/python-docs"
}
```

### Validation

Custom aliases must:

* Contain between 8 and 16 characters.
* Contain only letters, numbers, `_`, or `-`.
* Be unique.

### Example Validation Pattern

```text
^[a-zA-Z0-9_-]+$
```

### Possible Errors

**409 Conflict**

Returned when the requested custom alias already exists.

```json
{
  "detail": "Custom URL already exists"
}
```

**422 Unprocessable Entity**

Returned when the custom alias fails validation.

---

## 3. Redirect to Original URL

Redirects a user from a short URL to its original destination.

### Endpoint

```http
GET /short_url/{short_url}
```

### Example

```text
GET /short_url/k9A2xL
```

### Internal Flow

```text
Short Code
    │
    ▼
Database Lookup
    │
    ▼
Increment click_count
    │
    ▼
Commit Transaction
    │
    ▼
302 Redirect
    │
    ▼
Original URL
```

### Response

```http
302 Found
Location: https://fastapi.tiangolo.com/tutorial/
```

Every successful redirect increases the URL's `click_count`.

### URL Not Found

```http
404 Not Found
```

Example:

```json
{
  "detail": "Short URL not found"
}
```

---

## 4. Retrieve All URLs

Returns all stored shortened URLs and their statistics.

### Endpoint

```http
GET /short_url/all
```

### Example Response

```json
[
  {
    "id": 1,
    "original_url": "https://fastapi.tiangolo.com/tutorial/",
    "short_url": "k9A2xL",
    "click_count": 5,
    "created_at": "2026-10-01T22:00:00"
  },
  {
    "id": 2,
    "original_url": "https://docs.python.org/3/",
    "short_url": "python-docs",
    "click_count": 12,
    "created_at": "2026-10-01T22:05:00"
  }
]
```

---

## 5. Delete Shortened URL

Deletes a shortened URL using its database ID.

### Endpoint

```http
DELETE /short_url/delete/{url_id}
```

### Example

```http
DELETE /short_url/delete/1
```

### Response

```json
{
  "message": "URL deleted successfully",
  "deleted_url": {
    "id": 1,
    "original_url": "https://fastapi.tiangolo.com/tutorial/",
    "short_url": "k9A2xL",
    "click_count": 5,
    "created_at": "2026-10-01T22:00:00"
  }
}
```

### URL Not Found

```http
404 Not Found
```

---

## 6. Home / Health Status

Basic application status endpoint.

### Endpoint

```http
GET /
```

### Response

```json
{
  "message": "URL Shortener API is running"
}
```

---

# Middleware

The application includes several middleware components.

## Trusted Host Middleware

Restricts requests to configured hosts.

Development configuration allows:

```text
127.0.0.1
localhost
```

This helps prevent requests from unexpected host headers.

---

## CORS Middleware

CORS is configured to allow requests from frontend applications.

This is useful when the API and frontend are running on different origins during development.

> For production, allowed origins should be restricted to trusted frontend domains instead of using a wildcard configuration.

---

## Execution Time Middleware

The application includes HTTP middleware that measures request execution time.

The middleware:

```text
Request
   │
   ▼
Start Timer
   │
   ▼
Process Request
   │
   ▼
Response
   │
   ▼
Calculate Execution Time
   │
   ▼
Log Latency
```

This helps during development and performance debugging.

---

# Global Exception Handling

The application uses centralized exception handling for consistent API responses.

Handled cases include:

* `HTTPException`
* Unexpected internal server errors

Example error response:

```json
{
  "detail": "Resource not found"
}
```

Centralizing error handling keeps the API response format consistent across endpoints.

---

# URL Generation

For automatically generated URLs, the application creates a random 6-character alphanumeric slug.

Example:

```text
k9A2xL
TmpgGj
A7xP21
```

The generated code is checked against the database before insertion.

```text
Generate Code
     │
     ▼
Check Database
     │
 ┌───┴────┐
 │        │
Exists   Available
 │        │
 ▼        ▼
Generate  Store
Again     URL
```

This prevents duplicate short URLs.

---

# Custom URL Flow

Users can also provide their own alias.

Example:

```text
Original URL:
https://docs.python.org/3/

Custom Alias:
python-docs

Result:
http://127.0.0.1:8000/short_url/python-docs
```

Before storing the alias, the application checks whether it already exists.

```text
Custom Alias
     │
     ▼
Validate Format
     │
     ▼
Check Database
     │
 ┌───┴────┐
 │        │
Exists   Available
 │        │
 ▼        ▼
409      Store
```

---

# API Summary

| Method   | Endpoint                     | Purpose                   |
| -------- | ---------------------------- | ------------------------- |
| `GET`    | `/`                          | Application status        |
| `POST`   | `/short_url/create`          | Generate random short URL |
| `POST`   | `/short_url/custom_url`      | Create custom short URL   |
| `GET`    | `/short_url/{short_url}`     | Redirect to original URL  |
| `GET`    | `/short_url/all`             | Retrieve all URLs         |
| `DELETE` | `/short_url/delete/{url_id}` | Delete a shortened URL    |

---

# Example Usage

### Create a URL

```http
POST /short_url/create
```

```json
{
  "original_url": "https://www.python.org/"
}
```

Response:

```json
{
  "original_url": "https://www.python.org/",
  "new_url": "http://127.0.0.1:8000/short_url/A7xP21"
}
```

### Open the Short URL

```text
http://127.0.0.1:8000/short_url/A7xP21
```

The API:

```text
Finds A7xP21
      ↓
Increments click_count
      ↓
Saves database change
      ↓
Returns 302 redirect
      ↓
https://www.python.org/
```

---

# Future Improvements

The current project focuses on the core URL-shortening system. Possible future improvements include:

* User registration and authentication
* Login/logout
* JWT authentication
* User-specific URLs
* URL ownership
* Admin dashboard
* Detailed click analytics
* Click history
* Rate limiting
* Redis caching
* QR code generation
* URL expiration
* Custom domains
* Pagination
* Search and filtering
* Background analytics processing
* Docker deployment
* Cloud deployment
* Frontend dashboard

---

# Learning Objectives

This project was built to practice and understand:

* FastAPI REST API development
* SQLAlchemy 2.0
* PostgreSQL integration
* Pydantic validation
* Dependency injection
* Repository pattern
* Service layer architecture
* Database CRUD operations
* HTTP redirects
* Middleware
* Exception handling
* Environment configuration
* API documentation
* Git and GitHub workflow

---

# Project Status

**Current Version:** MVP

The core URL-shortening functionality is implemented, including:

* Random URL generation
* Custom aliases
* URL redirection
* Click tracking
* URL listing
* URL deletion
* Validation
* Middleware
* Exception handling
* PostgreSQL persistence

The project can be extended with authentication, analytics, Redis, rate limiting, and a frontend dashboard in future versions.

---

## Author

**Rohit Panchal**

Backend Developer | Python | FastAPI | PostgreSQL

---

## License

This project is intended for learning and portfolio purposes.
