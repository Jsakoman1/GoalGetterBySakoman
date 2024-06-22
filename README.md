# Financial Goals Tracker

Financial Goals Tracker is a web application built with Flask for managing and tracking financial goals. It allows users to set goals, monitor progress, and update goal details.

## Features

Create, view, edit, and delete financial goals.
Track progress towards each goal.
Simple and intuitive user interface.

## Requirements

Docker

Docker Compose

## Setup Instructions

### Clone the Repository
First, clone the repository to your local machine:

git clone https://github.com/Jsakoman1/GoalGetterBySakoman.git
cd GoalGetterBySakoman


### Build and Run the Docker Containers

docker build -t goalgetter-app .
docker run -d -p 5001:5001 --name goalgetter-container goalgetter-app

### Access the Application
Once the containers are running, the application will be available at: http://localhost:5001

## Usage

Open your web browser and go to http://localhost:5001.
Use the application to add, edit, and manage your financial goals.
Track the progress of each goal and view overall progress.

## Project Structure

The project directory structure is organized as follows:

```plaintext

GoalGetterBySakoman/
├── app.py                  # Main application file
├── docker-compose.yml      # Docker Compose configuration file
├── Dockerfile              # Dockerfile for building the Docker image
├── requirements.txt        # List of Python dependencies
├── static/                 # Folder for static files (CSS, images)
│   └── styles.css          # Custom CSS file
└── templates/              # Folder for HTML templates
    ├── add_goal.html       # Template for adding a new goal
    ├── edit_goal.html      # Template for editing an existing goal
    └── index.html          # Template for displaying goals and progress
