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

            console.log('cpuFrequencyData:', cpuFrequencyData);

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
                    reverse: true, // Reverse the x-axis to start from the right
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
