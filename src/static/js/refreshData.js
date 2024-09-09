function refreshCardData(apiEndpoint, cardSelector, dataKey, unit = '') {
    if (!apiEndpoint || !cardSelector || !dataKey) {
        console.error('Missing required parameters: apiEndpoint, cardSelector, or dataKey.');
        return;
    }

    fetch(apiEndpoint)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log(`Fetched data from ${apiEndpoint}:`, data);

            // Find the card element
            const cardElement = document.querySelector(cardSelector);
            if (!cardElement) {
                console.error(`Element with selector ${cardSelector} not found.`);
                return;
            }

            // Update the card content with the fetched data
            const dataValue = data[dataKey];
            if (dataValue === undefined) {
                console.warn(`Data key ${dataKey} not found in the response.`);
                cardElement.querySelector('.card-text').textContent = 'Data not available';
                return;
            }

            cardElement.querySelector('.card-text').textContent = `${dataValue}${unit}`;
        })
        .catch(error => {
            console.error(`Error fetching data from ${apiEndpoint}:`, error);
        });
}
