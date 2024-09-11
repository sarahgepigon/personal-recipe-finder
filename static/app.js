document.addEventListener("DOMContentLoaded", function () {
    const ingredientsList = document.getElementById('ingredients-list');
    const recipeContainer = document.getElementById('recipe-container');
    const submitButton = document.getElementById('submit-button');

    // Fetch and display all recipes initially in the old style
    fetch('/recipes')  // Adjust this API URL to match your backend
        .then(response => response.json())
        .then(data => {
            displayRecipes(data, []); // Empty array as no ingredients are selected
        })
        .catch(error => {
            console.error('Error fetching initial recipes:', error);
        });

// Fetch and display the ingredients with checkboxes
    fetch('/ingredients')
    .then(response => response.json())
    .then(data => {
        data.forEach(ingredient => {
            const ingredientDiv = document.createElement('div');
            ingredientDiv.classList.add('mb-2');

            const normalizedIngredient = ingredient.trim().toLowerCase();  // Normalize the ingredient here

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.value = normalizedIngredient;
            checkbox.id = normalizedIngredient;

            const label = document.createElement('label');
            label.htmlFor = normalizedIngredient;
            label.textContent = ingredient;

            ingredientDiv.appendChild(checkbox);
            ingredientDiv.appendChild(label);

            ingredientsList.appendChild(ingredientDiv);
        });
    })
    .catch(error => {
        console.error('Error fetching ingredients:', error);
    });

    // Handle submit button click
    submitButton.addEventListener('click', function () {
        const selectedIngredients = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
            .map(checkbox => checkbox.value.trim().toLowerCase());  // Normalize selected ingredients
    
        // Debugging: Print the selected ingredients to make sure they're being captured
        console.log('Selected Ingredients:', selectedIngredients);

        // Fetch filtered recipes based on selected ingredients
        fetch(`/recipes?ingredients=${encodeURIComponent(selectedIngredients.join(','))}`)
            .then(response => response.json())
            .then(data => {
                displayRecipes(data, selectedIngredients);  // Pass selected ingredients for styling
            })
            .catch(error => {
                console.error('Error fetching filtered recipes:', error);
            });
    });

    // Function to dynamically display recipe cards
    function displayRecipes(recipes, selectedIngredients) {
        recipeContainer.innerHTML = '';  // Clear previous results

        const noIngredientsSelected = selectedIngredients.length === 0;

        recipes.forEach(recipe => {
            const recipeCard = document.createElement('div');
            recipeCard.classList.add('recipe-card', 'p-4', 'm-4', 'border', 'rounded-lg', 'transition-all', 'duration-300');

            if (noIngredientsSelected) {
                // Old style: Transparent background, white text, white border
                recipeCard.classList.add('bg-transparent', 'text-white', 'border-white');
                recipeCard.classList.remove('bg-gradient-to-r', 'from-yellow-500', 'via-orange-500', 'to-red-500', 'text-black', 'shadow-lg');
            } else {
                // New style: Gradient background, black text, shadow
                recipeCard.classList.remove('bg-transparent', 'text-white', 'border-white');
                recipeCard.classList.add('bg-gradient-to-r', 'from-yellow-500', 'via-orange-500', 'to-red-500', 'text-black', 'shadow-lg');
            }

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

            const totalIngredients = recipe.total_ingredients;
            const matchedIngredients = selectedIngredients.filter(ingredient => recipe.recipe_ingredients_amounts[ingredient]).length;
            const counterText = `${matchedIngredients} out of ${totalIngredients} ingredients matched`;

            const counterDiv = document.createElement('div');
            counterDiv.classList.add('text-sm', 'text-green-500', 'mt-2');
            counterDiv.textContent = counterText;

            recipeCard.appendChild(recipeName);
            recipeCard.appendChild(ingredientsTitle);
            recipeCard.appendChild(ingredientsList);
            recipeCard.appendChild(stepsTitle);
            recipeCard.appendChild(stepsList);
            recipeCard.appendChild(counterDiv);

            recipeContainer.appendChild(recipeCard);
        });
    }
});