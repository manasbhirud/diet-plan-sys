// Function to update the height value in the slider
function updateHeightValue() {
    let height = document.getElementById("height").value;
    document.getElementById("heightValue").innerText = height + " cm";
}

// Function to update the weight value in the slider
function updateWeightValue() {
    let weight = document.getElementById("weight").value;
    document.getElementById("weightValue").innerText = weight + " kg";
}

// Function to go to the next step
function nextStep(currentStepId, nextStepId) {
    document.getElementById(currentStepId).style.display = 'none';
    document.getElementById(nextStepId).style.display = 'block';

    // Update progress bar
    let progress = 0;
    if (nextStepId === 'step2') {
        progress = 33;
    } else if (nextStepId === 'step3') {
        progress = 66;
    }
    document.getElementById("progressBar").style.width = progress + "%";
}

// Function to submit the form
function submitForm() {
    let height = document.getElementById("height").value;
    let weight = document.getElementById("weight").value;
    let age = document.getElementById("age").value;
    let gender = document.getElementById("Gender").value;
    let goal = document.getElementById("activity").value;
    let activity = document.getElementById("diet").value;

    // Ensure values are not empty
    if (!height || !weight || !age || !gender || !goal || !activity) {
        alert("Please fill in all fields before submitting.");
        return;
    }

    // Redirect to diet.html with parameters
    window.location.href = `home.html?height=${height}&weight=${weight}&age=${age}&gender=${gender}&goal=${goal}&activity=${activity}`;
}