async function reloadPositions() {
    const response = await fetch(window.URLS.portfolio);
    const positions = await response.json();

    const portfolioRoot = document.getElementById('portfolio-container');
    for (const position of positions['positions']) {
        let addUrl = `/position/${position.id}/add/`
        let sellUrl = `/position/${position.id}/sell/`
        const portfolioRow = document.createElement('div');
        portfolioRow.classList.add('portfolio-row');

        portfolioRow.innerHTML = `
                <div class="portfolio-cell">${position.ticker_symbol}</div>
                <div class="portfolio-cell">${position.count}</div>
                <div class="portfolio-cell">${position.avg_price.toFixed(2)}</div>
                <div class="portfolio-cell">${position.price.toFixed(2)}</div>
                <div class="portfolio-cell">${position.current_price.toFixed(2)}</div>
                <div class="portfolio-cell">${position.change.toFixed(2)}%</div>
                <div class="portfolio-cell"><a href="${addUrl}">Add</a> / <a href="${sellUrl}">Sell</a></div>
                `
        portfolioRoot.appendChild(portfolioRow);
        if (position['position_history'].length > 1) {
            portfolioRow.classList.add('accordion-toggle');
            accordionContent = document.createElement('div');
            accordionContent.classList.add('accordion-content');
            for (historyLine of position['position_history']) {
                historyRow = document.createElement('div');
                historyRow.classList.add('portfolio-row');
                historyRow.innerHTML = `
                        <div class="portfolio-cell">Something 1</div>
                        <div class="portfolio-cell">Something 2</div>
                        <div class="portfolio-cell">Something 3</div>
                        <div class="portfolio-cell">Something 4</div>
                        `
                accordionContent.appendChild(historyRow)
            }
            portfolioRoot.appendChild(accordionContent);
        }
    }

    //portfolioRoot.innerHTML = '';
    const loader = document.getElementById('loader');
    loader.remove();
    const bottomRow = document.createElement('div')
    bottomRow.classList.add('portfolio-row')
    bottomRow.innerHTML = `
            <div class="portfolio-cell">Cash:</div>
            <div class="portfolio-cell"></div>
            <div class="portfolio-cell"></div>
            <div class="portfolio-cell">${positions.cash.toFixed(2)}</div>
            `
    portfolioRoot.appendChild(bottomRow)
}

reloadPositions()
