
# Czech Realities

A FastAPI-based application for managing **Categories**, **Topics**, **Questions**, and **Answers**, with user authentication and an admin interface powered by **sqladmin**.

## Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Technology Stack](#technology-stack)  
4. [Prerequisites](#prerequisites)  
5. [Installation](#installation)  
6. [Configuration](#configuration)  
7. [Database Setup](#database-setup)  
8. [Running the Application](#running-the-application)  
9. [Admin Panel](#admin-panel)  
10. [API Endpoints](#api-endpoints)  
11. [Project Structure](#project-structure)
12. [License](#license)

---

## Overview

This application is designed for creating and managing quizzes or question banks. You can organize **Questions** by **Topics**, which in turn belong to **Categories**. Each question can have multiple **Answers**, and you can mark any number of answers as correct. The project also includes:

- **User authentication** (registration, login) using [FastAPI Users](https://fastapi-users.github.io/fastapi-users/).
- A built-in **admin interface** ([sqladmin](https://github.com/aminalaee/sqladmin)) to manage models.
- Example of how to structure a clean FastAPI application with separate routers, schemas, and CRUD logic.

---

## Features

1. **User Management**  
   - Register new users  
   - Login with JWT-based authentication  
   - Role-based: support for superuser privileges

2. **Admin Dashboard**  
   - Browse, create, edit, and delete Categories, Topics, Questions, and Answers  
   - Basic authentication for admin panel access

3. **Quiz Management**  
   - Random question generation  
   - Random “ticket” (one question per topic)  
   - Linking questions to topics, topics to categories  
   - Handling images (optional) via `image_url`

4. **Validation & Error Handling**  
   - Pydantic models for data validation  
   - Custom messages for errors (e.g., object not found)

---

## Technology Stack

- **[Python 3.10+]**
- **[FastAPI](https://fastapi.tiangolo.com/)** for building web APIs
- **[SQLAlchemy](https://www.sqlalchemy.org/)** for ORM
- **[FastAPI Users](https://fastapi-users.github.io/fastapi-users/)** for user registration & authentication
- **[sqladmin](https://github.com/aminalaee/sqladmin)** for the admin interface
- **[Alembic](https://alembic.sqlalchemy.org/)** (optional if you plan database migrations)
- **[PostgreSQL / SQLite / etc.]** as your relational database (the code can adapt to various engines)

---

## Prerequisites

- **Python 3.10** or higher  
- A running database service (e.g., PostgreSQL) or any other supported SQLAlchemy engine

---

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/IlyaPryzhykau/czech_realities.git
   cd czech_realities
   ```

2. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate       # On Linux / Mac
   .venv\Scripts\activate          # On Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

All main settings are defined in [`.env`](.env) (or environment variables) and read by **Pydantic Settings**. Key variables include:

| Variable                   | Description                                      | Example                       |
|---------------------------|--------------------------------------------------|-------------------------------|
| `APP_TITLE`               | Title of the FastAPI application                | `My Quiz Application`         |
| `DESCRIPTION`             | Description for the FastAPI docs                | `This is a quiz API...`       |
| `DATABASE_URL`            | SQLAlchemy database URL                         | `postgresql+asyncpg://...`    |
| `SECRET`                  | Secret key for JWT and admin auth               | `SOME_RANDOM_SECRET`          |
| `FIRST_SUPERUSER_EMAIL`   | Email for the initial superuser                 | `admin@example.com`           |
| `FIRST_SUPERUSER_PASSWORD`| Password for the initial superuser              | `supersecret`                 |

Make sure to provide a valid database URL. For example, for PostgreSQL with asyncpg driver:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/yourdb
```

---

## Database Setup

If your database is empty, on application startup it will create tables automatically (if using the SQLAlchemy default `create_all`). If you need migrations, configure **Alembic** or a similar tool.

Upon first run, the code calls `create_first_superuser()` to ensure there is at least one superuser account, using the credentials in your `.env`.

---

## Running the Application

1. **Run FastAPI with Uvicorn**:

   ```bash
   uvicorn app.main:app --reload
   ```

   By default, it listens on http://127.0.0.1:8000.

2. **Check the interactive docs** at http://127.0.0.1:8000/docs.

---

## Admin Panel

- The admin interface is served at **`/admin`**.
- Use the **username** = `FIRST_SUPERUSER_EMAIL` and **password** = `FIRST_SUPERUSER_PASSWORD` from your `.env` file to log in.
- Once logged in, you can manage Categories, Topics, Questions, and Answers from a user-friendly UI.

---

## API Endpoints

Below is a brief overview (not exhaustive). For full details, check the **interactive docs** at `/docs`.

- **Auth & Users** (`/auth/jwt`, `/users/`)
  - `POST /auth/jwt/login` - Login with email & password, receive JWT token
  - `POST /auth/register` - Register a new user
  - `GET /users` - List all users (admin required)
- **Categories** (`/category`)
  - `POST /category` - Create new category (superuser required)
  - `GET /category` - List categories
  - `PATCH /category/{id}` - Partially update category (superuser required)
  - `DELETE /category/{id}` - Delete category (superuser required)
- **Topics** (`/topic`)
  - `POST /topic` - Create topic (superuser required)
  - `GET /topic` - List topics
  - `PATCH /topic/{id}` - Update topic (superuser required)
  - `DELETE /topic/{id}` - Delete topic (superuser required)
- **Questions** (`/question`)
  - `POST /question` - Create question (superuser required)
  - `GET /question` - List questions
  - `GET /question/random-one` - Get a random question
  - `GET /question/by-topic/{topic_id}` - Get questions for a topic
  - `GET /question/random-ticket` - Get a random ticket (1 question per topic)
  - `PATCH /question/{id}` - Update question (superuser required)
  - `DELETE /question/{id}` - Delete question (superuser required)
- **Answers** (`/answer`)
  - `POST /answer` - Create answer (superuser required)
  - `GET /answer` - List answers
  - `GET /answer/{id}` - Get answer by id
  - `PATCH /answer/{id}` - Update answer (superuser required)
  - `DELETE /answer/{id}` - Delete answer (superuser required)

---

## Project Structure

A simplified directory layout might look like:

```
.
├── app
│   ├── admin
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── answer.py
│   │   ├── base.py
│   │   ├── category.py
│   │   ├── question.py
│   │   └── topic.py
│   ├── api
│   │   ├── endpoints
│   │   │   ├── __init__.py
│   │   │   ├── answer.py
│   │   │   ├── category.py
│   │   │   ├── constants.py
│   │   │   ├── question.py
│   │   │   ├── topic.py
│   │   │   ├── user.py
│   │   │   ├── validators.py
│   │   │   └── ...
│   │   └── routers.py
│   ├── core
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── init_db.py
│   │   └── user.py
│   ├── crud
│   │   ├── base.py
│   │   ├── answer.py
│   │   ├── category.py
│   │   ├── question.py
│   │   └── topic.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── answer.py
│   │   ├── category.py
│   │   ├── question.py
│   │   ├── topic.py
│   │   └── user.py
│   ├── schemas
│   │   ├── answer.py
│   │   ├── category.py
│   │   ├── question.py
│   │   ├── topic.py
│   │   └── user.py
│   └── main.py
├── .env
├── requirements.txt
└── README.md
```

**Key Directories**:
- **`app/admin`**: Admin configurations using `sqladmin`.
- **`app/api`**: FastAPI routers and endpoint modules.
- **`app/core`**: Core settings, database session, user authentication setup.
- **`app/crud`**: CRUD logic for each model.
- **`app/models`**: SQLAlchemy model definitions.
- **`app/schemas`**: Pydantic schemas for request/response validation.


---

## License


---

