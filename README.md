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

### Backend:
- **Flask**: Core framework for routing, request handling, and template rendering.
- **PyJWT**: For creating and verifying JWT tokens for secure authentication and user session management.
- **WTForms**: Prevents CSRF attacks by incorporating CSRF tokens.
- **Requests**: Simplifies API interaction for data sending and receiving.
- **Flask_SQLAlchemy**: Provides seamless integration with databases.
- **Flasgger**: For generating and displaying API documentation via Swagger UI.

### Frontend:
- **HTML, CSS, JS**: Core technologies used for building the frontend of the application.
- **Bootstrap 4**: For responsive design with pre-styled components and a flexible grid system.
- **Chart.js**: For creating interactive, customizable data visualizations.

### Others:
- **Flask_CORS**: For enabling Cross-Origin Resource Sharing (CORS).
- **Flask_Migrate**: For handling database migrations.
- *and more...*
---

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
- Python 3.8+
- Flask
- Other dependencies mentioned in `requirements.txt`

### Setup Instructions:
1. Clone the repository:
```bash
git clone https://github.com/mynkpdr/mad1project.git
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
4. Run the application:
```bash
python app.py
```

### Sample Data:
To populate the database with sample data for testing, you can use the createdb.py script. This script will insert some sample users, services, and other data into the database.

Note*: You need to make sure API is running because it uses API calls to send POST requests.

Run the following command to populate the database:
```bash
python load_data.py
```
The script will automatically add the following sample data:

- An admin user with full access
- A set of categories.
- A set of services.
- A set of professionals.
- A set of customers.
- A set of contacts.
- A set of service requests.
- A set of notification to admin, professionals and customers.
- A set of reviews

You can modify the createdb.py script to add more sample data as needed.


### Login:
- Admin: 
    - Email: ```admin@user.com ```
    - Password: ```123456```

- User: `http://127.0.0.1:5000/auth/login`
    - Email: ```anshul@user.com ```
    - Password: ```1234```

