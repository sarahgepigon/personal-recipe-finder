from flask import Flask, jsonify, render_template, request
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
    ingredients = get_all_ingredients_from_db()
    return jsonify(ingredients)

# Recipes API route - filter recipes by ingredients
@app.route('/recipes', methods=['GET'])
def recipes():
    ingredients_query = request.args.get('ingredients', '')
    selected_ingredients = [ing.strip() for ing in ingredients_query.split(',')]

    # Filter recipes based on the selected ingredients
    filtered_recipes = filter_recipes_by_ingredients(selected_ingredients)
    return jsonify(filtered_recipes)

# Function to fetch all unique ingredients from the database
def get_all_ingredients_from_db():
    conn = sqlite3.connect('recipe_finder.db')
    cursor = conn.cursor()
    cursor.execute("SELECT recipe_ingredients_amounts FROM recipes")
    rows = cursor.fetchall()
    conn.close()

    ingredient_set = set()
    for row in rows:
        ingredients = json.loads(row[0])
        for ingredient, details in ingredients.items():
            ingredient_set.add(f"{ingredient}: {details['amount']}")

    return list(ingredient_set)

# Function to filter recipes based on selected ingredients
def filter_recipes_by_ingredients(selected_ingredients):
    conn = sqlite3.connect('recipe_finder.db')
    cursor = conn.cursor()
    cursor.execute("SELECT recipe_name, recipe_ingredients_amounts, recipe_steps FROM recipes")
    recipes = cursor.fetchall()
    conn.close()

    matching_recipes = []

    for recipe in recipes:
        recipe_name, recipe_ingredients, recipe_steps = recipe
        recipe_ingredients = json.loads(recipe_ingredients)
        
        # Create a set of ingredients in the recipe
        recipe_ingredient_set = {f"{ingredient}: {details['amount']}" for ingredient, details in recipe_ingredients.items()}
        
        # Check if all selected ingredients are present in the recipe's ingredients
        if all(ingredient in recipe_ingredient_set for ingredient in selected_ingredients):
            matching_recipes.append({
                "recipe_name": recipe_name,
                "recipe_ingredients_amounts": recipe_ingredients,
                "recipe_steps": json.loads(recipe_steps)
            })

    return matching_recipes

if __name__ == '__main__':
    app.run(debug=True)