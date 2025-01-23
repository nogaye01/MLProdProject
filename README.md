# Project Setup

This project is a Machine Learning-based web app that predicts house prices based on various features (e.g., bedrooms, bathrooms, square footage, etc.). The app consists of a FastAPI backend, a React frontend, and a machine learning model trained using Scikit-Learn. It is deployed using Docker and follows a CI/CD pipeline for automated testing and deployment.

## Prerequisites

Before you can run this project, ensure that you have the following installed:

- **Node.js** 
- **npm** 
- **Python** 
- **pip** 
- **docker**
- **git**
- **PostgreSQL** installed locally to be able to install `psycopg2` package

## Setup Instructions

### 1. Environment variables

You need to setup `.env` in the root of both the backend and the frontend folders.

#### Frontend `.env` example

```env
VITE_API_BASE_URL=http://localhost:xxx  # Backend API URL
```

#### Backend `.env` example

```env
DATABASE_URL=postgresql://postgres.xxx 
JWT_SECRET_KEY=xxx
```

### 2. Frontend Setup
Navigate to the `frontend` directory and install the required Node.js dependencies.


```bash
cd frontend
npm install
npm start 
```

### 3. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```


