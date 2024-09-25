const maxDataPoints = 500;  // Number of data points to show on the chart

// Generalized function to create and update a line chart
function createLineChart(canvasId, label, dataStorage, borderColor, updateFunc) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array(maxDataPoints).fill(''),  // Empty labels for time intervals
            datasets: [{
                label: label,
                data: dataStorage,
                borderColor: borderColor,
                borderWidth: 2,
                fill: true,
                opacity: 0.5,
                tension: 0.6,  // Smooth line
                pointRadius: 0  // Removes the round tip (data points) on the line
            }]
        },
        options: {
            scales: {
                x: {
                    display: false  // Hide the x-axis labels and grid
                },
                y: {
                    display: false,  // Hide the y-axis labels and grid
                    beginAtZero: true,
                    max: 100  // Assuming max value is 100 for CPU and memory usage
                }
            },
            plugins: {
                legend: {
                    display: false  // Hide the legend
                }
            },
            animation: false,  // Disable animation for smooth updates
            responsive: true
        }
    });

    // Function to update the chart with new data
    function updateChart(newUsage) {
        // Add the new data point
        dataStorage.push(newUsage);

        // Keep the data array length within the maxDataPoints
        if (dataStorage.length > maxDataPoints) {
            dataStorage.shift();
        }

        // Update the chart
        chart.update();
    }

    // Set interval to fetch and update data every 2 seconds
    setInterval(() => {
        const newUsage = updateFunc();  // Call the update function to get the current usage
        // console.log(`${label} Usage:`, newUsage);
        updateChart(newUsage);
    }, 300);
}
