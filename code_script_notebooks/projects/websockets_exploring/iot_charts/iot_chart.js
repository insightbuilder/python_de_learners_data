// Create a WebSocket connection to the server
const socket = new WebSocket("ws://localhost:8765");

// Initialize empty arrays to store temperature and humidity data
let temperatures = [];
let humidities = [];

// Create a Chart.js chart
const ctx = document.getElementById('temperatureHumidityGraph').getContext('2d');

const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Temperature (°C)',
            borderColor: 'red',
            data: temperatures,
            fill: false
        }, {
            label: 'Humidity (%)',
            borderColor: 'blue',
            data: humidities,
            fill: false
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Time'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Value'
                }
            }]
        }
    }
});

// Event listener for when the WebSocket connection is established
socket.addEventListener('open', function (event) {
    console.log('WebSocket connection established.');
});

// Event listener for incoming WebSocket messages
socket.addEventListener('message', function (event) {
    // Parse the JSON message received from the server
    const data = JSON.parse(event.data);

    // Update the arrays with new temperature and humidity data
    temperatures.push(data.temperature);
    humidities.push(data.humidity);

    // Limit the number of data points to display on the graph
    const maxDataPoints = 10;
    if (temperatures.length > maxDataPoints) {
        temperatures.shift();
        humidities.shift();
    }

    // Update the chart with the new data
    chart.data.labels = Array.from(Array(temperatures.length).keys()).map(x => String(x));
    chart.data.datasets[0].data = temperatures;
    chart.data.datasets[1].data = humidities;
    chart.update();
});