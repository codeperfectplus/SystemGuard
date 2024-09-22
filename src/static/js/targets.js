// Function to fetch and populate target data
async function fetchTargetData() {
    try {
        const response = await fetch('/api/v1/targets'); // Replace with the actual URL if different
        const data = await response.json();

        const targetTableBody = document.getElementById('target-table-body');

        // Check if there are active targets
        if (data.active_targets && data.active_targets.length > 0) {
            data.active_targets.forEach(target => {
                const row = document.createElement('tr');

                const jobCell = document.createElement('td');
                jobCell.textContent = target.labels.job;
                row.appendChild(jobCell);

                const instanceCell = document.createElement('td');
                instanceCell.textContent = target.labels.instance;
                row.appendChild(instanceCell);

                const healthCell = document.createElement('td');
                healthCell.textContent = target.health;
                healthCell.className = target.health === 'up' ? 'health-up' : 'health-down';
                row.appendChild(healthCell);

                const lastScrapeCell = document.createElement('td');
                lastScrapeCell.textContent = new Date(target.lastScrape).toLocaleString();
                row.appendChild(lastScrapeCell);

                const lastErrorCell = document.createElement('td');
                lastErrorCell.textContent = target.lastError ? target.lastError : 'No Errors';
                row.appendChild(lastErrorCell);

                const scrapeUrlCell = document.createElement('td');
                scrapeUrlCell.textContent = target.scrapeUrl;
                row.appendChild(scrapeUrlCell);

                const scrapeDurationCell = document.createElement('td');
                scrapeDurationCell.textContent = target.lastScrapeDuration.toFixed(3);
                row.appendChild(scrapeDurationCell);

                // __scrape_interval__
                const scrapeIntervalCell = document.createElement('td');
                scrapeIntervalCell.textContent = target.discoveredLabels.__scrape_interval__;
                row.appendChild(scrapeIntervalCell);

                if (target.health === 'up') {
                    const dashboardCell = document.createElement('td');
                    const dashboardLink = document.createElement('a');
                    dashboardLink.href = target.scrapeUrl.replace(/\/metrics$/, '');
                    dashboardLink.textContent = 'View Dashboard';
                    dashboardLink.target = '_blank'; // Open link in a new tab
                    dashboardLink.rel = 'noopener noreferrer'; // Security measure for external links
                    dashboardCell.appendChild(dashboardLink);
                    row.appendChild(dashboardCell);
                } else {
                    const emptyCell = document.createElement('td');
                    row.appendChild(emptyCell);
                }

                // remove the instance from the prometheus

                const removeCell = document.createElement('td');
                const removeForm = document.createElement('form');
                removeForm.action = '/targets/remove_target'; // Replace with actual endpoint if needed
                removeForm.method = 'POST';
                removeForm.style.display = 'inline';

                const jobNameInput = document.createElement('input');
                jobNameInput.type = 'hidden';
                jobNameInput.name = 'job_name';
                jobNameInput.value = target.labels.job;
                removeForm.appendChild(jobNameInput);

                const targetToRemoveInput = document.createElement('input');
                targetToRemoveInput.type = 'hidden';
                targetToRemoveInput.name = 'target_to_remove';
                targetToRemoveInput.value = target.labels.instance;
                removeForm.appendChild(targetToRemoveInput);

                const submitButton = document.createElement('input');
                submitButton.type = 'submit';
                submitButton.value = 'Remove';
                submitButton.onclick = function () {
                    return confirm('Are you sure you want to remove this target?');
                };
                removeForm.appendChild(submitButton);

                removeCell.appendChild(removeForm);
                row.appendChild(removeCell);

                // Append the row to the table body
                targetTableBody.appendChild(row);

                // Append the row to the table body
                targetTableBody.appendChild(row);
            });
        } else {
            targetTableBody.innerHTML = '<tr><td colspan="7" class="error-message">No active targets found</td></tr>';
        }
    } catch (error) {
        console.error('Error fetching target data:', error);
        const targetTableBody = document.getElementById('target-table-body');
        targetTableBody.innerHTML = '<tr><td colspan="7" class="error-message">Failed to fetch targets</td></tr>';
    }
}

// Fetch the data when the page loads
document.addEventListener('DOMContentLoaded', fetchTargetData);