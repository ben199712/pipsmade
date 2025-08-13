// Withdraw Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializeWithdraw();
});

function initializeWithdraw() {
    // Initialize form handlers
    const methodSelect = document.getElementById('withdrawMethod');
    const amountInput = document.getElementById('withdrawAmount');
    
    if (methodSelect) {
        methodSelect.addEventListener('change', function() {
            showWithdrawForm(this.value);
            updateWithdrawSummary();
        });
    }
    
    if (amountInput) {
        amountInput.addEventListener('input', updateWithdrawSummary);
    }
    
    // Initialize withdraw form
    const withdrawForm = document.getElementById('withdrawForm');
    if (withdrawForm) {
        withdrawForm.addEventListener('submit', handleWithdrawSubmit);
    }
}

function showWithdrawForm(method) {
    // Hide all forms
    const forms = document.querySelectorAll('.withdraw-form-section');
    forms.forEach(form => form.style.display = 'none');
    
    // Show selected form
    if (method) {
        const targetForm = document.getElementById(method + 'WithdrawForm');
        if (targetForm) {
            targetForm.style.display = 'block';
        }
    }
}

function updateWithdrawSummary() {
    const methodSelect = document.getElementById('withdrawMethod');
    const amountInput = document.getElementById('withdrawAmount');
    const summaryAmount = document.getElementById('withdrawSummaryAmount');
    const summaryFee = document.getElementById('withdrawSummaryFee');
    const summaryTotal = document.getElementById('withdrawSummaryTotal');
    const summaryTime = document.getElementById('withdrawSummaryTime');
    
    if (!methodSelect || !amountInput) return;
    
    const method = methodSelect.value;
    const amount = parseFloat(amountInput.value) || 0;
    
    // Fee structure
    const fees = {
        'bank': 5, // Fixed fee
        'crypto': 0, // Network fee varies
        'paypal': amount * 0.025 // 2.5%
    };
    
    // Processing times
    const processingTimes = {
        'bank': '1-3 business days',
        'crypto': '10-60 minutes',
        'paypal': '1-2 business days'
    };
    
    let fee = 0;
    if (method && fees[method] !== undefined) {
        fee = fees[method];
    }
    
    const total = amount - fee;
    
    if (summaryAmount) {
        summaryAmount.textContent = formatCurrency(amount);
    }
    
    if (summaryFee) {
        summaryFee.textContent = formatCurrency(fee);
    }
    
    if (summaryTotal) {
        summaryTotal.textContent = formatCurrency(Math.max(0, total));
    }
    
    if (summaryTime && method) {
        summaryTime.textContent = processingTimes[method] || '-';
    }
}

function setMaxAmount() {
    const amountInput = document.getElementById('withdrawAmount');
    const maxAmount = 12450; // Available balance
    
    if (amountInput) {
        amountInput.value = maxAmount;
        updateWithdrawSummary();
    }
}

function handleWithdrawSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const methodSelect = document.getElementById('withdrawMethod');
    const amountInput = document.getElementById('withdrawAmount');
    
    const method = methodSelect.value;
    const amount = parseFloat(amountInput.value);
    
    // Show loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
    submitBtn.disabled = true;
    
    // Simulate processing
    setTimeout(() => {
        // Show success message
        if (window.dashboardUtils) {
            window.dashboardUtils.showNotification(
                `Withdrawal request of ${formatCurrency(amount)} via ${method} submitted successfully!`,
                'success'
            );
        }
        
        // Reset form
        form.reset();
        showWithdrawForm('');
        updateWithdrawSummary();
        
        // Reset button
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
        
    }, 3000);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}
