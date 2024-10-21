let lastUpdateDay = null; // Poslední aktualizovaný den

function updateClock() {
    const now = new Date();

    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');

    document.getElementById('clock').textContent = `${hours}:${minutes}:${seconds}`;

    const day = String(now.getDate()).padStart(2, '0');
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const year = now.getFullYear();

    if (lastUpdateDay !== day) {
        lastUpdateDay = day;
        document.getElementById('date').textContent = `${day}.${month}.${year}`;
    }
}

setInterval(updateClock, 1000);
updateClock(); // Zavolá funkci hned na začátku
