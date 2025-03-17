// Get references to the profile link and dropdown
const profileLink = document.getElementById('profile-link');
const profileDropdown = document.getElementById('profile-dropdown');

// Toggle dropdown visibility
profileLink.addEventListener('click', (event) => {
    event.preventDefault(); // Prevent default link behavior
    profileDropdown.style.display = profileDropdown.style.display === 'block' ? 'none' : 'block';
});

// Close dropdown if clicked outside
document.addEventListener('click', (event) => {
    if (!profileLink.contains(event.target) && !profileDropdown.contains(event.target)) {
        profileDropdown.style.display = 'none';
    }
});

// Get references to the input field, button, and chart
const mealInput = document.getElementById('meal-input');
const addMealButton = document.getElementById('add-meal-button');
const ctx = document.getElementById('nutritionChart').getContext('2d');

// Initialize the chart
const nutritionChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Calories', 'Proteins', 'Fats', 'Carbs'],
        datasets: [{
            label: 'Nutritional Value',
            data: [10, 10, 10, 10], // Initialize with zeros
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Load the JSON dataset
let dataset = [];

fetch('filtered_dataset.json')
    .then(response => response.json())
    .then(data => {
        dataset = data; // Store the dataset
    })
    .catch(error => {
        console.error('Error loading the dataset:', error);
    });

// Function to update the chart
const updateChart = (mealName) => {
    const meal = dataset.find(item => item['Dish'].toLowerCase() === mealName.toLowerCase());

    if (meal) {
        nutritionChart.data.datasets[0].data = [
            parseFloat(meal['Calories']),
            parseFloat(meal['Proteins (g)']),
            parseFloat(meal['Fats (g)']),
            parseFloat(meal['Carbs (g)'])
        ];
        nutritionChart.update();
    } else {
        // Reset the chart if no meal is found
        nutritionChart.data.datasets[0].data = [0, 0, 0, 0];
        nutritionChart.update();
        alert('Meal not found in the dataset!');
    }
};

// Update the chart when the "Add" button is clicked
addMealButton.addEventListener('click', () => {
    const mealName = mealInput.value.trim();
    if (mealName) {
        updateChart(mealName);
    } else {
        alert('Please enter a meal name!');
    }
});

// Set the link to diet.html with query parameters
const urlParams = new URLSearchParams(window.location.search);
const height = urlParams.get('height');
const weight = urlParams.get('weight');
const age = urlParams.get('age');
const gender = urlParams.get('gender');
const goal = urlParams.get('goal');
const activity = urlParams.get('activity');

const dietLink = document.getElementById('diet-link');
dietLink.href = `diet.html?height=${height}&weight=${weight}&age=${age}&gender=${gender}&goal=${goal}&activity=${activity}`;