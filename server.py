from flask import Flask, request, send_file, jsonify
from flask_cors import CORS  # Import CORS
import subprocess
import os


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/generate_meal_plan', methods=['GET'])
def generate_meal_plan():
    height = request.args.get('height')
    weight = request.args.get('weight')
    age = request.args.get('age')
    gender = request.args.get('gender')
    goal = request.args.get('goal')
    activity = request.args.get('activity')

    if not all([height, weight, age, gender, goal, activity]):
        return jsonify({"error": "Missing parameters!"}), 400

    # Debugging: Print received values
    print(f"Received values: height={height}, weight={weight}, age={age}, gender={gender}, goal={goal}, activity={activity}")

    try:
        # Run the Python script and capture output
        result = subprocess.run(["python", "project.py", height, weight, age, gender, activity, goal], capture_output=True, text=True)
        print("Python script output:", result.stdout)
        if result.stderr.strip():
            print("🐍 Python script errors:", result.stderr.strip())

        if result.stderr:
            return jsonify({"error": result.stderr.strip()}), 500  # Return full error


        if result.returncode != 0:
            return jsonify({"error": result.stderr.strip()}), 500  # Show full error

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    pdf_path = "weekly_meal_plan.pdf"
    if not os.path.exists(pdf_path):
        return jsonify({"error": "PDF generation failed!"}), 500

    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
