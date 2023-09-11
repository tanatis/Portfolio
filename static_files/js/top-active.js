async function loadTopActive() {
    const response = await fetch(window.URLS.dailyMovers);
    const positions = await response.json();

    const activeRoot = document.getElementById('top-active');
    const loader = document.getElementById('loader');
    loader.remove()
    const title = document.createElement('span');
    title.innerText = 'Most active';
    for (let i = 0; i < 10; i++) {
        const li = document.createElement('li');
        li.innerHTML = `
            <div class="daily-movers">${i+1}. <a href="/ticker/${positions['active'][i][0]}/">${positions['active'][i][0]}</a> (${positions['active'][i][1]})</div>
            <div class="${positions['active'][i][2] < 0 ? 'red' : 'green'}">${positions['active'][i][2].toFixed(2)} %</div>
        `
        activeRoot.appendChild(li);
    }
}
loadTopActive()
