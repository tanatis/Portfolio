async function loadLosers() {
    const response = await fetch(window.URLS.dailyMovers);
    const positions = await response.json();

    const losersRoot = document.getElementById('top-losers');
    const loader = document.getElementById('loader');
    loader.remove()
    const title = document.createElement('span');
    title.innerText = 'Top losers';
    for (let i = 0; i < 10; i++) {
        //console.log(positions['active'][i][0])
        const li = document.createElement('li');
        li.innerHTML = `
            <div class="daily-movers">${i+1}. <a href="/ticker/${positions['losers'][i][0]}/">${positions['losers'][i][0]}</a> (${positions['losers'][i][1]})</div>
            <div class="${positions['losers'][i][2] < 0 ? 'red' : 'green'}">${positions['losers'][i][2].toFixed(2)} %</div>
        `
        losersRoot.appendChild(li);
    }
}
loadLosers()