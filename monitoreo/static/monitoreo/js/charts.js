// ---------- INICIALIZAR GRÁFICA ----------
const ctx = document.getElementById('chart');
const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Temperatura (°C)',
            data: [],
            borderWidth: 3,
            borderColor: 'blue'
        }]
    },
    options: {
        responsive: true,
        animation: false,
        scales: {
            y: { beginAtZero: false }
        }
    }
});

// ---------- FUNCIÓN PARA OBTENER DATOS ----------
function refreshData() {
    fetch('/monitoreo/data/')
        .then(r => r.json())
        .then(d => {

            // TEMPERATURA
            if (d.temperatura !== null) {
                document.getElementById('temp').innerText = d.temperatura + "°C";

                // agregar punto a gráfica
                chart.data.labels.push("");
                chart.data.datasets[0].data.push(d.temperatura);

                // limitar a 20 puntos
                if (chart.data.labels.length > 20) {
                    chart.data.labels.shift();
                    chart.data.datasets[0].data.shift();
                }

                chart.update();
            } else {
                document.getElementById('temp').innerText = "--";
            }

            // HUMEDAD
            if (d.humedad !== null) {
                document.getElementById('hum').innerText = d.humedad + "%";
            } else {
                document.getElementById('hum').innerText = "--";
            }

            // CALIDAD DEL AIRE
            if (d.calidad !== null) {
                document.getElementById('air').innerText = d.calidad + " ppm";
            } else {
                document.getElementById('air').innerText = "--";
            }
        })
        .catch(err => console.error("Error al obtener datos:", err));
}

// Ejecutar cada 3 segundos
setInterval(refreshData, 3000);
refreshData();
