from flask import Flask, jsonify, render_template
import sqlite3
import json

app = Flask(__name__)

# Serve the frontend (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Ingredients API route
@app.route('/ingredients', methods=['GET'])
def ingredients():
    # Fetch ingredients from the database
    ingredients = get_all_ingredients_from_db()
    return jsonify(ingredients)

# Function to fetch all unique ingredients from the database
def get_all_ingredients_from_db():
    # Connect to SQLite database
    conn = sqlite3.connect('recipe_finder.db')
    cursor = conn.cursor()

    # Query the 'recipes' table to get the ingredients
    cursor.execute("SELECT recipe_ingredients_amounts FROM recipes")
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Collect all ingredients in a set to avoid duplicates
    ingredient_set = set()

    for row in rows:
        # Load the ingredients from the JSON field in the database
        ingredients = json.loads(row[0])
        for ingredient, details in ingredients.items():
            ingredient_set.add(f"{ingredient}: {details['amount']}")

    return list(ingredient_set)

if __name__ == '__main__':
    app.run(debug=True)