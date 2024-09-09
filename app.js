document.addEventListener("DOMContentLoaded", function() {
    // Fetch all recipes from the backend
    fetch('/recipes')
        .then(response => response.json())
        .then(data => {
            const recipeContainer = document.getElementById('recipe-container');
            
            // Iterate over each recipe and add it to the HTML
            data.forEach(recipe => {
                const recipeCard = document.createElement('div');
                recipeCard.classList.add('recipe-card', 'p-4', 'm-4', 'border', 'rounded-lg', 'shadow-lg');

                const recipeName = document.createElement('h2');
                recipeName.textContent = recipe.recipe_name;
                recipeName.classList.add('text-xl', 'font-bold', 'mb-2');

                const ingredientsTitle = document.createElement('h3');
                ingredientsTitle.textContent = "Ingredients:";
                ingredientsTitle.classList.add('text-lg', 'font-semibold', 'mt-2', 'mb-1');

                const ingredientsList = document.createElement('ul');
                for (let [ingredient, details] of Object.entries(recipe.recipe_ingredients_amounts)) {
                    const listItem = document.createElement('li');
                    listItem.textContent = `${ingredient}: ${details.amount} (Required: ${details.required ? 'Yes' : 'No'})`;
                    ingredientsList.appendChild(listItem);
                }

                const stepsTitle = document.createElement('h3');
                stepsTitle.textContent = "Steps:";
                stepsTitle.classList.add('text-lg', 'font-semibold', 'mt-2', 'mb-1');

                const stepsList = document.createElement('ol');
                for (let [stepNum, stepText] of Object.entries(recipe.recipe_steps)) {
                    const stepItem = document.createElement('li');
                    stepItem.textContent = `${stepNum}: ${stepText}`;
                    stepsList.appendChild(stepItem);
                }

                // Append all elements to the recipe card
                recipeCard.appendChild(recipeName);
                recipeCard.appendChild(ingredientsTitle);
                recipeCard.appendChild(ingredientsList);
                recipeCard.appendChild(stepsTitle);
                recipeCard.appendChild(stepsList);

                // Append the card to the main container
                recipeContainer.appendChild(recipeCard);
            });
        })
        .catch(error => console.error('Error fetching recipes:', error));
});