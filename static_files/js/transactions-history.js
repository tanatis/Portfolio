async function reloadHistory(url = window.URLS.history) {
    const response = await fetch(url);
    const {results, count, previous, next} = await response.json();

    const historyRoot = document.getElementById('api-history');
    historyRoot.innerHTML = '';


    for (const history of results) {
        const historyRow = document.createElement('div');
        historyRow.classList.add('history-row');
        historyRow.innerHTML = `
                <div class="history-cell">${history.date_added}</div>
                <div class="history-cell">${history.ticker ? history.ticker : 'CASH'}</div>
                <div class="history-cell">${history.operation_type}</div>
                <div class="history-cell">${history.count ? history.count : '--'}</div>
                <div class="history-cell">${history.price.toFixed(2)}</div>
                `
        historyRoot.appendChild(historyRow);
    }

    const paginationLinks = document.getElementById('pagination-links');
    paginationLinks.innerHTML = '';

    if (previous) {
        const prevLink = document.createElement('a');
        prevLink.classList.add('pagination-link')
        prevLink.href = 'javascript:void(0)';
        prevLink.innerText = 'Previous';
        prevLink.addEventListener('click', () => reloadHistory(previous));
        paginationLinks.appendChild(prevLink);
    }

    for (let i = 1; i <= Math.ceil(count / 15); i++) {
        const pageLink = document.createElement('a');
        pageLink.classList.add('pagination-link')
        pageLink.href = 'javascript:void(0)';
        pageLink.innerText = i.toString();
        if (url.includes(`page=${i}`)) {
            // pageLink.style.fontWeight = 'bold';
            pageLink.classList.add('pagination-active')
        }
        pageLink.addEventListener('click', () => {
            const newUrl = url.includes('?') ? url.replace(/page=\d+/i, `page=${i}`) : `${url}?page=${i}`;
            reloadHistory(newUrl);
        });
        paginationLinks.appendChild(pageLink);
    }

    if (next) {
        const nextLink = document.createElement('a');
        nextLink.classList.add('pagination-link')
        nextLink.href = 'javascript:void(0)';
        nextLink.innerText = 'Next';
        nextLink.addEventListener('click', () => reloadHistory(next));
        paginationLinks.appendChild(nextLink);
    }
}

reloadHistory()