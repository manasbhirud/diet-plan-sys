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


// Get references to the dropdown button, content, and input field
const dropdownButton = document.querySelector('.dropdown-button');
const dropdownContent = document.createElement('div');
dropdownContent.classList.add('dropdown-content');
document.querySelector('.input-container').appendChild(dropdownContent); // Append to input container

const inputField = document.querySelector('.input-field');

// Function to populate dropdown items
const dropdownItems = ['Apple', 'Banana', 'Orange', 'Grapes'];

dropdownItems.forEach(item => {
    const link = document.createElement('a');
    link.href = '#';
    link.textContent = item;
    link.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent page jump
        inputField.value = item; // Set input value
        dropdownContent.style.display = 'none'; // Hide dropdown
    });
    dropdownContent.appendChild(link);
});

// Toggle dropdown visibility
dropdownButton.addEventListener('click', () => {
    dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
});

// Close dropdown if clicked outside
document.addEventListener('click', (event) => {
    if (!dropdownButton.contains(event.target) && !dropdownContent.contains(event.target)) {
        dropdownContent.style.display = 'none';
    }
});

const urlParams = new URLSearchParams(window.location.search);
const height = urlParams.get('height');
const weight = urlParams.get('weight');
const age = urlParams.get('age');
const gender = urlParams.get('gender');
const goal = urlParams.get('goal');
const activity = urlParams.get('activity');

// Set the link to diet.html with query parameters
const dietLink = document.getElementById('diet-link');
dietLink.href = `diet.html?height=${height}&weight=${weight}&age=${age}&gender=${gender}&goal=${goal}&activity=${activity}`;