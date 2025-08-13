// Portfolio Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializePortfolio();
});

function initializePortfolio() {
    // Initialize charts
    initializePortfolioCharts();
    
    // Initialize filter buttons
    const filterButtons = document.querySelectorAll('.portfolio-filters .btn');
    filterButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            filterButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            filterHoldings(this.textContent.trim());
        });
    });
    
    // Initialize chart controls
    const chartControls = document.querySelectorAll('.chart-controls .btn');
    chartControls.forEach(btn => {
        btn.addEventListener('click', function() {
            chartControls.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            updatePortfolioChart(this.textContent);
        });
    });
}

function initializePortfolioCharts() {
    // Portfolio Performance Chart
    const portfolioCtx = document.getElementById('portfolioPerformanceChart');
    if (portfolioCtx) {
        new Chart(portfolioCtx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Portfolio Value',
                    data: [10000, 10500, 10200, 11000, 11800, 12450],
                    borderColor: '#10B981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        grid: {
                            color: '#E5E7EB'
                        },
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                },
                elements: {
                    point: {
                        radius: 6,
                        hoverRadius: 8,
                        backgroundColor: '#10B981',
                        borderColor: '#ffffff',
                        borderWidth: 2
                    }
                }
            }
        });
    }
    
    // Asset Allocation Chart
    const allocationCtx = document.getElementById('assetAllocationChart');
    if (allocationCtx) {
        new Chart(allocationCtx, {
            type: 'doughnut',
            data: {
                labels: ['Crypto', 'Stocks', 'Forex', 'Bonds'],
                datasets: [{
                    data: [40, 30, 20, 10],
                    backgroundColor: [
                        '#10B981',
                        '#3B82F6',
                        '#F59E0B',
                        '#8B5CF6'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                cutout: '60%'
            }
        });
    }
}

function updatePortfolioChart(period) {
    // This would update the chart based on the selected period
    console.log('Updating portfolio chart for period:', period);
}

function filterHoldings(filter) {
    const tableRows = document.querySelectorAll('.holdings-table tbody tr');
    
    tableRows.forEach(row => {
        const assetName = row.querySelector('.asset-info h6').textContent.toLowerCase();
        const assetType = row.querySelector('.asset-info small').textContent.toLowerCase();
        
        if (filter === 'All Assets' || 
            assetName.includes(filter.toLowerCase()) || 
            assetType.includes(filter.toLowerCase()) ||
            (filter === 'Crypto' && (assetName.includes('bitcoin') || assetType.includes('btc'))) ||
            (filter === 'Stocks' && assetType.includes('aapl')) ||
            (filter === 'Forex' && assetType.includes('forex')) ||
            (filter === 'Bonds' && assetType.includes('bond'))) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}
