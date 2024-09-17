// Powered by card 
document.addEventListener("DOMContentLoaded", function () {
    // Select all card elements on the page
    const cards = document.querySelectorAll('.card');

    cards.forEach((card) => {
        // Create a new element for the text
        const providerText = document.createElement('p');
        providerText.classList.add('data-provider-text');
        providerText.innerHTML = 'Powered by SystemGuard';

        // Append the text element to each card
        card.appendChild(providerText);
    });
});
