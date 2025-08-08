## Introduction

This project is a client-server application that uses a Python Tkinter desktop app as the client and a Node.js Express API as the backend server. The system's purpose is to allow the user to input a prompt into the desktop app, which then sends the prompt to the backend. The backend uses the Gemini and Mistral APIs to generate a command based on the prompt. This command is sent back to the desktop app, which executes it on the local machine and displays the output. The entire backend is deployed on Render for easy access and scalability.

## Tech Stack

Frontend (Desktop App)
- Python: The core programming language.
- Tkinter: Python's standard GUI library for creating the desktop window.
- requests: A library for making HTTP requests to the backend API.
- subprocess: A built-in Python module for running external commands and capturing their output.

Backend (API)
- Node.js: The JavaScript runtime environment.
- Express.js: A popular framework for building the RESTful API endpoints.
- Gemini API: Used for generating commands from user prompts.
- Mistral API: An alternative or supplementary LLM for generating commands.

Deployment
- Render: The platform used for deploying the Node.js Express application

## Implementation and How to Run

### Backend Setup

First, you'll need to set up the backend. Clone the project repository and install the dependencies using npm install in `backend-server` folder. You'll need to create a .env file and add your Gemini and Mistral API keys and model names. The backend uses these keys to authenticate with the respective LLMs.

### Frontend Setup

To run the desktop app, the easiest method is to download the app.exe file. This file can be found in the `desktop-app/dist/` directory within the project's repository. This pre-packaged executable contains all the necessary Python code and dependencies, allowing you to run the application on a Windows machine without needing to install Python or any libraries. Simply double-click the file to launch the desktop app and connect to the deployed backend.