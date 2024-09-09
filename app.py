from flask import Flask, jsonify, send_file
import sqlite3
import json

app = Flask(__name__)

# Fetch all recipes from the database
def get_all_recipes():
    conn = sqlite3.connect('recipe_finder.db')
    cursor = conn.cursor()
    cursor.execute("SELECT recipe_name, recipe_ingredients_amounts, recipe_steps FROM recipes")
    recipes = cursor.fetchall()
    conn.close()

    recipe_list = []
    for recipe in recipes:
        recipe_list.append({
            "recipe_name": recipe[0],
            "recipe_ingredients_amounts": json.loads(recipe[1]),
            "recipe_steps": json.loads(recipe[2])
        })
    
    return recipe_list

# Route to serve index.html from the root directory
@app.route('/')
def index():
    return send_file('index.html')

# Route to serve app.js from the root directory
@app.route('/app.js')
def serve_js():
    return send_file('app.js')

# API route to get all recipes
@app.route('/recipes', methods=['GET'])
def recipes():
    all_recipes = get_all_recipes()
    return jsonify(all_recipes)

if __name__ == '__main__':
    app.run(debug=True)