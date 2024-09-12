from app import db, Recipe, app  # Import the app and db from your Flask app
import sqlite3
import json

# Connect to the existing SQLite database
sqlite_conn = sqlite3.connect('recipe_finder.db')
cursor = sqlite_conn.cursor()

# Fetch all the recipes from SQLite
cursor.execute('SELECT * FROM recipes')
recipes = cursor.fetchall()

# Wrap database operations inside an application context
with app.app_context():
    # Map the SQLite recipe to the new PostgreSQL structure and insert
    for recipe in recipes:
        id, recipe_name, created_ts, updated_ts, recipe_ingredients, recipe_steps = recipe

        # Create a new Recipe object for SQLAlchemy
        new_recipe = Recipe(
            recipe_name=recipe_name,
            created_ts=created_ts,
            updated_ts=updated_ts,
            recipe_ingredients_amounts=json.loads(recipe_ingredients),  # Convert from string to JSON
            recipe_steps=json.loads(recipe_steps)  # Convert from string to JSON
        )

        # Add to PostgreSQL session
        db.session.add(new_recipe)

    # Commit the changes to the PostgreSQL database
    db.session.commit()

# Close SQLite connection
sqlite_conn.close()

print("Data migration completed successfully!")