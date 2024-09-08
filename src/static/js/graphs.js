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

// Function to create a chart with multiple datasets
function createChart(ctx, datasets, yLabel) {
    if (ctx.chart) {
        ctx.chart.destroy(); // Destroy the existing chart if it exists
    }

    ctx.chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: datasets[0].data.map((_, i) => i), // Assuming all datasets have the same length
            datasets: datasets
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
    createChart(ctxCpu, [{
        label: 'CPU Usage (%)',
        data: cpuData,
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: true,
        tension: 0.4
    }], 'CPU Usage (%)');

    // Memory Usage Chart
    const ctxMemory = document.getElementById('memoryTimeChart').getContext('2d');
    createChart(ctxMemory, [{
        label: 'Memory Usage (%)',
        data: memoryData,
        borderColor: 'rgba(153, 102, 255, 1)',
        backgroundColor: 'rgba(153, 102, 255, 0.2)',
        fill: true,
        tension: 0.4
    }], 'Memory Usage (%)');

    // Battery Percentage Chart
    const ctxBattery = document.getElementById('batteryTimeChart').getContext('2d');
    createChart(ctxBattery, [{
        label: 'Battery Percentage (%)',
        data: batteryData,
        borderColor: 'rgba(255, 159, 64, 1)',
        backgroundColor: 'rgba(255, 159, 64, 0.2)',
        fill: true,
        tension: 0.4
    }], 'Battery Percentage (%)');

    // Network Sent & Received Chart
    const ctxNetwork = document.getElementById('networkTimeChart').getContext('2d');
    createChart(ctxNetwork, [
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
    createChart(ctxDashboardMemory, [{
        label: 'Dashboard Memory Usage (%)',
        data: dashboardMemoryUsageData,
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        fill: true,
        tension: 0.4
    }], 'Dashboard Memory Usage (%)');

    // CPU Frequency Chart
    const ctxCpuFrequency = document.getElementById('cpuFrequencyTimeChart').getContext('2d');
    createChart(ctxCpuFrequency, [{
        label: 'CPU Frequency (GHz)',
        data: cpuFrequencyData,
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        fill: true,
        tension: 0.4
    }], 'CPU Frequency (GHz)');

    // Current Temperature Chart
    const ctxCurrentTemp = document.getElementById('currentTempTimeChart').getContext('2d');
    createChart(ctxCurrentTemp, [{
        label: 'Current Temperature (°C)',
        data: currentTempData,
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        fill: true,
        tension: 0.4
    }], 'Current Temperature (°C)');
}

// Refresh button interaction
document.getElementById('refresh').addEventListener('click', () => {
    location.reload();
});
