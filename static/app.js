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

        // Log the selected ingredients
        console.log('Selected Ingredients:', selectedIngredients);
        alert(`Selected Ingredients: ${selectedIngredients.join(', ')}`);
    });
});