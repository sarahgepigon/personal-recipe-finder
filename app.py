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

# Recipes API route - rank recipes based on matching ingredients
@app.route('/recipes', methods=['GET'])
def recipes():
    ingredients_query = request.args.get('ingredients', '')
    selected_ingredients = [ing.strip() for ing in ingredients_query.split(',')]

    # Filter and rank recipes based on the selected ingredients
    ranked_recipes = rank_recipes_by_ingredients(selected_ingredients)
    return jsonify(ranked_recipes)

# Function to fetch all unique ingredients from the database
def get_all_ingredients_from_db():
    conn = sqlite3.connect('recipe_finder.db')
    cursor = conn.cursor()
    cursor.execute("SELECT recipe_ingredients_amounts FROM recipes")
    rows = cursor.fetchall()
    conn.close()

    ingredient_set = set()
    for row in rows:
        ingredients = json.loads(row[0])  # Parse JSON from the database
        for ingredient, details in ingredients.items():
            ingredient_set.add(f"{ingredient}: {details['amount']}")

    return list(ingredient_set)

# Function to rank recipes based on the number of matched ingredients
def rank_recipes_by_ingredients(selected_ingredients):
    conn = sqlite3.connect('recipe_finder.db')
    cursor = conn.cursor()
    cursor.execute("SELECT recipe_name, recipe_ingredients_amounts, recipe_steps FROM recipes")
    recipes = cursor.fetchall()
    conn.close()

    ranked_recipes = []

    for recipe in recipes:
        recipe_name, recipe_ingredients, recipe_steps = recipe
        recipe_ingredients = json.loads(recipe_ingredients)  # Parse JSON ingredients
        recipe_steps = json.loads(recipe_steps)  # Parse JSON steps

        # Create a set of ingredients in the recipe
        recipe_ingredient_set = {f"{ingredient}: {details['amount']}" for ingredient, details in recipe_ingredients.items()}

        # Count how many selected ingredients match the recipe
        matched_ingredients = [ing for ing in selected_ingredients if ing.split(':')[0] in recipe_ingredients]
        num_matched = len(matched_ingredients)
        total_ingredients = len(recipe_ingredients)

        # Only add recipes where at least 1 ingredient matches
        if num_matched > 0:
            ranked_recipes.append({
                "recipe_name": recipe_name,
                "recipe_ingredients_amounts": recipe_ingredients,
                "recipe_steps": recipe_steps,
                "num_matched": num_matched,  # How many ingredients match
                "total_ingredients": total_ingredients  # Total ingredients in the recipe
            })

    # Sort recipes by number of matched ingredients, descending
    ranked_recipes.sort(key=lambda x: x['num_matched'], reverse=True)

    return ranked_recipes

if __name__ == '__main__':
    app.run(debug=True)