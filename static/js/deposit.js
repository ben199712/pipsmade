// Deposit Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializeDeposit();
});

function initializeDeposit() {
    // Initialize form handlers
    const methodSelect = document.getElementById('depositMethod');
    const amountInput = document.getElementById('depositAmount');
    
    if (methodSelect) {
        methodSelect.addEventListener('change', function() {
            showDepositForm(this.value);
            updateDepositSummary();
        });
    }
    
    if (amountInput) {
        amountInput.addEventListener('input', updateDepositSummary);
    }
    
    // Initialize deposit form
    const depositForm = document.getElementById('depositForm');
    if (depositForm) {
        depositForm.addEventListener('submit', handleDepositSubmit);
    }
    
    // Initialize card number formatting
    const cardNumberInput = document.querySelector('#cardForm input[placeholder*="1234"]');
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', formatCardNumber);
    }
    
    // Initialize expiry date formatting
    const expiryInput = document.querySelector('#cardForm input[placeholder="MM/YY"]');
    if (expiryInput) {
        expiryInput.addEventListener('input', formatExpiryDate);
    }
}

function selectMethod(method) {
    const methodSelect = document.getElementById('depositMethod');
    if (methodSelect) {
        methodSelect.value = method;
        showDepositForm(method);
        updateDepositSummary();
    }
    
    // Update method selection UI
    const methodCards = document.querySelectorAll('.deposit-method');
    methodCards.forEach(card => {
        card.classList.remove('selected');
        if (card.dataset.method === method) {
            card.classList.add('selected');
        }
    });
}

function showDepositForm(method) {
    // Hide all forms
    const forms = document.querySelectorAll('.deposit-form-section');
    forms.forEach(form => form.style.display = 'none');
    
    // Show selected form
    if (method) {
        const targetForm = document.getElementById(method + 'Form');
        if (targetForm) {
            targetForm.style.display = 'block';
        }
    }
}

function updateDepositSummary() {
    const methodSelect = document.getElementById('depositMethod');
    const amountInput = document.getElementById('depositAmount');
    const summaryAmount = document.getElementById('summaryAmount');
    const summaryFee = document.getElementById('summaryFee');
    const summaryTotal = document.getElementById('summaryTotal');
    const summaryTime = document.getElementById('summaryTime');
    
    if (!methodSelect || !amountInput) return;
    
    const method = methodSelect.value;
    const amount = parseFloat(amountInput.value) || 0;
    
    // Fee structure
    const fees = {
        'bank': 0,
        'card': 0.029, // 2.9%
        'crypto': 0 // Network fee varies
    };
    
    // Processing times
    const processingTimes = {
        'bank': 'Instant',
        'card': 'Instant',
        'crypto': '10-30 minutes'
    };
    
    let fee = 0;
    if (method && fees[method] !== undefined) {
        fee = amount * fees[method];
    }
    
    const total = amount - fee;
    
    if (summaryAmount) {
        summaryAmount.textContent = formatCurrency(amount);
    }
    
    if (summaryFee) {
        summaryFee.textContent = formatCurrency(fee);
    }
    
    if (summaryTotal) {
        summaryTotal.textContent = formatCurrency(total);
    }
    
    if (summaryTime && method) {
        summaryTime.textContent = processingTimes[method] || '-';
    }
}

function handleDepositSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const methodSelect = document.getElementById('depositMethod');
    const amountInput = document.getElementById('depositAmount');
    
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
                `Deposit of ${formatCurrency(amount)} via ${method} processed successfully!`,
                'success'
            );
        }
        
        // Reset form
        form.reset();
        showDepositForm('');
        updateDepositSummary();
        
        // Reset button
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
        
        // Remove method selection
        const methodCards = document.querySelectorAll('.deposit-method');
        methodCards.forEach(card => card.classList.remove('selected'));
        
    }, 3000);
}

function formatCardNumber(e) {
    let value = e.target.value.replace(/\s/g, '').replace(/[^0-9]/gi, '');
    let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
    e.target.value = formattedValue;
}

function formatExpiryDate(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length >= 2) {
        value = value.substring(0, 2) + '/' + value.substring(2, 4);
    }
    e.target.value = value;
}

function copyAddress() {
    const addressInput = document.querySelector('.crypto-address input');
    if (addressInput) {
        addressInput.select();
        document.execCommand('copy');
        
        if (window.dashboardUtils) {
            window.dashboardUtils.showNotification('Address copied to clipboard!', 'success');
        }
    }
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}
