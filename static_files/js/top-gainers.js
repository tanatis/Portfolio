async function loadGainers() {
    const response = await fetch(window.URLS.dailyMovers);
    const positions = await response.json();

    const gainersRoot = document.getElementById('top-gainers');
    const loader = document.getElementById('loader');
    loader.remove()
    const title = document.createElement('span');
    title.innerText = 'Top gainers';
    for (let i = 0; i < 10; i++) {
        const li = document.createElement('li');
        li.innerHTML = `
            <div class="daily-movers">${i+1}. <a href="/ticker/${positions['gainers'][i][0]}/">${positions['gainers'][i][0]}</a> (${positions['gainers'][i][1]})</div>
            <div class="${positions['gainers'][i][2] < 0 ? 'red' : 'green'}">${positions['gainers'][i][2].toFixed(2)} %</div>
        `
        gainersRoot.appendChild(li);
    }
}
loadGainers()