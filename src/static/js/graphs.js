// Variables to store chart instances
let cpuTimeChart, memoryTimeChart, batteryTimeChart, networkTimeChart, dashboardMemoryTimeChart, cpuFrequencyTimeChart, currentTempTimeChart;

// Function to fetch and display data
function fetchDataAndRenderCharts() {
    // Get the selected filter value
    const filterValue = document.getElementById('timeFilter').value;
    
    // Fetch data with the selected time filter
    fetch(`/api/graphs_data?filter=${filterValue}`)
        .then(response => response.json())
        .then(data => {
            const cpuData = data.cpu;
            const timeData = data.time.map(t => new Date(t)); // Ensure date objects
            const memoryData = data.memory;
            const batteryData = data.battery;
            const networkSentData = data.network_sent;
            const networkReceivedData = data.network_received;
            const dashboardMemoryUsageData = data.dashboard_memory_usage;
            const cpuFrequencyData = data.cpu_frequency;
            const currentTempData = data.current_temp;

            createCharts(cpuData, timeData, memoryData, batteryData, networkSentData, networkReceivedData, dashboardMemoryUsageData, cpuFrequencyData, currentTempData);
        })
        .catch(error => console.error('Error fetching data:', error));
}

// Function to create a chart with multiple datasets
function createChart(ctx, labels, datasets, yLabel) {
    if (ctx.chart) {
        ctx.chart.destroy(); // Destroy the existing chart if it exists
    }

    ctx.chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,  // Use timeData for x-axis labels
            datasets: datasets
        },
        options: {
            scales: {
                x: {
                    type: 'time', // Use 'time' scale for proper date formatting
                    time: {
                        unit: 'minute', // Adjust based on the granularity of your data
                        tooltipFormat: 'll HH:mm', // Tooltip format for time
                        displayFormats: {
                            minute: 'HH:mm', // Display format for minute-level granularity
                            hour: 'MMM D, HH:mm', // Display format for hour-level granularity
                            day: 'MMM D', // Display format for day-level granularity
                            week: 'MMM D', // Display format for week-level granularity
                            month: 'MMM YYYY', // Display format for month-level granularity
                            quarter: '[Q]Q YYYY', // Display format for quarter-level granularity
                            year: 'YYYY' // Display format for year-level granularity
                        }
                    },
                    title: {
                        display: true,
                        text: 'Time'
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

// Trigger data update when the select dropdown value changes
document.getElementById('timeFilter').addEventListener('change', () => {
    fetchDataAndRenderCharts();
});
