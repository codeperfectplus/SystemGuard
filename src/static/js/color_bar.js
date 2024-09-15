// document.addEventListener('DOMContentLoaded', function () {
//     updateColorBars();
// });

// function updateColorBars() {
//     const bars = [
//         { selector: '.battery-bar', dataAttr: 'data-battery', limits: [25, 75] },
//         { selector: '.disk-bar', dataAttr: 'data-disk-usage', limits: [60, 80] },
//         { selector: '.cpu-usage-bar', dataAttr: 'data-cpu-usage', limits: [50, 80] },
//         { selector: '.memory-usage-bar', dataAttr: 'data-memory-usage', limits: [0.5, 0.8], maxAttr: 'data-memory-total' },
//         { selector: '.frequency-bar', dataAttr: 'data-cpu-frequency', limits: [0.5, 0.8], maxAttr: 'data-cpu-max-frequency' },
//         { selector: '.temp-bar', dataAttr: 'data-cpu-temp', limits: [0.65, 0.9], maxAttr: 'data-cpu-max-temp' }
//     ];

//     bars.forEach(({ selector, dataAttr, limits, maxAttr }) => {
//         const bar = document.querySelector(selector);
//         const card = document.querySelector(`[${dataAttr}]`);
//         const maxElement = maxAttr ? document.querySelector(`[${maxAttr}]`) : null;

//         if (!bar || !card) {
//             // console.warn(`Element not found for selector: ${selector} or data attribute: ${dataAttr}`);
//             return;
//         }

//         let percentage = parseFloat(card.getAttribute(dataAttr));

//         if (isNaN(percentage)) {
//             console.warn(`Invalid percentage value for ${dataAttr}`);
//             return;
//         }

//         // If maxAttr is defined, use it to scale the limits
//         if (maxElement) {
//             const maxValue = parseFloat(maxElement.getAttribute(maxAttr));
//             if (isNaN(maxValue)) {
//                 // console.warn(`Invalid max value for ${maxAttr}`);
//                 return;
//             }

//             limits = [maxValue * limits[0], maxValue * limits[1]];
//         }

//         // Apply class based on percentage within the defined limits
//         if (percentage <= limits[0]) {
//             bar.classList.add('low');
//         } else if (percentage > limits[0] && percentage <= limits[1]) {
//             bar.classList.add('medium');
//         } else {
//             bar.classList.add('high');
//         }
//     });
// }
