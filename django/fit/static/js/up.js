document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('progressForm').addEventListener('submit', (event) => {
        event.preventDefault();

        const startDate = document.getElementById('start').value;
        const endDate = document.getElementById('end').value;

        fetch(`/get_progress/?start=${startDate}&end=${endDate}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const progressContainer = document.getElementById('progress-records');


                    if (data.records.length > 0) {
                        const workoutTypes = {}; 

                        data.records.forEach(record => {
                            if (Array.isArray(record.data)) {
                                record.data.forEach(item => {
                                    if (workoutTypes[item.type]) {
                                        workoutTypes[item.type] += item.parameter;
                                    } else {
                                        workoutTypes[item.type] = item.parameter;
                                    }
                                });
                            }
                        });

                        const labels = Object.keys(workoutTypes); 
                        const dataValues = Object.values(workoutTypes); 

                        const canvasElement = document.getElementById('progressChart');
                        if (canvasElement) {
                            const ctx = canvasElement.getContext('2d');

                            
                            if (canvasElement.chart) {
                                canvasElement.chart.destroy();  
                            }

                           
                            canvasElement.chart = new Chart(ctx, {
                                type: 'bar',
                                data: {
                                    labels: labels,
                                    datasets: [{
                                        label: 'Количество',
                                        data: dataValues,
                                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                        borderColor: 'rgba(75, 192, 192, 1)',
                                        borderWidth: 1
                                    }]
                                },
                                options: {
                                    responsive: true,
                                    scales: {
                                        y: {
                                            beginAtZero: true
                                        }
                                    }
                                }
                            });
                        } else {
                            console.error('Canvas элемент с id "progressChart" не найден.');
                        }
                    } else {
                        progressContainer.innerHTML = '<p>Нет записей за этот период.</p>';
                    }
                } else {
                    alert('Ошибка: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при загрузке прогресса.');
            });
    });
});
