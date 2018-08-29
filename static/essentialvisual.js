function showEssentialVisual(data) {
    var background_colors = ["rgba(30,144,255,1)", "rgba(255,0,0,1)"]

    var options = {
        legend: {
            labels: {
                fontSize: 16
            }
        }
    };

    var data = {
        datasets: [{
            data: data,
            backgroundColor: background_colors,
            // options: options
        }],
        labels: [
            'Essential',
            'Non-Essential',
        ]
    };

    var ctx = document.getElementById("essentialVisual")

    var essentialVisual = new Chart(ctx, {
    type: 'doughnut',
    data: data,
    options: options
    });

}