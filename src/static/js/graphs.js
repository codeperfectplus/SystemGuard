// Variables to store chart instances
let cpuTimeChart, memoryTimeChart, batteryTimeChart, networkTimeChart, dashboardMemoryTimeChart, cpuFrequencyTimeChart, currentTempTimeChart;

// Function to fetch data and render charts
function fetchDataAndRenderCharts() {
    // Retrieve stored filter value from local storage or set default value
    const storedFilterValue = localStorage.getItem('filterValue') || 5;

    // Set the filter element value to the stored filter value
    document.getElementById('timeFilter').value = storedFilterValue;

    console.log('Stored Filter Value:', storedFilterValue);

    // Fetch data with the selected time filter
    fetch(`/api/v1/prometheus/graphs_data?filter=${storedFilterValue}`)
        .then(response => response.json())
        .then(data => {
            const cpuData = data.cpu;
            const memoryData = data.memory;
            const batteryData = data.battery;
            const networkSentData = data.network_sent;
            const networkReceivedData = data.network_received;
            const dashboardMemoryUsageData = data.dashboard_memory_usage;
            const cpuFrequencyData = data.cpu_frequency;
            const currentTempData = data.current_temp;
            const currentTime = data.current_time;
            const timeZoneName = Intl.DateTimeFormat().resolvedOptions().timeZone;

            // Format the time data using the currentTime from backend
            const timeData = data.time.map(time => formatDate(time, currentTime));

            displayTimeAndTimeZone(currentTime, timeZoneName);

            createCharts(cpuData, timeData, memoryData, batteryData, networkSentData, networkReceivedData, dashboardMemoryUsageData, cpuFrequencyData, currentTempData);
        })
        .catch(error => console.error('Error fetching data:', error));
}

// Add event listener to refresh data when filter value changes
document.getElementById('timeFilter').addEventListener('change', (event) => {
    // Save the new filter value to local storage
    localStorage.setItem('filterValue', event.target.value);
    // Fetch data with the new filter value
    fetchDataAndRenderCharts();
});

// Initial fetch when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchDataAndRenderCharts();
});

// Add the refresh button to fetch the data
document.getElementById('refreshData').addEventListener('click', () => {
    fetchDataAndRenderCharts();
});

document.getElementById('refreshCpuTime').addEventListener('click', () => {
    fetchDataAndRenderCharts();
});

document.getElementById('refreshMemoryTime').addEventListener('click', () => {
    fetchDataAndRenderCharts();
});

document.getElementById('refreshBatteryTime').addEventListener('click', () => {
    fetchDataAndRenderCharts();
});

document.getElementById('refreshNetworkTime').addEventListener('click', () => {
    fetchDataAndRenderCharts();
});

document.getElementById('refreshDashboardMemoryTime').addEventListener('click', () => {
    fetchDataAndRenderCharts();
});

document.getElementById('refreshCpuFrequencyTime').addEventListener('click', () => {
    fetchDataAndRenderCharts();
});

document.getElementById('refreshCurrentTempTime').addEventListener('click', () => {
    fetchDataAndRenderCharts();
});


function formatDate(dateString, currentTime) {
    const date = new Date(dateString);
    const now = new Date(currentTime);  // Use currentTime from backend

    // Helper function to format with leading zeros
    const pad = (num) => String(num).padStart(2, '0');

    // Manually extract UTC components
    const day = pad(date.getUTCDate()); // e.g., 09
    const month = pad(date.getUTCMonth() + 1); // e.g., 04
    const year = date.getUTCFullYear(); // e.g., 2021
    const hours = pad(date.getUTCHours()); // e.g., 11
    const minutes = pad(date.getUTCMinutes()); // e.g., 33


    // Calculate time differences
    const diffDays = Math.floor((now - date) / (1000 * 60 * 60 * 24));
    const diffWeeks = Math.floor(diffDays / 7);
    const diffMonths = now.getMonth() - date.getUTCMonth() + (12 * (now.getFullYear() - date.getUTCFullYear()));
    const diffYears = now.getFullYear() - date.getUTCFullYear();

    // Determine the label based on time differences
    // // Reset the time to 12am for the date comparison
    // date.setUTCHours(0, 0, 0, 0);
    // now.setUTCHours(0, 0, 0, 0);

    // if (diffDays === 0) {
    //     return `Today ${hours}:${minutes}`;
    // } else if (diffDays === 1) {
    //     return `Yesterday ${hours}:${minutes}`;
    // } else if (diffDays <= 3) {
    //     return `${diffDays} Days Ago ${hours}:${minutes}`;
    // } else if (diffDays <= 7) {
    //     return `${Math.ceil(diffDays / 7)} Week${diffDays > 7 ? 's' : ''} Ago ${hours}:${minutes}`;
    // } else if (diffDays <= 30) {
    //     return `${Math.ceil(diffDays / 7)} Weeks Ago ${hours}:${minutes}`;
    // } else if (diffMonths < 12) {
    //     return `${diffMonths} Month${diffMonths > 1 ? 's' : ''} Ago ${hours}:${minutes}`;
    // } else if (diffYears < 2) {
    //     return `Last Year ${hours}:${minutes}`;
    // } else {
    //     return `${year}/${month}/${day} ${hours}:${minutes}`;
    // }

    return `${year}/${month}/${day} ${hours}:${minutes}`;
}

