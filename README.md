# Blog Management System API

# Project Overview

A production-ready Blog Management API built using FastAPI.
This system supports authentication, role-based authorisation, blog management, commenting, and audit logging.

---

# Key Features

*  JWT Authentication (Access + Refresh Tokens)
*  Role-Based Access Control (Admin, Author, User)
*  Blog CRUD Operations
*  Comment System (Create, View, Delete)
*  Audit Logging (Track user actions)
*  FastAPI with automatic API docs
*  Database integration using SQLAlchemy

---

# Tech Stack

| Layer    | Technology        |
| -------- | ----------------- |
| Backend  | FastAPI           |
| Database | MYSQL             |
| ORM      | SQLAlchemy        |
| Auth     | JWT (python-jose) |
| Security | Passlib (bcrypt)  |

---

# Project Structure

```bash
blog_management_system/
│
├── app/
│   ├── core/             
│   │   ├── config.py
│   │   ├── security.py
│   │   └── dependencies.py
│   │
│   ├── models/           
│   │   ├── user.py
│   │   ├── blog.py
│   │   ├── comment.py
│   │   └── audit.py
│   │
│   ├── schemas/           
│   │   ├── user.py
│   │   ├── blog.py
│   │   └── comment.py
│   │
│   ├── routes/            
│   │   ├── auth.py
│   │   ├── blog.py
│   │   ├── comment.py
│   │   └── audit.py
│   │
│   ├── services/          
│   │   ├── auth_service.py
│   │   ├── blog_service.py
│   │   ├── comment_service.py
│   │   └── audit_service.py
│   │
│   ├── database.py        
│   └── main.py            
│
├── .env                   
├── .gitignore
├── requirements.txt
└── README.md
---

# Roles & Permissions

| Role   | Permissions    |
| ------ | -------------- |
| Admin  | Full access    |
| Author | Manage blogs   |
| User   | Comment & view |

---

# Testing

You can test APIs using:

* Swagger UI
* Postman
