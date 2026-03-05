# 🐾 Fur Ever Home

> A full-stack pet adoption platform built with Django that connects loving homes with pets in need.

Fur Ever Home was created as part of a 16-week full-stack development course to showcase our skills in backend development, frontend design, database modelling, and dynamic user interaction.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [User Stories](#user-stories)
- [Wire Frames](#wireframes)
- [Design](#design)
- [Tech Stack](#tech-stack)
- [Database Models](#database-models)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
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
<br>
<img width="685" height="363" alt="image" src="https://github.com/user-attachments/assets/9eebc08b-d4f9-48e9-b6b8-35136161fa82" />
 <br>
- Browse pets by category
- View detailed pet profiles

<br>
<img width="553" height="617" alt="image" src="https://github.com/user-attachments/assets/20e7508f-044b-4a2e-bdee-abee4c06b00b" />
<br>
- Submit adoption requests

 <br>
- <img width="548" height="682" alt="image" src="https://github.com/user-attachments/assets/e7a90b13-3805-4531-84b0-d302c513bcfa" />
 <br>
- Save favourite pets

 <br>
- <img width="566" height="268" alt="image" src="https://github.com/user-attachments/assets/cd29b958-6e3a-43ca-b12b-6a3c5f4776b1" />
 <br>
 
- Responsive design for multiple screen sizes
 
<br>
Mobile
<br>
<img width="286" height="624" alt="image" src="https://github.com/user-attachments/assets/509440ba-48f1-4f92-986f-8f3fd27fc349" />
 <br>

Large screens and desktops

 <br>
<img width="1163" height="719" alt="image" src="https://github.com/user-attachments/assets/7dcacdff-ac3d-4ea0-b691-39b113524386" />
 <br>

- Approve or reject adoption applications
- Create, update, and delete pet listings
 
-### 🛠 Admin Features 
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
## Design
### Colour Pallet
The Fur Ever Home colour scheme was designed to communicate trust, warmth, and approachability, reflecting the emotional nature of pet adoption. Calming teal tones guide key interactions and establish reliability, while warm neutral colours create a welcoming, home-like feel that aligns with the platform’s purpose. A vibrant orange accent is used strategically for call-to-action elements such as “Adopt Now” buttons, drawing attention to important decisions and encouraging positive user engagement. Accent colours are applied thoughtfully to highlight key actions and system feedback, improving usability and ensuring important features stand out clearly within the interface.
<img width="1035" height="777" alt="image" src="https://github.com/user-attachments/assets/d944a4b8-e542-4bcb-85b0-96992a730218" />
### Fonts
 Google Fonts were used for the headings. We wanted a unique and fun font to help engage our users and tie the website together cohesively.
<img width="653" height="440" alt="image" src="https://github.com/user-attachments/assets/48a980e7-41f1-436a-84fa-a2ea1aa4491f" />

`<style>
@import url('https://fonts.googleapis.com/css2?family=Bubblegum+Sans&display=swap');
</style>`
 
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
- Postgress
- DJ database

### Tools
- Git & GitHub
- VS Code
- Google fonts
- Cloudinary
- Claude AI/ Chat GTP/ Copilot.
- Lucid charts (ERD creation)
- Balsamiq (wireframes)

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
<img width="1062" height="630" alt="image" src="https://github.com/user-attachments/assets/676c1d00-d26e-4c1f-94a1-222d6fcb9d4e" />




---

## ⚙ Installation

bash
#### Clone the repository
git clone https://github.com/your-username/fur-ever-home.git

#### Navigate into the project directory
cd fur-ever-home

#### Create a virtual environment
python -m venv venv

#### Activate the virtual environment
##### Windows
venv\Scripts\activate

##### Mac/Linux
source venv/bin/activate

##### Install dependencies
pip install -r requirements.txt

##### Apply migrations
python manage.py migrate

##### Run the development server
python manage.py runserver

Visit the application at:

http://127.0.0.1:8000/

## ▶ Usage

Register for an account or log in.

Browse available pets.

View pet details.

Submit an adoption request.

Admin users can manage listings and review applications.

## Testing
-W3c HTML Validation- No Errors
<img width="894" height="772" alt="image" src="https://github.com/user-attachments/assets/4fadad00-1292-4110-98ed-8a4eb69ea909" />


-CSS Validation- no errors.

<img width="812" height="356" alt="image" src="https://github.com/user-attachments/assets/11bb1c1e-d016-4a21-91ed-23d7d6abd1f6" />


-Lighthouse Testing.- Shows that our Perfomance and Best Practices are impeaded due to use of Cloudinary and image sizes. 

<img width="424" height="382" alt="image" src="https://github.com/user-attachments/assets/22508c64-b7ac-4fcc-b2e5-022c87501692" />



-Automatic Testing- Unit tests were created for the models, form and views. All came back without errors.



## 🚀 Future Improvements

Messaging system between adopters and shelters

Email notifications for application updates

Advanced filtering and search functionality

Image upload enhancements

Deployment to a live hosting platform

## 👥 Contributors

Aimee 
Cal
Josh
Wouter

## 🏆 Project Purpose

Fur Ever Home was created to celebrate the completion of a 16-week full-stack development course and to demonstrate our ability to design and build a fully functional web application using modern web technologies.
