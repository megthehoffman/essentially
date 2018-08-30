function showEssentialVisual(num_data) {

var ctx = document.getElementById("essentialVisual");

var essentialVisual = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: [
            'Essential',
            'Non-Essential',
        ],
    datasets: [{
      data: num_data,
      backgroundColor: ["rgba(30,144,255,1)", "rgba(255,0,0,1)"]
    }]
  },
  options: {
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
          return data['datasets'][0]['data'][tooltipItem['index']];
        },
        afterLabel: function(tooltipItem, data) {
          var dataset = data['datasets'][0];
          console.log(dataset)
          var percent = Math.round((dataset['data'][tooltipItem['index']] / dataset["_meta"][0]['total']) * 100)
          console.log(dataset['data'][tooltipItem['index']])
          console.log('cat')
          console.log(dataset["_meta"][0]['total'])
          return '(' + percent + '%)';
        }
        },
            backgroundColor: '#FFF',
            titleFontSize: 14,
            titleFontColor: '#0066ff',
            bodyFontColor: '#000',
            bodyFontSize: 12,
            displayColors: false
        }
      }
    });

}