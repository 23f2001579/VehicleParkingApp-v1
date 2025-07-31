# Vehicle Parking App

## By: Gowri Shankara Narayanan A

### 23f3004197 | Modern Application Development – I | IIT Madras

---

## Project Overview

This project is part of the **Modern Application Development - I** course at **IIT Madras** and focuses on building a multi-user web application for **Vehicle Parking**. It is a multi-user app (one requires an administrator and other users) that manages different parking lots, parking spots and parked vehicles.
 

## Screenshots







### Key Features:
- Customers can request services from their chosen professional.
- Professionals can either accept or reject service requests.
- After service completion, customers can mark the request as closed and provide feedback.
- Admins have full control to create services, manage customer/professional profiles, and more.
- The application is extendable and scalable to integrate additional secure features.

---

## Technologies Used

- **Flask**: Lightweight Python web framework used to build the web application, handle HTTP routes process requests, and render templates.
- **Jinja2**:A powerful templating engine used in Flask to dynamically generate HTML pages using Python variables and logic within .html templates.
- **SQLite3**: A lightweight, file-based relational database used to store data such as users, parking lots, reservations, and more. Ideal for development and smaller-scale apps.
- **SQLAlchemy**: Python SQL toolkit and ORM for interacting with relational databases in an object-oriented way.
- **Flask-Login**: Provides session management and user authentication capabilities, including login, logout, and tracking of current user sessions.
- **Matplotlib**: Used to generate dynamic charts (bar plots, pie charts) for analyzing user behavior and parking lot performance.

- HTML & CSS: Defines the structure and visual presentation of the web pages.
- Bootstrap 5: A modern CSS framework for responsive design. Helps style forms, buttons, layout, and components efficiently.

In addition to these, several other modules and libraries contribute to the functionality and security of this web application.

## Database Schema

**User**: Stores details of people using the system. Differentiates between general users and admins.
**ParkingLot**: Represents each physical parking area. Contains info like location, price, capacity, and address.
**ParkingSpot**: Represents individual slots within a parking lot. Tracks availability and whether the spot is active.
**Reservation**: Central table logging all parking activities. Ties together users, lots, and spots. Records time and cost-related details of each booking.



---

## Architecture

The project follows a modular structure for easy maintainability:
```
.
├── README.md		- Documentation	
├── app.py			- Initializes the flask app 	
├── controllers/			- contains controllers for database, models and routes for all pages
├── db_init.py			- python script for DB initialisation
├── instance/			- contains database
├── requirements.txt		- required models and libraries
├── sample_data	/		- stores dummy data for repopulation	
├── static/
│   ├── img			- folder for charts
│   └── style.css			- stylesheet
├── templates/			- one folder to store all .html files
│   ├── admin/			- admin pages
│   ├── auth/			- login and register pages
│   └── user/			- user pages
└── venv/			- Virtual environment files


```
---

## Installation & Setup

### Requirements:
- Python
- Flask
- Other dependencies mentioned in `requirements.txt`

### Setup Instructions:
1. Clone the repository:
```bash
git clone https://github.com/23f2001579/VehicleParkingApp.git
cd mad1project
 ```
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Linux/MacOS
venv\Scripts\activate     # For Windows
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Create Database:
```bash
python db_init.py
```
5. Run the application:
```bash
python app.py
```

### Sample Data:
To populate the database with sample data for testing, you can use the load_data.py script. This script will insert some sample users, services, and other data into the database.

Run the following command to populate the database:
```bash
python load_data.py
```
The script will automatically add the following sample data:

- A set of Users.
- A set of Parking Lots.
- A set of Parking Spots.

You can modify the createdb.py script to add more sample data as needed.


### Login:
- Admin: 
    - Email: ```admin@user.com ```
    - Password: ```123456```

- User: `http://127.0.0.1:5000/auth/login`
    - Email: ```anshul@user.com ```
    - Password: ```1234```

