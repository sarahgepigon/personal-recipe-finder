document.addEventListener("DOMContentLoaded", function() {
    const ingredientsList = document.getElementById('ingredients-list');
    const submitButton = document.getElementById('submit-button');

    // Fetch and display the ingredients with checkboxes
    fetch('/ingredients')
        .then(response => response.json())
        .then(data => {
            // For each ingredient, create a checkbox with a label
            data.forEach(ingredient => {
                const ingredientDiv = document.createElement('div');
                ingredientDiv.classList.add('mb-2');

                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.value = ingredient;
                checkbox.id = ingredient;

                const label = document.createElement('label');
                label.htmlFor = ingredient;
                label.textContent = ingredient;

                // Append the checkbox and label to the div
                ingredientDiv.appendChild(checkbox);
                ingredientDiv.appendChild(label);

                // Append the div to the ingredients list container
                ingredientsList.appendChild(ingredientDiv);
            });
        })
        .catch(error => {
            console.error('Error fetching ingredients:', error);
        });

    // Handle submit button click
    submitButton.addEventListener('click', function() {
        // Get all checked checkboxes
        const selectedIngredients = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
                                         .map(checkbox => checkbox.value);

        // If no ingredients are selected, alert the user
        if (selectedIngredients.length === 0) {
            alert('Please select at least one ingredient.');
            return;
        }

        // Fetch filtered recipes based on selected ingredients
        fetch(`/recipes?ingredients=${encodeURIComponent(selectedIngredients.join(','))}`)
            .then(response => response.json())
            .then(data => {
                const recipeContainer = document.getElementById('recipe-container');
                recipeContainer.innerHTML = '';  // Clear previous results

                // If no recipes found
                if (data.length === 0) {
                    recipeContainer.innerHTML = '<p class="text-center text-red-500">No recipes found with the selected ingredients.</p>';
                    return;
                }

                // Display each recipe
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
                        listItem.textContent = `${ingredient}: ${details.amount}`;
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

                    console.log(recipe.recipe_steps);  // Check if steps are correctly parsed

                    // Append all elements to the recipe card
                    recipeCard.appendChild(recipeName);
                    recipeCard.appendChild(ingredientsTitle);
                    recipeCard.appendChild(ingredientsList);
                    recipeCard.appendChild(stepsTitle);

                    // Append the card to the main container
                    recipeContainer.appendChild(recipeCard);
                });
            })
            .catch(error => {
                console.error('Error fetching recipes:', error);
            });
    });
});