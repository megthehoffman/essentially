// Designed with guidance from https://jsfiddle.net/m7s43hrs/
function showEssentialVisual(category_sums) {

var ctx = document.getElementById("essentialVisual");

var essentialVisual = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: [
            'Essential',
            'Non-Essential',
        ],
    datasets: [{
      data: category_sums,
      backgroundColor: ["rgba(30,144,255,1)", "rgba(255,0,0,1)"]
    }]
  },
  options: {
    layout: {
        padding: {
            left: 0,
            right: 0,
            top: 40,
            bottom: 0
        }
    },
    legend: {
        labels: {
            fontSize: 16
        }
    },
    tooltips: {
      callbacks: {
        title: function(tooltipItem, data) {
          return data['labels'][tooltipItem[0]['index']];    
        },
        label: function(tooltipItem, data) {
          var sum = data['datasets'][0]['data'][tooltipItem['index']];
          return '$' + sum.toFixed(2)
        },
        },
            backgroundColor: '#FFF',
            titleFontSize: 14,
            titleFontColor: '#666',
            bodyFontColor: '#666',
            bodyFontSize: 12,
            displayColors: false
        }
      }
    });

}

