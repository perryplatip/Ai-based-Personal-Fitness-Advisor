AI-Based Personal Fitness Advisor

This project is a web application that provides personalized workout and diet plans using Google Gemini AI. Users enter their fitness details such as age, weight, height, diet preference, and workout goals. The AI generates customized plans and stores them in MongoDB for future reference.

Features

    Personalized workout plan generator
    
    Personalized nutrition and diet planner
    
    Yoga page for flexibility and relaxation
    
    Progress tracking page
    
    Workout timer module
    
    Simple and user-friendly interface

Technologies Used
    
    Python Flask (Backend)
    
    HTML, CSS, JavaScript (Frontend)
    
    Google Gemini AI API (AI Recommendation)
    
    MongoDB (Database)

How It Works

    User fills a form with fitness or nutrition details
    
    Backend sends the data as a prompt to Gemini AI
    
    AI generates a customized plan
    
    The plan is displayed and stored in MongoDB
    
    Installation and Run

Install Python dependencies:

    pip install flask pymongo requests
    
    
    Make sure MongoDB is running:
    
    mongod


Run the Flask app:

    python app.py


Open in browser:

    http://127.0.0.1:5000/

Future Scope

    Login and user authentication
    
    BMI and calorie tracking
    
    Progress charts and analytics
    
    Mobile app development
    
    Pose detection with camera
