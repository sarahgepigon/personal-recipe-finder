// Sample ingredient data (for v2 I will fetch this from app.py (databased logic) instead)
const ingredientsList = [
    { name: 'Green Pepper', amount: '1/4 cup' },
    { name: 'Onion', amount: '1/2 cup' },
    { name: 'Garlic', amount: '2 cloves' },
    { name: 'Tomato', amount: '1 cup' }
  ];
  
  // Function to populate the multi-select dropdown
  function populateIngredientDropdown() {
    const ingredientSelect = document.getElementById('ingredients');
    
    ingredientsList.forEach(ingredient => {
      const option = document.createElement('option');
      option.value = JSON.stringify(ingredient); // Store as JSON string
      option.textContent = `${ingredient.name}, ${ingredient.amount}`;
      ingredientSelect.appendChild(option);
    });
  }
  
  // Function to handle recipe search on button click
  async function handleSearch() {
    const ingredientSelect = document.getElementById('ingredients');
    const selectedOptions = Array.from(ingredientSelect.selectedOptions);
    
    // Get the selected ingredients and amounts
    const selectedIngredients = selectedOptions.map(option => JSON.parse(option.value));
  
    // Send the selected ingredients to the backend
    const response = await fetch('/api/search-recipes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ ingredients: selectedIngredients })
    });
  
    const recipes = await response.json();
    displayRecipes(recipes);
  }
  
  // Function to display recipe results
  function displayRecipes(recipes) {
    const recipeResultsDiv = document.getElementById('recipe-results');
    recipeResultsDiv.innerHTML = ''; // Clear previous results
  
    recipes.forEach(recipe => {
      const recipeDiv = document.createElement('div');
      recipeDiv.classList.add('recipe');
  
      const recipeName = document.createElement('h3');
      recipeName.textContent = recipe.recipe_name;
  
      const recipeIngredients = document.createElement('p');
      recipeIngredients.textContent = `Ingredients: ${JSON.stringify(recipe.recipe_ingredients_amounts)}`;
  
      const recipeSteps = document.createElement('p');
      recipeSteps.textContent = `Steps: ${JSON.stringify(recipe.recipe_steps)}`;
  
      recipeDiv.appendChild(recipeName);
      recipeDiv.appendChild(recipeIngredients);
      recipeDiv.appendChild(recipeSteps);
  
      recipeResultsDiv.appendChild(recipeDiv);
    });
  }
  
  // Event listeners
  document.getElementById('search-button').addEventListener('click', handleSearch);
  
  // Populate dropdown when the page loads
  populateIngredientDropdown();