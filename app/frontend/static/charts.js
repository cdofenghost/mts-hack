const ctx = document.getElementById('graphChart').getContext('2d');

// Current Weather Stuff
const temp = document.getElementById('tempValue');
const humi= document.getElementById('humidityValue');
const windStats = document.getElementById('windStats');
const press = document.getElementById('pressureValue');

const gradient = ctx.createLinearGradient(0, 0, 0, 400);
gradient.addColorStop(0, 'rgba(255, 0, 51, 0.3)');
gradient.addColorStop(1, 'rgba(241, 126, 145, 0.125)');

let labels = [];
let humidities = [];
let temperatures = [];
let pressures = [];
let windSpeeds = [];
let windDirections = [];
// let COs = [];
// let SO2s = [];
// let H2Ss = [];
// let NO2s = [];
let datasets = null;

let chart = null;

let predictions = null;

document.addEventListener('DOMContentLoaded', async function() {
  try {
    const response = await fetch('http://127.0.0.1:8000/predict_with_full', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
        }),
    });
    predictions = await response.json();
    let len = await Object.keys(predictions.predictions).length;

    let perHour = Math.floor(len / 24);
    for (let i = 0; i < len; i++) {
        var hour = Math.floor(i / perHour);
        var minute = (i % (perHour)) * 2;
        var time = `+${hour}:${minute}0`;

        labels.push(`${time}`);

        // if (i % perHour === 0)
        //     labels.push(`${time}`);
        // else
        //     labels.push('');

        //console.log(predictions[i].humidity[0], predictions[i].pressure[0], predictions[i].temperature[0], predictions[i].wind_direction[0], predictions[i].wind_speed[0]);
        humidities.push(predictions.predictions[i].humidity);
        pressures.push(predictions.predictions[i].pressure);
        temperatures.push(predictions.predictions[i].temperature);
        windDirections.push(predictions.predictions[i].wind_direction);
        windSpeeds.push(predictions.predictions[i].wind_speed);
        // NO2s.push(predictions.predictions[i].no2);
        // COs.push(predictions.predictions[i].co);
        // H2Ss.push(predictions.predictions[i].h2s);
        // SO2s.push(predictions.predictions[i].so2);
    }

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
                            return tooltipItem.raw.toFixed(2);
                        }
                    },
                    bodyFont: {
                        family: "MTSTextRegular",
                    }
                },
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Временная шкала (в будущее)',
                        font: {
                        size: 14,
                        weight: 'bold'
                        },
                        color: '#666'
                    },
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
                    title: {
                        display: true,
                        text: 'RH, %',
                        font: {
                        size: 14,
                        weight: 'bold'
                        },
                        color: '#666'
                    },
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
            label: "RH, %",
            data: humidities,
        },
        Pressure: {
            label: "P, мм рт. ст.",
            data: pressures,
        },
        Temperature: {
            label: "T, C°",
            data: temperatures,
        },
        WindDirection: {
            label: "Направление ветра, °",
            data: windDirections,
        },
        WindSpeed: {
            label: "Скорость ветра, м/c",
            data: windSpeeds,
        },
        // CO: {
        //     label: "Давление",
        //     data: COs,
        // },
        // NO2: {
        //     label: "Давление",
        //     data: NO2s,
        // },
        // H2S: {
        //     label: "Температура",
        //     data: H2Ss,
        // },
        // SO2: {
        //     label: "Направление ветра",
        //     data: SO2s,
        // },
    };

    temp.textContent = `${Math.round(temperatures[0])}°`;
    humi.textContent = Math.round(humidities[0]) + "%";
    press.textContent = `${Math.round(pressures[0])} мм рт. ст.`;
    windStats.textContent = `${Math.round(windSpeeds[0])}м/c, (${Math.round(windDirections[0])})`;

  }
  catch { ; }
});

function updateChart(company) {
    const { label, data } = datasets[company];

    chart.data.datasets[0].label = label;
    chart.data.datasets[0].data = data;
    chart.options.scales.y.title.text = label;
    chart.update();

    document.querySelectorAll(".legend button").forEach(item => {
        item.innerHTML = `${item.textContent}`;
        item.id = "";
    });

    event.target.id = 'active';
    event.target.innerHTML = `<u>${event.target.textContent}</u>`;

}