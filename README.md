# Plant Community Web Application

## Overview
This project is a Flask-based web application designed as a community platform for plant enthusiasts. The application provides features for both registered and unregistered users, allowing them to explore a plant catalog, engage in discussions, and connect with other users in meaningful ways.

## Features

### Public Features
- **Plant Catalog**:
  - Browse a collection of plants with detailed information and images.
  - View comments and discussions related to each plant.

### Registered User Features
- **Commenting System**:
  - Participate in discussions by adding comments to plant entries.
- **Personal Plant Collection**:
  - Add plants to your personal collection using the **"Add to Collection"** button.
  - View your collection on your user profile page.
- **Real-time Chat**:
  - Engage in group discussions using a web-socket-based chat feature.
- **Direct Messaging**:
  - Exchange private messages with other users.
  - Messages are securely stored in the database in encrypted form.

### Admin Features
- **Admin Panel**:
  - Manage the plant catalog (add, update, or delete plant entries).
  - Manage user accounts (view, edit, or deactivate users).

## Technologies Used
- **Backend**: Flask
- **Database**: SQLAlchemy (compatible with PostgreSQL, MySQL, SQLite, etc.)
- **Web Sockets**: Flask-SocketIO for real-time communication
- **Frontend**: Jinja2 templates
- **Admin Interface**: Flask-Admin

## Installation

### Prerequisites
- Python 3.8+
- A virtual environment tool (e.g., `venv` or `virtualenv`)
- A database system (e.g., SQLite, PostgreSQL, or MySQL)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Vaanry/Plant_community.git
   cd Plant_community
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Настройте переменные окружения в файле `.env`:
   ```env
   FLASK_APP=your app name
   FLASK_ENV=development
   DATABASE_URI=your database url
   SECRET_KEY=your secret key
   SESSION_COOKIE_NAME=random name
   ENCRYPTION_KEY=generate your encryption key using Fernet.generate_key()
   ```

5. Set up the database:
   - Update the database URI in `settings.py`.
   - Run migrations:
     ```bash
     flask db upgrade
     ```

6. Start the application:
   ```bash
   flask run
   ```

7. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Development
To run the development environment:
- Enable debugging mode:
  ```bash
  flask run --debug
  ```

## Running Tests
To run the test suite:
```bash
pytest
```
