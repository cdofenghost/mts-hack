const ctx = document.getElementById('graphChart').getContext('2d');

const gradient = ctx.createLinearGradient(0, 0, 0, 400);
gradient.addColorStop(0, 'rgba(255, 0, 51, 0.3)');
gradient.addColorStop(1, 'rgba(241, 126, 145, 0.125)');

let labels = [];
let humidities = [];
let temperatures = [];
let pressures = [];
let windSpeeds = [];
let windDirections = [];
let datasets = null;

let chart = null;

let predictions = null;

document.addEventListener('DOMContentLoaded', async function() {
  try {
    const response = await fetch('http://127.0.0.1:8000/predict', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            station: "string",
            time: "string",
        }),
    });
    predictions = await response.json();
    let len = await Object.keys(predictions.predictions).length;
    console.log(predictions.predictions);

    let perHour = (Number)(len / 24);
    for (let i = 0; i < len; i++) {
        var hour = Math.floor(i / perHour);
        var minute = (i % (perHour)) * 2;
        var time = `+${hour}:${minute}0`;

        console.log(i, i % perHour, Math.floor(i / perHour));
        labels.push(`${time}`);

        // if (i % perHour === 0)
        //     labels.push(`${time}`);
        // else
        //     labels.push('');

        humidities.push(predictions.predictions[i].humidity[0]);
        pressures.push(predictions.predictions[i].pressure[0]);
        temperatures.push(predictions.predictions[i].temperature[0]);
        windDirections.push(predictions.predictions[i].wind_direction[0]);
        windSpeeds.push(predictions.predictions[i].wind_speed[0]);

    }
    console.log(labels);
    console.log(humidities);
    console.log(pressures);
    console.log(temperatures);
    console.log(windSpeeds);
    console.log(windDirections);


    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: 'One',
                data: humidities,
                fill: true,
                backgroundColor: gradient,
                borderColor: "#FF0032",
                tension: 0.4,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false,
                    labels: {
                        font: {
                            family: "MTSTextRegular",
                        }
                    }
                },
                tooltip: {
                    enabled: true,
                    callbacks: {
                        label: function (tooltipItem) {
                            return tooltipItem.raw.toFixed(6);
                        }
                    },
                    bodyFont: {
                        family: "MTSTextRegular",
                    }
                },
            },
            scales: {
                x: {
                    grid: {
                        drawOnChartArea: false,
                        drawBorder: true,
                    },
                    ticks: {
                        font: {
                            family: "MTSTextRegular",
                            size: 18,
                        },
                        color: "#000",
                    }
                },
                y: {
                    grid: {
                        drawOnChartArea: false,
                        drawBorder: true,
                    },
                    ticks: {
                        font: {
                            family: "MTSTextRegular",
                            size: 18,
                        },
                    }
                }
            }
        }
    });

    datasets = {
        Humidity: {
            label: "Влажность",
            data: humidities,
        },
        Pressure: {
            label: "Давление",
            data: pressures,
        },
        Temperature: {
            label: "Температура",
            data: temperatures,
        },
        WindDirection: {
            label: "Направление ветра",
            data: windDirections,
        },
        
    };
  }
  catch { ; }
});

function updateChart(company) {
    const { label, data } = datasets[company];

    chart.data.datasets[0].label = label;
    chart.data.datasets[0].data = data;
    chart.update();

    document.querySelectorAll(".legend button").forEach(item => {
        item.innerHTML = `${item.textContent}`;
        item.id = "";
    });

    event.target.id = 'active';
    event.target.innerHTML = `<u>${event.target.textContent}</u>`;

}