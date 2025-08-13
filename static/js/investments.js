// Investments Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializeInvestments();
});

function initializeInvestments() {
    // Initialize form handlers
    const planSelect = document.getElementById('planSelect');
    const amountInput = document.getElementById('investmentAmount');
    const durationSelect = document.getElementById('durationSelect');
    
    if (planSelect) {
        planSelect.addEventListener('change', updateInvestmentSummary);
    }
    
    if (amountInput) {
        amountInput.addEventListener('input', updateInvestmentSummary);
    }
    
    if (durationSelect) {
        durationSelect.addEventListener('change', updateInvestmentSummary);
    }
    
    // Initialize filter buttons
    const filterButtons = document.querySelectorAll('.investment-filters .btn');
    filterButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            filterButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            filterInvestments(this.textContent.trim());
        });
    });
}

function selectPlan(planType) {
    // Update modal form
    const planSelect = document.getElementById('planSelect');
    if (planSelect) {
        planSelect.value = planType;
        updateInvestmentSummary();
    }
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('newInvestmentModal'));
    modal.show();
}

function updateInvestmentSummary() {
    const planSelect = document.getElementById('planSelect');
    const amountInput = document.getElementById('investmentAmount');
    const durationSelect = document.getElementById('durationSelect');
    const expectedROI = document.getElementById('expectedROI');
    const summaryAmount = document.getElementById('summaryAmount');
    const summaryReturn = document.getElementById('summaryReturn');
    const summaryTotal = document.getElementById('summaryTotal');
    
    if (!planSelect || !amountInput || !durationSelect) return;
    
    const plan = planSelect.value;
    const amount = parseFloat(amountInput.value) || 0;
    const duration = parseInt(durationSelect.value) || 0;
    
    // ROI rates for different plans
    const roiRates = {
        'crypto': { min: 15, max: 25 },
        'stocks': { min: 8, max: 15 },
        'forex': { min: 10, max: 18 },
        'bonds': { min: 5, max: 8 }
    };
    
    if (plan && roiRates[plan]) {
        const avgROI = (roiRates[plan].min + roiRates[plan].max) / 2;
        const annualizedROI = avgROI * (duration / 365);
        const expectedReturn = amount * (annualizedROI / 100);
        const totalPayout = amount + expectedReturn;
        
        if (expectedROI) {
            expectedROI.value = `${avgROI}% annually`;
        }
        
        if (summaryAmount) {
            summaryAmount.textContent = formatCurrency(amount);
        }
        
        if (summaryReturn) {
            summaryReturn.textContent = formatCurrency(expectedReturn);
        }
        
        if (summaryTotal) {
            summaryTotal.textContent = formatCurrency(totalPayout);
        }
    }
}

function createInvestment() {
    const form = document.getElementById('investmentForm');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    // Simulate investment creation
    const planSelect = document.getElementById('planSelect');
    const amountInput = document.getElementById('investmentAmount');
    
    const plan = planSelect.value;
    const amount = parseFloat(amountInput.value);
    
    // Show loading state
    const submitBtn = document.querySelector('#newInvestmentModal .btn-primary');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Creating Investment...';
    submitBtn.disabled = true;
    
    setTimeout(() => {
        // Hide modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('newInvestmentModal'));
        modal.hide();
        
        // Show success message
        if (window.dashboardUtils) {
            window.dashboardUtils.showNotification(
                `Investment of ${formatCurrency(amount)} in ${plan} plan created successfully!`,
                'success'
            );
        }
        
        // Reset form
        form.reset();
        updateInvestmentSummary();
        
        // Reset button
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }, 2000);
}

function filterInvestments(filter) {
    const tableRows = document.querySelectorAll('.investment-table tbody tr');
    
    tableRows.forEach(row => {
        const investmentType = row.querySelector('.investment-info h6').textContent.toLowerCase();
        
        if (filter === 'All' || investmentType.includes(filter.toLowerCase())) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}
