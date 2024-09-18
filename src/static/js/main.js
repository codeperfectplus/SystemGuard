document.addEventListener("DOMContentLoaded", function () {
    // Select all card elements on the page
    const cards = document.querySelectorAll('.card');

    cards.forEach((card) => {
        // Create a new element for the text
        const providerText = document.createElement('p');
        providerText.classList.add('data-provider-text');
        providerText.innerHTML = 'Powered by <strong>SystemGuard</strong>';

        // Append the text element to the card
        card.appendChild(providerText);
    });
});
