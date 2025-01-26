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
- **supabase**

## Setup Instructions

### 1. Environment variables

You need to setup `.env` in the root of the backend folder.

#### Backend `.env` example

```env
MLFLOW_TRACKING_URI=https://dagshub.com/###/####.mlflow
MLFLOW_EXPERIMENT_NAME=#####

AWS_ACCESS_KEY_ID=#######
AWS_SECRET_ACCESS_KEY=########
AWS_BUCKET_NAME=s3://########
AWS_REGION=##-####-#

DAGSHUB_TOKEN=#########
DAGSHUB_USERNAME=######

SUPABASE_URL=https://##########.supabase.co
SUPABASE_KEY=################
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


