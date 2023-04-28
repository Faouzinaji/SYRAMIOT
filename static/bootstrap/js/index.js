const renderChart=(data,labels)=>{
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'Legal Entity Per Country',
            data: data,
            backgroundColor: [
                 'rgba(99, 255, 132, 1)',
                'rgba(28, 245, 6, 0.55)',
                'rgba(255, 206, 86,1)',
                'rgba(221, 242, 16, 0.55)',
                'rgba(142, 12, 247, 0.55)',
                'rgba(247, 12, 196, 0.55)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
            title:{
                display:true,
                text:"Legal Entity Per Country"
            }
    },
});
};
const renderChartLine=(data,labels)=>{
    var ctx = document.getElementById('myChart2').getContext('2d');
    var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Legal Entity Per Country',
            data: data,
            backgroundColor: [
                  'rgba(99, 255, 132, 1)',
                'rgba(28, 245, 6, 0.55)',
                'rgba(255, 206, 86,1)',
                'rgba(221, 242, 16, 0.55)',
                'rgba(142, 12, 247, 0.55)',
                'rgba(247, 12, 196, 0.55)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
            title:{
                display:true,
                text:"Legal Entity Per Country"
            }
    },
});
};

const getChartData=()=>{

    fetch('/inventory/legal_entity_summary')
        .then((res)=>res.json())
        .then(
            (results)=>
            {
            console.log('results',results.users_data);
            const category_data=results.users_data;
            const [labels,data]=[
                Object.keys(category_data),
                Object.values(category_data)
            ];
            renderChart(data,labels);
            renderChartLine(data,labels);
            // renderChartPie(data,labels);

            // renderChartDonut(data,labels);
        });
};
document.onload=getChartData();


