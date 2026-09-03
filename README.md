# Live Music Notes (LMN)

Live Music Notes is a Django web application for keeping track of live music experiences. Users can browse artists, venues, and shows, create an account, and write notes and ratings about shows they have attended.

The application includes user authentication, an admin interface for managing application data, and an automated spam detection feature for submitted notes using the Gemini API.

## Live Website

Live Music Notes is deployed using Microsoft Azure App Service.

**Live Site:**  
https://ariel-lmn-hcfugqdfc0fwhmds.centralus-01.azurewebsites.net/

## Features

- Browse artists and their information
- Browse music venues
- View live shows and show details
- Create an account and log in
- Create notes about shows
- Rate live music experiences
- View notes submitted by users
- Automatically check submitted notes for spam using the Gemini API
- Manage artists, venues, shows, notes, and users through the Django admin interface

## Technologies Used

- Python
- Django
- SQLite
- HTML
- CSS
- JavaScript
- Gemini API
- Gunicorn
- Microsoft Azure App Service
- GitHub Actions

## Deployment

Live Music Notes is hosted on Microsoft Azure App Service and connected to this GitHub repository using GitHub Actions.

Changes pushed to the `main` branch are automatically built and deployed to the live application.

The deployed application uses a persistent SQLite database for application data.

## About the Project

Live Music Notes was developed as a collaborative web development project. The application demonstrates Django development concepts including models, views, templates, user authentication, database relationships, form handling, automated testing, API integration, and cloud deployment.

This repository is my version of the project and is maintained and deployed through my GitHub account.

## Local Installation

### 1. Create a Virtual Environment

Create and activate a Python virtual environment.

### 2. Install Dependencies

From the directory containing `requirements.txt`, run:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root for local environment variables.

The application supports environment variables including:

```text
DEBUG
SECRET_KEY
GEMINI_API_KEY
```

The `.env` file should not be committed to GitHub.

### 4. Migrate the Database

```bash
python manage.py migrate
```

### 5. Create a Superuser

To access the Django admin interface, create a superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts to create a username and password.

### 6. Run the Development Server

```bash
python manage.py runserver
```

The local site will be available at:

```text
http://127.0.0.1:8000/
```

The Django admin interface will be available at:

```text
http://127.0.0.1:8000/admin/
```

## Initial Data

Fixture files are included for sample artists, venues, shows, and notes.

They are located in:

```text
lmn/fixtures/init_data/
```

The included fixtures are:

```text
init_artists.json
init_venues.json
init_shows.json
init_notes.json
```

Artists, venues, and shows should be loaded before notes because the show data references existing artists and venues.

Example:

```bash
python manage.py loaddata lmn/fixtures/init_data/init_artists.json
python manage.py loaddata lmn/fixtures/init_data/init_venues.json
python manage.py loaddata lmn/fixtures/init_data/init_shows.json
```

The notes fixture references existing users and should only be loaded when the required users exist in the database.

## Testing

Run the full Django test suite with:

```bash
python manage.py test
```

Individual tests or test packages can also be run:

```bash
python manage.py test lmn.tests.test_views
python manage.py test lmn.tests.test_views.TestUserAuthentication
python manage.py test lmn.tests.test_views.TestUserAuthentication.test_user_registration_logs_user_in
```

## Test Coverage

The project uses Coverage to generate test coverage reports.

From the directory containing `manage.py`, run:

```bash
coverage run --source='.' manage.py test lmn.tests
coverage report
```

## Linting

### Python

The project uses Flake8 for Python linting:

```bash
flake8 .
```

### HTML Templates

The project uses djLint for Django template files.

Mac/Linux:

```bash
djlint lmn/templates
```

Windows:

```powershell
djlint lmn\templates
```

## Database

Live Music Notes uses SQLite for local development.

The Azure deployment also uses SQLite with its database stored in Azure's persistent App Service storage.
