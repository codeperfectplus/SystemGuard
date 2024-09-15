document.addEventListener('DOMContentLoaded', function () {
    const bars = [
        { selector: '.battery-bar', dataAttr: 'data-battery', limits: [25, 75] },
        { selector: '.disk-bar', dataAttr: 'data-disk-usage', limits: [50, 80] },
        { selector: '.cpu-usage-bar', dataAttr: 'data-cpu-usage', limits: [50, 80] },
        { selector: '.memory-usage-bar', dataAttr: 'data-memory-usage', limits: [.5, .8] , max_attr: 'data-memory-total' },
        { selector: '.frequency-bar', dataAttr: 'data-cpu-frequency', limits: [.5, .8], max_attr: 'data-cpu-max-frequency' },
        { selector: '.temp-bar', dataAttr: 'data-cpu-temp', limits: [.7, .9], max_attr: 'data-cpu-max-temp' },
        // todo: find max frequency and max temperature for the CPU
    ];

    bars.forEach(({ selector, dataAttr, limits, max_attr}) => {
        const bar = document.querySelector(selector);
        const card = document.querySelector(`[${dataAttr}]`);
        const max_value = document.querySelector(`[${max_attr}]`);
        console.log(max_value);
    

        if (!bar || !card) {
            // console.warn(`Element not found for selector: ${selector} or data attribute: ${dataAttr}`);
            return;
        }

        // if max_attr is defined, use that to define the limits
        if (max_value) {
            const max = parseInt(card.getAttribute(max_attr), 10);

            if (isNaN(max)) {
                // console.warn(`Invalid max value for ${max_value}`);
                return;
            }

            limits = [max * limits[0], max * limits[1]];
            console.log(`Limits for ${dataAttr}: ${limits}`);
        }

        const percentage = parseInt(card.getAttribute(dataAttr), 10);

        if (isNaN(percentage)) {
            // console.warn(`Invalid percentage value for ${dataAttr}`);
            return;
        }

        if (percentage <= limits[0]) {
            bar.classList.add('low');
        } else if (percentage > limits[0] && percentage <= limits[1]) {
            bar.classList.add('medium');
        } else {
            bar.classList.add('high');
        }
    });
});