function displayTimeAndTimeZone(currentTime, timeZoneName) {
    // Display the current time and timezone
    document.getElementById('currentTime').textContent = `Current Time: ${currentTime}`;
    document.getElementById('timeZoneName').textContent = `Time Zone: ${timeZoneName}`;
    // Update currentTime by 1 second every second
    setInterval(() => {
        const date = new Date(currentTime);
        date.setSeconds(date.getSeconds() + 1);
        currentTime = date.toISOString();
        document.getElementById('currentTime').textContent = `Current Time: ${currentTime}`;
    }, 1000);
}

// add the refresh button to fetch the data
document.getElementById('refreshData').addEventListener('click', () => {
    fetchDataAndRenderCharts();
});


// Function to create a chart with multiple datasets
function createChart(ctx, labels, datasets, yLabel) {
    if (ctx.chart) {
        ctx.chart.destroy(); // Destroy the existing chart if it exists
    }

    ctx.chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,  // Use your timeData directly as labels
            datasets: datasets
        },
        options: {
            scales: {
                x: {
                    type: 'category', 
                    title: {
                        display: true,
                        text: 'Time'
                    },
                    ticks: {
                        autoSkip: true,          
                        maxTicksLimit: 10,       
                        maxRotation: 20,         
                        minRotation: 0,
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: yLabel
                    }
                }
            }
        }
    });
}


// Function to create charts with the fetched data
function createCharts(cpuData, timeData, memoryData, batteryData, networkSentData, networkReceivedData, dashboardMemoryUsageData, cpuFrequencyData, currentTempData) {
    // CPU Usage Chart
    const ctxCpu = document.getElementById('cpuTimeChart').getContext('2d');
    createChart(ctxCpu, timeData, [{
        label: 'CPU Usage (%)',
        data: cpuData,
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: true,
        tension: 0.4
    }], 'CPU Usage (%)');

    // Memory Usage Chart
    const ctxMemory = document.getElementById('memoryTimeChart').getContext('2d');
    createChart(ctxMemory, timeData, [{
        label: 'Memory Usage (%)',
        data: memoryData,
        borderColor: 'rgba(153, 102, 255, 1)',
        backgroundColor: 'rgba(153, 102, 255, 0.2)',
        fill: true,
        tension: 0.4
    }], 'Memory Usage (%)');

    // Battery Percentage Chart
    const ctxBattery = document.getElementById('batteryTimeChart').getContext('2d');
    createChart(ctxBattery, timeData, [{
        label: 'Battery Percentage (%)',
        data: batteryData,
        borderColor: 'rgba(255, 159, 64, 1)',
        backgroundColor: 'rgba(255, 159, 64, 0.2)',
        fill: true,
        tension: 0.4
    }], 'Battery Percentage (%)');

    // Network Sent & Received Chart
    const ctxNetwork = document.getElementById('networkTimeChart').getContext('2d');
    createChart(ctxNetwork, timeData, [
        {
            label: 'Network Sent (MB)',
            data: networkSentData,
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            fill: true,
            tension: 0.4
        },
        {
            label: 'Network Received (MB)',
            data: networkReceivedData,
            borderColor: 'rgba(54, 162, 235, 1)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            fill: true,
            tension: 0.4
        }
    ], 'Data Transferred (MB)');

    // Dashboard Memory Usage Chart
    const ctxDashboardMemory = document.getElementById('dashboardMemoryTimeChart').getContext('2d');
    createChart(ctxDashboardMemory, timeData, [{
        label: 'Dashboard Memory Usage (%)',
        data: dashboardMemoryUsageData,
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        fill: true,
        tension: 0.4
    }], 'Dashboard Memory Usage (%)');

    // CPU Frequency Chart
    const ctxCpuFrequency = document.getElementById('cpuFrequencyTimeChart').getContext('2d');
    createChart(ctxCpuFrequency, timeData, [{
        label: 'CPU Frequency (GHz)',
        data: cpuFrequencyData,
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        fill: true,
        tension: 0.4
    }], 'CPU Frequency (GHz)');

    // Current Temperature Chart
    const ctxCurrentTemp = document.getElementById('currentTempTimeChart').getContext('2d');
    createChart(ctxCurrentTemp, timeData, [{
        label: 'Current Temperature (°C)',
        data: currentTempData,
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        fill: true,
        tension: 0.4
    }], 'Current Temperature (°C)');
}

// Fetch initial data when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchDataAndRenderCharts();
});
