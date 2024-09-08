function refreshCardData(apiEndpoint, cardSelector, dataKey, unit = '') {
    fetch(`${apiEndpoint}`)
        .then(response => response.json())
        .then(data => {
            console.log(`Fetched ${apiEndpoint} data:`, data);
            // Update the card content with the fetched data
            document.querySelector(cardSelector + ' .card-text').textContent = `${data[dataKey]}${unit}`;
        })
        .catch(error => {
            console.error(`Error fetching ${apiEndpoint}:`, error);
        });
}
