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
- Automatically check submitted notes for spam
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

### 1. Create a virtual environment

Create and activate a Python virtual environment.

### 2. Install dependencies

From the directory containing `requirements.txt`, run:

```bash
pip install -r requirements.txt
