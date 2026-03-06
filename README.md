# Fur Ever Home by Aimee, Callum, Josh, Wouter.
---
<img width="690" height="419" alt="image" src="https://github.com/user-attachments/assets/24e520d7-157d-433a-81a6-e6a52f7f6d4d" />

> A full-stack pet adoption platform built with Django that connects loving homes with pets in need.

Fur Ever Home was created as part of a 16-week full-stack development course to showcase our skills in backend development, frontend design, database modelling, and dynamic user interaction.

Live site: `https://fur-ever-home-pets-784e2d19c73a.herokuapp.com/`

Project board: `https://github.com/users/aimeelittle1708-hub/projects/7`

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [User Stories](#user-stories)
- [Wireframes](#wireframes)
- [Design](#design)
- [Tech Stack](#tech-stack)
- [Database Models](#database-models)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Use of AI](#use-of-ai)  
- [Future Improvements](#future-improvements)
- [Contributors](#contributors)

---

## Overview

Fur Ever Home is a web-based adoption platform designed to make finding and adopting pets simple and accessible.

<img width="1145" height="726" alt="image" src="https://github.com/user-attachments/assets/79dd14c3-a9b2-42cf-b9ae-a4c575cbaf63" />


The platform allows users to:

- Browse available pets
- View detailed pet profiles

<img width="1129" height="708" alt="image" src="https://github.com/user-attachments/assets/934a3782-5c8a-41dd-bdb4-78ad28ed1e86" />

<img width="961" height="587" alt="image" src="https://github.com/user-attachments/assets/3b5b310e-21d3-4325-8885-bcb61e6611a6" />
  
- Create an account
  
<img width="415" height="378" alt="image" src="https://github.com/user-attachments/assets/de49167c-2bcf-4b72-ab93-c069655e8a87" />

- Submit adoption requests
- Save favourite pets

<img width="582" height="559" alt="image" src="https://github.com/user-attachments/assets/ccc28a14-6b94-4724-8608-94416b05b04e" />


Administrators can:

- Add, edit, and remove pet listings
- Manage adoption requests
- Maintain up-to-date records

This project demonstrates full-stack development using Django, HTML, CSS, and JavaScript.

---

## Features

### User Features

- User registration and login
- Secure authentication system
- Browse pets by category
- View detailed pet profiles
- Submit adoption requests
- Save favourite pets
- Responsive design for multiple screen sizes

### Admin Features

- Create, update, and delete pet listings
- Approve or reject adoption applications
- Manage user accounts

### Technical Features

- Django ORM and relational database models
- Form validation and error handling
- Dynamic UI updates using JavaScript
- Clean and responsive CSS styling
- Separation of concerns (templates, views, models)

---

## User Stories

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

### Colour Palette

The Fur Ever Home colour scheme was designed to communicate trust, warmth, and approachability, reflecting the emotional nature of pet adoption. Calming teal tones guide key interactions and establish reliability, while warm neutral colours create a welcoming, home-like feel that aligns with the platform's purpose. A vibrant orange accent is used strategically for call-to-action elements such as "Adopt Now" buttons, drawing attention to important decisions and encouraging positive user engagement. Accent colours are applied thoughtfully to highlight key actions and system feedback, improving usability and ensuring important features stand out clearly within the interface.

<img width="1035" height="777" alt="image" src="https://github.com/user-attachments/assets/d944a4b8-e542-4bcb-85b0-96992a730218" />

### Fonts

Google Fonts were used for headings to create a playful and engaging visual identity.

<img width="641" height="442" alt="image" src="https://github.com/user-attachments/assets/5ef7e0ec-8e48-4145-8abb-f95a559c6e28" />

```html
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bubblegum+Sans&display=swap');
</style>
```
---
## Tech Stack

### Backend

- Python
- Django

### Frontend

- HTML5
- CSS3
- JavaScript

### Database

- SQLite (development)
- PostgreSQL (production)
- `dj-database-url`

### Cloud Services

- Cloudinary

### Tools

- Git and GitHub
- VS Code
- Google Fonts
- Lucidchart (ERD creation)
- Balsamiq (wireframes)

---

## Database Models

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

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/fur-ever-home.git

# Navigate into the project directory
cd fur-ever-home

# Create a virtual environment
python -m venv venv

# Activate the virtual environment (Windows)
venv\Scripts\activate

# Activate the virtual environment (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run the development server
python manage.py runserver
```

Visit the application at:

`http://127.0.0.1:8000/`

## Usage

- Register for an account or log in.
- Browse available pets.
- View pet details.
- Submit an adoption request.
- Admin users can manage listings and review applications.

---

## Testing

- W3C HTML validation: no errors.

<img width="593" height="522" alt="image" src="https://github.com/user-attachments/assets/a8c479a5-19d8-47db-8707-202382d30a69" />

- CSS validation: no errors.

<img width="800" height="343" alt="image" src="https://github.com/user-attachments/assets/0510c406-454d-4dae-bbf1-1f506ec3110c" />

- Lighthouse testing: performance and best-practice scores are impacted by Cloudinary usage and image sizes.

<img width="414" height="387" alt="image" src="https://github.com/user-attachments/assets/794d2700-e452-4c71-a115-190178678450" />
  
- Automated testing: unit tests were created for models, forms, and views.

---
## Use of AI 

### AI Tools

AI tools were used to support development in ways aligned with the project goals. Used for Debugging and content generation.

AI Used For:

Drafting example content (pet profiles)
Debugging Django template syntax issues
Improving UX messaging and accessibility improvements

### Reflection

AI accelerated development by reducing time spent on debugging repetitive syntax errors and by helping restructure views/models in a maintainable way. We validated AI suggestions by cross-checking Django documentation and testing changes incrementally in local development before committing.

---

## Future Improvements

- Messaging system between adopters and shelters.
- Email notifications for application updates.
- Advanced filtering and search functionality.
- Image upload enhancements.
- Deployment improvements and observability.

---

## Contributors

- Aimee
- Cal
- Josh
- Wouter

## Project Purpose

Fur Ever Home was created to celebrate the completion of a 16-week full-stack development course and to demonstrate our ability to design and build a fully functional web application using modern web technologies.
