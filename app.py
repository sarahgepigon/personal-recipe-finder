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
    # Split and strip selected ingredients, only keeping the part before the colon (i.e., the ingredient name)
    selected_ingredients = [ing.split(':')[0].strip().lower() for ing in ingredients_query.split(',') if ing.strip()]

    # Debugging: Print the selected ingredients to make sure the backend is receiving them correctly
    print('Selected Ingredients:', selected_ingredients)

    # If no ingredients are selected, return all recipes
    if not selected_ingredients:  
        recipes = get_recipes_from_db()  # Fetch all recipes if no ingredients are selected
    else:
        recipes = rank_recipes_by_ingredients(selected_ingredients)  # Filter recipes based on selected ingredients

    return jsonify(recipes)

# Function to fetch all recipes (if no ingredients are selected)
def get_recipes_from_db():
    conn = sqlite3.connect('recipe_finder.db')
    cursor = conn.cursor()

    # Fetch recipe names, ingredients (JSON), and steps (JSON)
    cursor.execute("SELECT recipe_name, recipe_ingredients_amounts, recipe_steps FROM recipes")
    recipes = cursor.fetchall()

    formatted_recipes = []
    for recipe in recipes:
        recipe_name = recipe[0]
        ingredients_json = recipe[1]
        steps_json = recipe[2]

        # Parse the JSON strings into Python dictionaries
        ingredients = json.loads(ingredients_json)
        steps = json.loads(steps_json)

        formatted_recipes.append({
            'recipe_name': recipe_name,
            'recipe_ingredients_amounts': ingredients,
            'recipe_steps': steps,
            'total_ingredients': len(ingredients)  # Calculate total ingredients
        })

    conn.close()

    return formatted_recipes

# Function to fetch all unique ingredients from the database
def get_all_ingredients_from_db():
    conn = sqlite3.connect('recipe_finder.db')
    cursor = conn.cursor()

    # Fetch the ingredients JSON column
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

    # Strip and normalize selected ingredients
    selected_ingredient_names = {ing.split(':')[0].strip().lower() for ing in selected_ingredients}
    print(f"Selected ingredients for matching: {selected_ingredient_names}")  # Debugging

    for recipe in recipes:
        recipe_name, recipe_ingredients, recipe_steps = recipe
        recipe_ingredients = json.loads(recipe_ingredients)  # Parse JSON ingredients
        recipe_steps = json.loads(recipe_steps)  # Parse JSON steps

        # Normalize ingredient names (strip spaces and convert to lowercase)
        recipe_ingredient_names = {ingredient.strip().lower() for ingredient in recipe_ingredients.keys()}
        print(f"\nRecipe: {recipe_name}")
        print(f"Ingredients in recipe: {recipe_ingredient_names}")

        # Find matching ingredients
        matched_ingredients = selected_ingredient_names.intersection(recipe_ingredient_names)
        num_matched = len(matched_ingredients)
        total_ingredients = len(recipe_ingredient_names)

        print(f"Matched ingredients: {matched_ingredients}")
        print(f"Number of matched ingredients: {num_matched}")
        print(f"Total ingredients in recipe: {total_ingredients}")

        # Only include recipes where at least 1 ingredient matches
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