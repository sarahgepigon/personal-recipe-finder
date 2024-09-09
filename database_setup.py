import sqlite3
import json

# Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('recipe_finder.db')
cursor = conn.cursor()

# Create a table for storing recipes (if it doesn't exist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_name TEXT NOT NULL,
        created_ts TEXT NOT NULL,
        updated_ts TEXT NOT NULL,
        recipe_ingredients_amounts TEXT NOT NULL,  -- Store ingredients as JSON string
        recipe_steps TEXT NOT NULL  -- Store steps as JSON string
    )
''')

# Sample recipe data to be inserted
recipes = [
    {
        "created_ts": "2023-01-01",
        "updated_ts": "2023-06-01",
        "recipe_name": "Garlic Tomato Pasta",
        "recipe_ingredients_amounts": {
            "Garlic": {"amount": "2 cloves", "required": True},
            "Tomato": {"amount": "1 cup", "required": True},
            "Olive Oil": {"amount": "2 tbsp", "required": False}
        },
        "recipe_steps": {
            "1": "Boil pasta in salted water.",
            "2": "Heat olive oil in a pan.",
            "3": "Saute garlic until golden.",
            "4": "Add tomatoes and cook until soft.",
            "5": "Toss pasta with garlic and tomatoes."
        }
    },
    {
        "created_ts": "2023-02-15",
        "updated_ts": "2023-07-10",
        "recipe_name": "Stuffed Green Peppers",
        "recipe_ingredients_amounts": {
            "Green Pepper": {"amount": "1 large", "required": True},
            "Onion": {"amount": "1/2 cup", "required": True},
            "Cheese": {"amount": "1/4 cup", "required": False}
        },
        "recipe_steps": {
            "1": "Cut the top off the green pepper.",
            "2": "Chop the onion and saute until soft.",
            "3": "Stuff the pepper with onion and cheese mixture.",
            "4": "Bake for 20 minutes."
        }
    }
]

# Insert sample data into the SQLite database
for recipe in recipes:
    # Check if the recipe already exists
    cursor.execute('SELECT * FROM recipes WHERE recipe_name = ?', (recipe['recipe_name'],))
    result = cursor.fetchone()

    if result:
        print(f"Recipe '{recipe['recipe_name']}' already exists in the database. Skipping insertion.")
    else:
        cursor.execute('''
            INSERT INTO recipes (recipe_name, created_ts, updated_ts, recipe_ingredients_amounts, recipe_steps)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            recipe['recipe_name'],
            recipe['created_ts'],
            recipe['updated_ts'],
            json.dumps(recipe['recipe_ingredients_amounts']),  # Convert ingredients to JSON string
            json.dumps(recipe['recipe_steps'])  # Convert steps to JSON string
        ))
        print(f"Inserted recipe '{recipe['recipe_name']}' successfully.")

# Commit the transaction and close the connection
conn.commit()
conn.close()

print("Sample recipes added to SQLite database successfully!")