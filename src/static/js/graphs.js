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

            // current time from backend to display
            const currentTime = data.current_time;
            const timeZoneName = Intl.DateTimeFormat().resolvedOptions().timeZone;
            displayTimeAndTimeZone(currentTime, timeZoneName);

            // Format the time data using the currentTime from backend
            const timeData = data.time.map(time => formatDate(time, timeZoneName)); // Use timeZoneName from displayTimeAndTimeZone function

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

function formatDate(utcTime, timeZone) {
    const date = new Date(utcTime);
    
    // Format options can be adjusted for your needs
    const options = {
        timeZone: timeZone,
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false // Change to true if you prefer 12-hour format
    };

    // Generate formatted string
    const formattedDate = date.toLocaleString('en-US', options);

    // For better graph display, you might want just the date and hour
    return formattedDate.replace(/, (\d{2}:\d{2})/, ' $1'); // Example: "09/22/2024 14:30"
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

    const allDataPoints = datasets.flatMap(dataset => dataset.data);
    const minY = Math.min(...allDataPoints.filter(value => typeof value === 'number'));
    const maxY = Math.max(...allDataPoints.filter(value => typeof value === 'number'));

    ctx.chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets.map(dataset => ({
                ...dataset,
                borderWidth: 2,
                fill: false,
                tension: 0.3,
                pointRadius: 5,
                pointHoverRadius: 7,
                backgroundColor: dataset.backgroundColor || 'rgba(75, 192, 192, 0.2)',
                borderColor: dataset.borderColor || 'rgba(75, 192, 192, 1)',
            })),
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
                        maxTicksLimit: 6,       
                        maxRotation: 0,         
                        minRotation: 0,
                    }
                },
                y: {
                    beginAtZero: minY < 0 ? false : true, // Adjust y-axis based on data
                    title: {
                        display: true,
                        text: yLabel,
                    },
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
