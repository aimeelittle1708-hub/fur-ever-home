# 🐾 Fur Ever Home

> A full-stack pet adoption platform built with Django that connects loving homes with pets in need.

Fur Ever Home was created as part of a 16-week full-stack development course to showcase our skills in backend development, frontend design, database modelling, and dynamic user interaction.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [User Stories](#user-stories)
- [Wire Frames](#wireframes)
- [Tech Stack](#tech-stack)
- [Database Models](#database-models)
- [Installation](#installation)
- [Usage](#usage)
- [Future Improvements](#future-improvements)
- [Contributors](#contributors)

---

## 📖 Overview

Fur Ever Home is a web-based adoption platform designed to make finding and adopting pets simple and accessible.

The platform allows users to:
- Browse available pets
- View detailed pet profiles
- Create an account
- Submit adoption requests
- Save favourite pets

Administrators can:
- Add, edit, and remove pet listings
- Manage adoption requests
- Maintain up-to-date records

This project demonstrates full-stack development using Django, HTML, CSS, and JavaScript.

---

## ✨ Features

### 👤 User Features
- User registration and login
- Secure authentication system
- Browse pets by category
- View detailed pet profiles
- Submit adoption requests
- Save favourite pets
- Responsive design for multiple screen sizes

### 🛠 Admin Features
- Create, update, and delete pet listings
- Approve or reject adoption applications
- Manage user accounts

### 💡 Technical Features
- Django ORM and relational database models
- Form validation and error handling
- Dynamic UI updates using JavaScript
- Clean and responsive CSS styling
- Separation of concerns (templates, views, models)

---

## 🧠 User Stories

- As a user, I want to browse pets so that I can find one to adopt.
- As a user, I want to create an account so that I can submit an adoption request.
- As a user, I want to save pets to my favourites so that I can view them later.
- As an admin, I want to manage pet listings so that information stays accurate.
- As an admin, I want to review adoption requests so that I can approve suitable applicants.

---
## Wireframes
<img width="2414" height="1362" alt="image" src="https://github.com/user-attachments/assets/745dfd04-a12e-4977-8c57-e19c370956f4" />


<img width="2416" height="1362" alt="image" src="https://github.com/user-attachments/assets/c21cae74-de09-4d38-96da-f9f5eb9c6eca" />


<img width="826" height="2558" alt="image" src="https://github.com/user-attachments/assets/8858a13a-517b-40eb-8ee5-dc7ea23ac7d4" />


<img width="1608" height="1924" alt="image" src="https://github.com/user-attachments/assets/37e08385-99d7-40e2-a6ad-bd3bc2163ac7" />

---

## 🛠 Tech Stack

### Backend
- Python
- Django

### Frontend
- HTML5
- CSS3
- JavaScript

### Database
- SQLite (development)

### Tools
- Git & GitHub
- VS Code

---

## 🗄 Database Models

### User (Django Authentication)
- username
- email
- password

### Pet
- name
- species
- breed
- age
- description
- image
- available (Boolean)

### AdoptionRequest
- user (ForeignKey)
- pet (ForeignKey)
- status (Pending / Approved / Rejected)
- created_at

### Favourite
- user (ForeignKey)
- pet (ForeignKey)

---

## ⚙ Installation

bash
# Clone the repository
git clone https://github.com/your-username/fur-ever-home.git

# Navigate into the project directory
cd fur-ever-home

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run the development server
python manage.py runserver

Visit the application at:

http://127.0.0.1:8000/
▶ Usage

Register for an account or log in.

Browse available pets.

View pet details.

Submit an adoption request.

Admin users can manage listings and review applications.

🚀 Future Improvements

Messaging system between adopters and shelters

Email notifications for application updates

Advanced filtering and search functionality

Image upload enhancements

Deployment to a live hosting platform

👥 Contributors

Aimee 
Cal
Josh
Wouter

🏆 Project Purpose

Fur Ever Home was created to celebrate the completion of a 16-week full-stack development course and to demonstrate our ability to design and build a fully functional web application using modern web technologies.
