const renderChart_person_per_country=(data,labels)=>{
    var ctx = document.getElementById('myChart3').getContext('2d');
    var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'No of Registered Business per categories',
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
                text:"No of Registered Business per categories"
            }
    },
});
};

const renderChartLine_person_per_country=(data,labels)=>{
    var ctx = document.getElementById('myChart4').getContext('2d');
    var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'No of Registered Business per categories',
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
                text:"No of Registered Business per categories"
            }
    },
});
};

const getChartData_person_per_country=()=>{

    fetch('/inventory/user_count_summary')
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
            renderChart_person_per_country(data,labels);
            // renderChartPie(data,labels);
            renderChartLine_person_per_country(data,labels);
            // renderChartDonut2(data,labels)
        });
};
document.onload=getChartData_person_per_country();
console.log('Hello from stat js');


