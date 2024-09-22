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
    fetch(`/api/v1/prometheus/graphs_data/targets?filter=${storedFilterValue}`)
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
            const timeData = data.time.map(time => formatDate(time, timeZoneName)); // Use timeZoneName from displayTimeAndTimeZone function

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
    const cpuDatasets = cpuData.map((cpu, index) => ({
        label: `CPU Usage (%) ${cpu.metric.instance}`,
        data: cpu.values,
        borderColor: `rgba(${75 + index * 20}, 192, 192, 1)`,
        backgroundColor: `rgba(${75 + index * 20}, 192, 192, 0.2)`,
        tension: 0.4
    }));

    createChart(ctxCpu, timeData, cpuDatasets, 'CPU Usage (%)');

    // Memory Usage Chart
    const ctxMemory = document.getElementById('memoryTimeChart').getContext('2d');
    const memoryDatasets = memoryData.map((memory, index) => ({
        label: `Memory Usage (%) ${memory.metric.instance}`,
        data: memory.values,
        borderColor: `rgba(${75 + index * 20}, 75, 192, 1)`,
        backgroundColor: `rgba(${75 + index * 20}, 75, 192, 0.2)`,
        tension: 0.4
    }));

    createChart(ctxMemory, timeData, memoryDatasets, 'Memory Usage (%)');    

    // Battery Percentage Chart
    const ctxBattery = document.getElementById('batteryTimeChart').getContext('2d');
    const batteryDatasets = batteryData.map((battery, index) => ({
        label: `Battery Usage (%) ${battery.metric.instance}`,
        data: battery.values,
        borderColor: `rgba(${192 + index * 20}, 75, 75, 1)`,
        backgroundColor: `rgba(${192 + index * 20}, 75, 75, 0.2)`,
        tension: 0.4
    }));

    createChart(ctxBattery, timeData, batteryDatasets, 'Battery Percentage (%)');

    // Network Sent & Received Chart
    const ctxNetwork = document.getElementById('networkTimeChart').getContext('2d');
    const networkDatasets = [
        ...networkSentData.map((networkSent, index) => ({
            label: `Network Sent (MB) ${networkSent.metric.instance}`,
            data: networkSent.values,
            borderColor: `rgba(${75 + index * 20}, 75, 192, 1)`,
            backgroundColor: `rgba(${75 + index * 20}, 75, 192, 0.2)`,
            tension: 0.4
        })),
        ...networkReceivedData.map((networkReceived, index) => ({
            label: `Network Received (MB) ${networkReceived.metric.instance}`,
            data: networkReceived.values,
            borderColor: `rgba(${192 + index * 20}, 75, 75, 1)`,
            backgroundColor: `rgba(${192 + index * 20}, 75, 75, 0.2)`,
            tension: 0.4
        }))
    ];

    createChart(ctxNetwork, timeData, networkDatasets, 'Data Transferred (MB)');

    // Dashboard Memory Usage Chart
    const ctxDashboardMemory = document.getElementById('dashboardMemoryTimeChart').getContext('2d');
    const dashboardMemoryDatasets = dashboardMemoryUsageData.map((dashboardMemory, index) => ({
        label: `Dashboard Memory Usage (%) ${dashboardMemory.metric.instance}`,
        data: dashboardMemory.values,
        borderColor: `rgba(${75 + index * 20}, 192, 75, 1)`,
        backgroundColor: `rgba(${75 + index * 20}, 192, 75, 0.2)`,
        tension: 0.4
    }));

    createChart(ctxDashboardMemory, timeData, dashboardMemoryDatasets, 'Dashboard Memory Usage (%)');

    // CPU Frequency Chart
    const ctxCpuFrequency = document.getElementById('cpuFrequencyTimeChart').getContext('2d');
    const cpuFrequencyDatasets = cpuFrequencyData.map((cpuFrequency, index) => ({
        label: `CPU Frequency (GHz) ${cpuFrequency.metric.instance}`,
        data: cpuFrequency.values,
        borderColor: `rgba(${192 + index * 20}, 192, 75, 1)`,
        backgroundColor: `rgba(${192 + index * 20}, 192, 75, 0.2)`,
        tension: 0.4,

    }));

    createChart(ctxCpuFrequency, timeData, cpuFrequencyDatasets, 'CPU Frequency (GHz)');

    // Current Temperature Chart
    const ctxCurrentTemp = document.getElementById('currentTempTimeChart').getContext('2d');
    const currentTempDatasets = currentTempData.map((currentTemp, index) => ({
        label: `Current Temperature (°C) ${currentTemp.metric.instance}`,
        data: currentTemp.values,
        borderColor: `rgba(${75 + index * 20}, 192, 192, 1)`,
        backgroundColor: `rgba(${75 + index * 20}, 192, 192, 0.2)`,
        tension: 0.4
    }));

    createChart(ctxCurrentTemp, timeData, currentTempDatasets, 'Current Temperature (°C)');
}

// Fetch initial data when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchDataAndRenderCharts();
});
