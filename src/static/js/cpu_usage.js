document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('cpuUsageChart').getContext('2d');
    const cpuUsageChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Array.from({length: {{ cpu_usage|length }}}, (_, i) => `Core ${i}`),
            datasets: [{
                label: 'CPU Usage (%)',
                data: {{ cpu_usage|tojson }},
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});