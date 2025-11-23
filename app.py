from flask import Flask, render_template, request
import requests
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client['workout_db']  # database
workouts_collection = db['workouts'] 
diets_collection = db['diets']   # collection

# Replace with your Gemini API key
GEMINI_API_KEY = "AIzaSyA12WpVsT_zptlEySIU6f-Y0Nn8D9OohUk"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

@app.route("/")
def index():
    return render_template("indexhomepage.html")

@app.route("/LoginUI.html")
def login():
    return render_template("LoginUI.html")

@app.route("/indexhomepage.html")
def homepage():
    return render_template("indexhomepage.html")

@app.route("/progressUI.html")
def progressUI():
    return render_template("progressUI.html")



@app.route("/YOGA.html")
def yoga():
    return render_template("YOGA.html")

@app.route("/nutritionpage.html")
def nutrition():
    return render_template("nut.html")

@app.route("/Communitypage.html")
def community():
    return render_template("Communitypage.html")

@app.route("/TimerModule.html")
def timermodule():
    return render_template("TimerModule.html")

@app.route("/Workout.html")
def workout():
    return render_template("Workout-copy.html")

@app.route("/generate-workout", methods=["POST"])
def generate_workout():
    try:
        workout_level = request.form.get("workout-level")
        workout_type = request.form.get("workout-type")
        goal = request.form.get("goal")
        disability = request.form.get("disability")
        daysperweek = request.form.get("daysperweek")
        age = request.form.get("age")
        weight = request.form.get("weight")
        height = request.form.get("height")

        # Build prompt
        user_prompt = f"""
        Create a short, personalized workout plan.
        Workout Level: {workout_level}
        Workout Type: {workout_type}
        Goal: {goal}
        Disability or Physical Limitation: {disability if disability else "None"}
        Days per Week: {daysperweek}
        Age: {age}
        Weight: {weight} kg
        Height: {height} cm

        Format the response clearly as:
        - **Workout Schedule (Day 1 to Day N)**
        • 3-5 bullet points per day  
        • Include short warm-up, main workout, and quick stretch

        Also add:
        - 2 short fitness tips at the end

        Keep the entire response **concise (under 200 words)**, easy to read, and motivating.
        """

        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": user_prompt}]}]}

        response = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            return render_template("generate_plan.html", plan=f"API Error: {response.text}")

        data = response.json()
        ai_plan = data["candidates"][0]["content"]["parts"][0]["text"]

        # Store in MongoDB
        workout_entry = {
            "workout_level": workout_level,
            "workout_type": workout_type,
            "goal": goal,
            "disability": disability if disability else "None",
            "days_per_week": daysperweek,
            "age": age,
            "weight": weight,
            "height": height,
            "plan": ai_plan,
            "created_at": datetime.datetime.utcnow()
        }
        workouts_collection.insert_one(workout_entry)

        return render_template("generate_workout.html", plan=ai_plan)
    
    except Exception as e:
        return render_template("generate_workout.html", plan=f"Error: {str(e)}")
    
@app.route("/generate_plan", methods=["POST"])
def generate_plan():
    try:
        diet = request.form.get("diet")
        goal = request.form.get("goal")
        allergies = request.form.get("allergies")
        age = request.form.get("age")
        weight = request.form.get("weight")

     
        user_prompt = f"""
        Create a personalized nutrition plan.
        Dietary Preference: {diet}
        Health Goal: {goal}
        Allergies: {allergies if allergies else "None"}
        Age: {age}
        Weight: {weight} kg

        Format the response as:
        - Breakfast
        - Lunch
        - Snacks
        - Dinner

        Each section should include recommended foods, portion sizes, and short explanations.
        Give the diet in bullet points and it should be easier to understand to the reader.
        """

        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": user_prompt}]}]}

        response = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=payload,
            timeout=120
        )

        if response.status_code != 200:
            return render_template("generate_plan.html", plan=f"API Error: {response.text}")
        
        data = response.json()
        ai_plan = data["candidates"][0]["content"]["parts"][0]["text"]
        
        # Store in MongoDB
        plan_entry = {
            "diet": diet,
            "goal": goal,
            "allergies": allergies if allergies else "None",
            "age": age,
            "weight": weight,
            "plan": ai_plan,
            "created_at": datetime.datetime.utcnow()
        }
        diets_collection.insert_one(plan_entry)

       

        return render_template("generate_plan.html", plan=ai_plan)

    except Exception as e:
        return render_template("generate_plan.html", plan=f"Error: {str(e)}")


if __name__ == "__main__":
    app.run(debug=True)
