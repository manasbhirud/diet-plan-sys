// Data for the charts
const days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'];

const calorieData = [2000, 2100, 1900, 2200, 2300, 2400, 2500];
const proteinData = [50, 55, 60, 65, 70, 75, 80];
const fatsData = [30, 35, 40, 45, 50, 55, 60];
const carbsData = [200, 210, 220, 230, 240, 250, 260];

// Function to create a chart
function createChart(ctx, title, data, backgroundColor) {
  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels: days,
      datasets: [{
        label: title,
        data: data,
        backgroundColor: backgroundColor,
        borderColor: 'rgba(11, 1, 3, 0.6)',
        borderWidth: 2
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      },
      responsive: true,
      plugins: {
        legend: {
          display: false
        },
        title: {
          display: true,
          text: title,
          font: {
            size: 18
          }
        }
      }
    }
  });
}

// Create the charts
const calorieChart = createChart(document.getElementById('calorieChart'), 'Calorie', calorieData, 'rgba(255, 99, 132, 0.6)');
const proteinChart = createChart(document.getElementById('proteinChart'), 'Protein', proteinData, 'rgba(54, 162, 235, 0.6)');
const fatsChart = createChart(document.getElementById('fatsChart'), 'Fats', fatsData, 'rgba(255, 206, 86, 0.6)');
const carbsChart = createChart(document.getElementById('carbsChart'), 'Carbs', carbsData, 'rgba(75, 192, 192, 0.6)');