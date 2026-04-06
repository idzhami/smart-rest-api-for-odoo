# 🚀 Smart REST API for Odoo | JWT Auth, Swagger UI, Full CRUD API

**Author:** Usman Idzhami  

---

## 🔥 The Ultimate REST API Solution for Odoo

**Smart REST API for Odoo** is a powerful module designed to help you build secure, scalable, and developer-friendly REST APIs on top of Odoo.

Perfect for:
- Developers
- Software Houses
- Startups
- Enterprises

👉 Seamlessly integrate Odoo with:
- Mobile Apps (Android / iOS)
- Web Apps (React, Vue, Next.js)
- Third-party systems (ERP, Marketplace, Payment Gateway)

---

## ⭐ Key Features

### 🔐 JWT Authentication (Secure API)
- Login & Logout API
- Token validation
- Bearer Authentication support

### 🔄 Full REST API (CRUD Ready)
- GET (List & Detail)
- POST (Create)
- PUT (Update)
- DELETE (Delete)

### 📘 Swagger UI (Interactive API Docs)
- Auto-generated API documentation
- Test API directly from browser
- Built-in Bearer Authorization

### ⚙️ Developer Friendly
- Custom API decorator (`register_endpoint`)
- Clean & modular architecture
- Easy to extend and customize

### 📦 Standard JSON Response
- Consistent response format
- Pagination ready
- Structured error handling

---

## 🚀 Use Cases

- 📱 Mobile App Integration (Flutter, Kotlin, Swift)
- 🌐 Headless Odoo (React / Vue frontend)
- 🔗 Third-party integrations
- 🏢 ERP modernization

---

## 📡 Available API Endpoints

### 🔐 Authentication
- `POST /api/v1/login`  

### 📦 Products API
- `GET /api/v1/products`
- `POST /api/v1/products`
- `PUT /api/v1/products/{id}`
- `DELETE /api/v1/products/{id}`

---

## 🔑 Authentication Flow

1. Login → get JWT token  
2. Use token in header:

Authorization: Bearer <your_token>

3. Access protected endpoints  


---

## 📘 Swagger API Documentation

Access Swagger UI: http://localhost:8069/swagger


Features:
- Interactive API testing
- Input parameters directly
- JWT Authorization support

---

## 🛠️ Installation Guide

### 1. Install Module
- Copy module to addons directory
- Update Apps List
- Install **Smart REST API for Odoo**

---

### 2. Install JWT Library (Required)

This module requires JWT for authentication.

pip install PyJWT

If error occurs:

pip install PyJWT --upgrade


---

### 3. Configure Secret Key

Edit in controller:

```python
SECRET_KEY = "your_secure_secret_key"

```

💼 Why Choose This Module?

✔ Easy to use
✔ No complex configuration
✔ Secure JWT authentication
✔ Swagger documentation included
✔ Production-ready

🏢 About the Author

Developed by Usman Idzhami
ERP Developer & Odoo Specialist

📞 Support : https://www.linkedin.com/in/usman-idzhami-a8a5021b9/
