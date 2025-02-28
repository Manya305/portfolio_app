# Portfolio Website

A dynamic portfolio website built with Flask and Bootstrap, featuring personal details, skills, projects, experience, and contact information.

## Features

- Responsive design using Bootstrap
- Dynamic content management
- Project showcase
- Skills and experience sections
- Contact form
- Admin panel for content management

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a .env file with the following variables:
   ```
   FLASK_APP=app
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///portfolio.db
   ```

5. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Run the application:
   ```bash
   flask run
   ```

Visit http://localhost:5000 to view the website.

## Project Structure

```
portfolio_app/
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/
│   ├── models.py
│   ├── routes.py
│   └── __init__.py
├── migrations/
├── instance/
├── .env
├── requirements.txt
└── README.md
``` 