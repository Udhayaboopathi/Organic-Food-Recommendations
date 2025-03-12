import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()



app = Flask(__name__)

print(os.getenv("API_KEY"))
# Set the API key for the Generative AI model   


api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API key not found!")
genai.configure(api_key = api_key)  

def get_food_recommendation(problem):
    """Fetches organic food recommendations from Gemini API in structured format."""
    prompt = f"""
    List the best Indian organic processed foods for {problem} along with their benefits and recipes.
    Provide output in the following structured format:
    
    Food: <Food Name 1>
    Benefits: <Food 1 Benefits>
    Recipe: 
    - Step 1
    - Step 2
    - Step 3
    
    Food: <Food Name 2>
    Benefits: <Food 2 Benefits>
    Recipe: 
    - Step 1
    - Step 2
    - Step 3
    
    Ensure each food has a distinct name, benefits, and a simple step-by-step recipe.
    """
    
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    
    if not response.text:
        return []

    foods = []
    items = response.text.strip().split("\n\n")  # Separate each food item
    
    for item in items:
        lines = item.split("\n")
        food_data = {"food": "", "benefits": "", "recipe": []}
        capturing_recipe = False  # Flag to capture multi-line recipes

        for line in lines:
            line = line.strip()
            if line.startswith("Food:"):
                food_data["food"] = line.replace("Food:", "").strip()
            elif line.startswith("Benefits:"):
                food_data["benefits"] = line.replace("Benefits:", "").strip()
            elif line.startswith("Recipe:"):
                capturing_recipe = True  # Start capturing recipe
                food_data["recipe"] = []  # Reset recipe list
            elif capturing_recipe and line.startswith("- "):  
                # Capture steps that start with "- "
                food_data["recipe"].append(line.replace("- ", "").strip())

        if food_data["food"]:
            foods.append(food_data)

    return foods


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['GET'])
def recommend():
    problem = request.args.get('problem', '').strip()
    if not problem:
        return jsonify({"error": "Please provide a health problem."}), 400
    
    recommendations = get_food_recommendation(problem)

    print(recommendations)
    
    if not recommendations:
        return jsonify({"error": "No recommendations found."}), 404
    
    return jsonify({"recommendations": recommendations})

if __name__ == '__main__':
    app.run(debug=True)
