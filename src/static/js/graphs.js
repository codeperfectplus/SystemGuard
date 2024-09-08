// Variables to store chart instances
let cpuTimeChart, memoryTimeChart, batteryTimeChart, networkTimeChart, dashboardMemoryTimeChart, cpuFrequencyTimeChart, currentTempTimeChart;

fetch('/api/graphs_data')
    .then(response => response.json())
    .then(data => {
        const cpuData = data.cpu;
        const timeData = data.time;
        const memoryData = data.memory;
        const batteryData = data.battery;
        const networkSentData = data.network_sent;
        const networkReceivedData = data.network_received;
        const dashboardMemoryUsageData = data.dashboard_memory_usage;
        const cpuFrequencyData = data.cpu_frequency;
        const currentTempData = data.current_temp;

        // Create charts after data is fetched
        createCharts(cpuData, timeData, memoryData, batteryData, networkSentData, networkReceivedData, dashboardMemoryUsageData, cpuFrequencyData, currentTempData);
    })
    .catch(error => console.error('Error fetching data:', error));

// Function to create a chart
function createChart(ctx, label, data, borderColor, backgroundColor, yLabel, timeData) {
    if (ctx.chart) {
        ctx.chart.destroy(); // Destroy the existing chart if it exists
    }

    ctx.chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timeData,  // Ensure the timeData is passed in here
            datasets: [{
                label: label,
                data: data,
                borderColor: borderColor,
                backgroundColor: backgroundColor,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Time' } },
                y: { beginAtZero: true, title: { display: true, text: yLabel } }
            }
        }
    });
}

// Function to create charts with the fetched data
function createCharts(cpuData, timeData, memoryData, batteryData, networkSentData, networkReceivedData, dashboardMemoryUsageData, cpuFrequencyData, currentTempData) {
    // CPU Usage Chart
    const ctxCpu = document.getElementById('cpuTimeChart').getContext('2d');
    createChart(ctxCpu, 'CPU Usage (%)', cpuData, 'rgba(75, 192, 192, 1)', 'rgba(75, 192, 192, 0.2)', 'CPU Usage (%)', timeData);

    // Memory Usage Chart
    const ctxMemory = document.getElementById('memoryTimeChart').getContext('2d');
    createChart(ctxMemory, 'Memory Usage (%)', memoryData, 'rgba(153, 102, 255, 1)', 'rgba(153, 102, 255, 0.2)', 'Memory Usage (%)', timeData);

    // Battery Percentage Chart
    const ctxBattery = document.getElementById('batteryTimeChart').getContext('2d');
    createChart(ctxBattery, 'Battery Percentage (%)', batteryData, 'rgba(255, 159, 64, 1)', 'rgba(255, 159, 64, 0.2)', 'Battery Percentage (%)', timeData);

    // Network Sent & Received Chart
    const ctxNetwork = document.getElementById('networkTimeChart').getContext('2d');
    createChart(ctxNetwork, 'Network Sent (MB)', networkSentData, 'rgba(255, 99, 132, 1)', 'rgba(255, 99, 132, 0.2)', 'Data Transferred (MB)', timeData);
    createChart(ctxNetwork, 'Network Received (MB)', networkReceivedData, 'rgba(54, 162, 235, 1)', 'rgba(54, 162, 235, 0.2)', 'Data Transferred (MB)', timeData);

    // Dashboard Memory Usage Chart
    const ctxDashboardMemory = document.getElementById('dashboardMemoryTimeChart').getContext('2d');
    createChart(ctxDashboardMemory, 'Dashboard Memory Usage (%)', dashboardMemoryUsageData, 'rgba(255, 99, 132, 1)', 'rgba(255, 99, 132, 0.2)', 'Dashboard Memory Usage (%)', timeData);

    // CPU Frequency Chart
    const ctxCpuFrequency = document.getElementById('cpuFrequencyTimeChart').getContext('2d');
    createChart(ctxCpuFrequency, 'CPU Frequency (GHz)', cpuFrequencyData, 'rgba(255, 99, 132, 1)', 'rgba(255, 99, 132, 0.2)', 'CPU Frequency (GHz)', timeData);

    // Current Temperature Chart
    const ctxCurrentTemp = document.getElementById('currentTempTimeChart').getContext('2d');
    createChart(ctxCurrentTemp, 'Current Temperature (°C)', currentTempData, 'rgba(255, 99, 132, 1)', 'rgba(255, 99, 132, 0.2)', 'Current Temperature (°C)', timeData);
}

// Refresh button interaction
document.getElementById('refresh').addEventListener('click', () => {
    location.reload();
});
