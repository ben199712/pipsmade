// Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    initializeCharts();
    initializeSidebar();
});

// Initialize Dashboard
function initializeDashboard() {
    // Sidebar toggle for mobile
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }
    
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
            if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                sidebar.classList.remove('active');
            }
        }
    });
    
    // Chart controls
    const chartControls = document.querySelectorAll('.chart-controls .btn');
    chartControls.forEach(btn => {
        btn.addEventListener('click', function() {
            chartControls.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Update chart based on selected period
            const period = this.textContent;
            updatePortfolioChart(period);
        });
    });
}

// Initialize Charts
function initializeCharts() {
    // Portfolio Performance Chart
    const portfolioCtx = document.getElementById('portfolioChart');
    if (portfolioCtx) {
        window.portfolioChart = new Chart(portfolioCtx, {
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
    const allocationCtx = document.getElementById('allocationChart');
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
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    }
                },
                cutout: '60%'
            }
        });
    }
}

// Update Portfolio Chart
function updatePortfolioChart(period) {
    if (!window.portfolioChart) return;
    
    let data, labels;
    
    switch(period) {
        case '1M':
            labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4'];
            data = [12000, 12200, 12100, 12450];
            break;
        case '3M':
            labels = ['Month 1', 'Month 2', 'Month 3'];
            data = [11000, 11800, 12450];
            break;
        case '6M':
            labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
            data = [10000, 10500, 10200, 11000, 11800, 12450];
            break;
        case '1Y':
            labels = ['Q1', 'Q2', 'Q3', 'Q4'];
            data = [9500, 10200, 11500, 12450];
            break;
        default:
            return;
    }
    
    window.portfolioChart.data.labels = labels;
    window.portfolioChart.data.datasets[0].data = data;
    window.portfolioChart.update();
}

// Initialize Sidebar
function initializeSidebar() {
    // Get current page
    const currentPage = window.location.pathname.split('/').pop();
    
    // Update active nav item
    const navLinks = document.querySelectorAll('.sidebar-nav .nav-link');
    navLinks.forEach(link => {
        link.classList.remove('active');
        const href = link.getAttribute('href');
        if (href === currentPage) {
            link.classList.add('active');
        }
    });
}

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatPercentage(value) {
    return (value > 0 ? '+' : '') + value.toFixed(1) + '%';
}

// Simulate real-time updates
function simulateRealTimeUpdates() {
    setInterval(() => {
        // Update stats with small random changes
        updateStatsCards();
    }, 30000); // Update every 30 seconds
}

function updateStatsCards() {
    const statsCards = document.querySelectorAll('.stats-card');
    
    statsCards.forEach(card => {
        const amountElement = card.querySelector('h3');
        const changeElement = card.querySelector('.stats-change');
        
        if (amountElement && changeElement) {
            // Generate small random change
            const currentValue = parseFloat(amountElement.textContent.replace(/[$,%]/g, ''));
            const changePercent = (Math.random() - 0.5) * 2; // -1% to +1%
            const newValue = currentValue * (1 + changePercent / 100);
            
            // Update display
            if (amountElement.textContent.includes('$')) {
                amountElement.textContent = formatCurrency(newValue);
            } else if (amountElement.textContent.includes('%')) {
                amountElement.textContent = newValue.toFixed(1) + '%';
            } else {
                amountElement.textContent = Math.round(newValue).toString();
            }
            
            // Update change indicator
            changeElement.textContent = formatPercentage(changePercent);
            changeElement.className = 'stats-change ' + (changePercent > 0 ? 'positive' : changePercent < 0 ? 'negative' : 'neutral');
        }
    });
}

// Initialize real-time updates
// simulateRealTimeUpdates();

// Notification handling
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Export functions for use in other pages
window.dashboardUtils = {
    formatCurrency,
    formatPercentage,
    showNotification,
    initializeSidebar
};
