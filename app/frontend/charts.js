const ctx = document.getElementById('graphChart').getContext('2d');

const gradient = ctx.createLinearGradient(0, 0, 0, 400);
gradient.addColorStop(0, 'rgba(255, 0, 50, 0.5)');
gradient.addColorStop(1, 'rgba(241, 126, 145, 0.125)');

let chart = new Chart(ctx, {
    type: "line",
    data: {
        labels: ['+0', '+1', '+2', '+3', '+4', '+5', '+6'],
        datasets: [{
            label: 'One',
            data: [1000.00, 1020.00, 980.00, 1050.00, 1000.00, 1070.00, 1040.00],
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
                callbacks: {
                    label: function (tooltipItem) {
                        return "$" + tooltipItem.yLabel.toFixed(2);
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
                    },
                    color: "#FF0032",
                }
            },
            y: {
                display: false,
                grid: {
                    drawOnChartArea: false,
                    drawBorder: true,
                },
                ticks: {
                    font: {
                        family: "MTSTextRegular",
                    },
                }
            }
        }
    }
});

const datasets = {
    One: {
        label: "One",
        data: [1000.00, 1020.00, 980.00, 1050.00, 1000.00, 1070.00, 1040.00],
    },
    Two: {
        label: "Two",
        data: [950.00, 920.00, 930.00, 900.00, 980.00, 970.00, 950.00],
    },
    Three: {
        label: "Three",
        data: [1100.00, 1120.00, 1180.00, 1150.00, 1100.00, 1170.00, 1140.00],
    },
    Four: {
        label: "Four",
        data: [1200.00, 1240.00, 1220.00, 1270.00, 1290.00, 1280.00, 1290.00],
    },
};

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