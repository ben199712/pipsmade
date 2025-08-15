/**
 * Enhanced Withdrawal Page JavaScript
 * Provides interactive features and better user experience
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeWithdrawPage();
});

function initializeWithdrawPage() {
    // Initialize all components
    initializeWalletSelection();
    initializeFormValidation();
    initializeBalanceToggle();
    initializeCounterAnimations();
    initializeFeeCalculator();
    initializeCharts();
    
    console.log('Enhanced withdrawal page initialized');
}

// Wallet Selection Functionality
function initializeWalletSelection() {
    const walletCards = document.querySelectorAll('.crypto-balance-card.interactive-card');
    const cryptoSelect = document.getElementById('id_crypto_type');
    const amountInput = document.getElementById('id_amount');
    const maxButton = document.getElementById('maxButton');
    
    // Add click handlers to wallet cards
    walletCards.forEach(card => {
        card.addEventListener('click', function() {
            const crypto = this.dataset.crypto;
            const balance = this.dataset.balance;
            selectWallet(crypto, balance);
        });
        
        // Add hover effects
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 10px 25px rgba(0,0,0,0.1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 5px 15px rgba(0,0,0,0.05)';
        });
    });
    
    // Max button functionality
    if (maxButton) {
        maxButton.addEventListener('click', function() {
            const selectedCrypto = cryptoSelect?.value;
            if (selectedCrypto) {
                const walletCard = document.querySelector(`[data-crypto="${selectedCrypto}"]`);
                if (walletCard) {
                    const balance = walletCard.dataset.balance;
                    amountInput.value = balance;
                    calculateFees();
                }
            }
        });
    }
}

// Wallet Selection Function
function selectWallet(crypto, balance) {
    const cryptoSelect = document.getElementById('id_crypto_type');
    const amountInput = document.getElementById('id_amount');
    const availableBalanceText = document.getElementById('availableBalance');
    
    // Update form fields
    if (cryptoSelect) {
        cryptoSelect.value = crypto;
        cryptoSelect.dispatchEvent(new Event('change'));
    }
    
    // Update available balance text
    if (availableBalanceText) {
        availableBalanceText.textContent = `Available: ${balance} ${crypto}`;
        availableBalanceText.className = 'form-text text-success';
    }
    
    // Clear amount field and focus
    if (amountInput) {
        amountInput.value = '';
        amountInput.focus();
        amountInput.placeholder = `Enter amount (Max: ${balance})`;
    }
    
    // Highlight selected wallet
    document.querySelectorAll('.crypto-balance-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    const selectedCard = document.querySelector(`[data-crypto="${crypto}"]`);
    if (selectedCard) {
        selectedCard.classList.add('selected');
    }
    
    // Show success message
    showNotification(`Selected ${crypto} wallet with ${balance} available`, 'success');
}

// Form Validation
function initializeFormValidation() {
    const form = document.getElementById('withdrawForm');
    const submitBtn = document.getElementById('submitBtn');
    const confirmCheckbox = document.getElementById('confirmWithdrawal');
    
    if (form) {
        form.addEventListener('input', validateForm);
        form.addEventListener('change', validateForm);
    }
    
    if (confirmCheckbox) {
        confirmCheckbox.addEventListener('change', function() {
            if (submitBtn) {
                submitBtn.disabled = !this.checked;
            }
        });
    }
}

function validateForm() {
    const cryptoSelect = document.getElementById('id_crypto_type');
    const amountInput = document.getElementById('id_amount');
    const destinationInput = document.getElementById('id_destination_address');
    const confirmAddressInput = document.getElementById('id_confirm_address');
    const submitBtn = document.getElementById('submitBtn');
    
    let isValid = true;
    
    // Validate crypto selection
    if (!cryptoSelect?.value) {
        isValid = false;
    }
    
    // Validate amount
    if (!amountInput?.value || parseFloat(amountInput.value) <= 0) {
        isValid = false;
    }
    
    // Validate addresses match
    if (destinationInput?.value !== confirmAddressInput?.value) {
        isValid = false;
        if (confirmAddressInput?.value) {
            showFieldError(confirmAddressInput, 'Addresses do not match');
        }
    } else if (confirmAddressInput?.value) {
        clearFieldError(confirmAddressInput);
    }
    
    // Update submit button
    if (submitBtn) {
        submitBtn.disabled = !isValid || !document.getElementById('confirmWithdrawal')?.checked;
    }
    
    return isValid;
}

// Balance Toggle Functionality
function initializeBalanceToggle() {
    const toggleBtn = document.getElementById('toggleBalanceView');
    
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            const balanceValues = document.querySelectorAll('.balance-value');
            const balanceHidden = document.querySelectorAll('.balance-hidden');
            const icon = this.querySelector('i');
            
            balanceValues.forEach((el, index) => {
                if (el.style.display === 'none') {
                    el.style.display = 'inline';
                    balanceHidden[index].style.display = 'none';
                    this.innerHTML = '<i class="fas fa-eye"></i> Hide Balances';
                } else {
                    el.style.display = 'none';
                    balanceHidden[index].style.display = 'inline';
                    this.innerHTML = '<i class="fas fa-eye-slash"></i> Show Balances';
                }
            });
        });
    }
}

// Counter Animations
function initializeCounterAnimations() {
    const counters = document.querySelectorAll('.counter');
    
    counters.forEach(counter => {
        const target = parseFloat(counter.dataset.target) || 0;
        const duration = 2000; // 2 seconds
        const increment = target / (duration / 16); // 60fps
        let current = 0;
        
        const updateCounter = () => {
            current += increment;
            if (current < target) {
                counter.textContent = current.toFixed(2);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target.toFixed(2);
            }
        };
        
        // Start animation when element is visible
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    updateCounter();
                    observer.unobserve(entry.target);
                }
            });
        });
        
        observer.observe(counter);
    });
}

// Fee Calculator
function initializeFeeCalculator() {
    const amountInput = document.getElementById('id_amount');
    const cryptoSelect = document.getElementById('id_crypto_type');
    
    if (amountInput) {
        amountInput.addEventListener('input', calculateFees);
    }
    
    if (cryptoSelect) {
        cryptoSelect.addEventListener('change', calculateFees);
    }
}

function calculateFees() {
    const amount = parseFloat(document.getElementById('id_amount')?.value) || 0;
    const crypto = document.getElementById('id_crypto_type')?.value;
    
    if (amount > 0 && crypto) {
        // Fee percentages (should match backend)
        const feeRates = {
            'BTC': 0.02,
            'ETH': 0.025,
            'USDT': 0.015,
            'BNB': 0.02
        };
        
        const feeRate = feeRates[crypto] || 0.02;
        const platformFee = amount * feeRate;
        const netAmount = amount - platformFee;
        
        // Update fee calculator display
        const feeCalculator = document.getElementById('feeCalculator');
        if (feeCalculator) {
            feeCalculator.style.display = 'block';
            
            document.getElementById('withdrawalAmount').textContent = `${amount} ${crypto}`;
            document.getElementById('platformFee').textContent = `${platformFee.toFixed(8)} ${crypto}`;
            document.getElementById('netAmount').textContent = `${netAmount.toFixed(8)} ${crypto}`;
        }
    }
}

// Mini Charts
function initializeCharts() {
    // Simple sparkline charts for stats cards
    const charts = ['balanceChart', 'withdrawalChart', 'pendingChart'];
    
    charts.forEach(chartId => {
        const canvas = document.getElementById(chartId);
        if (canvas) {
            drawSparkline(canvas, generateSampleData());
        }
    });
}

function drawSparkline(canvas, data) {
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    ctx.clearRect(0, 0, width, height);
    ctx.strokeStyle = '#28a745';
    ctx.lineWidth = 2;
    
    const max = Math.max(...data);
    const min = Math.min(...data);
    const range = max - min || 1;
    
    ctx.beginPath();
    data.forEach((value, index) => {
        const x = (index / (data.length - 1)) * width;
        const y = height - ((value - min) / range) * height;
        
        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    
    ctx.stroke();
}

function generateSampleData() {
    return Array.from({length: 10}, () => Math.random() * 100);
}

// Utility Functions
function showNotification(message, type = 'info') {
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

function showFieldError(field, message) {
    clearFieldError(field);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback d-block';
    errorDiv.textContent = message;
    
    field.classList.add('is-invalid');
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    field.classList.remove('is-invalid');
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function refreshBalances() {
    showNotification('Refreshing wallet balances...', 'info');
    
    // Simulate API call
    setTimeout(() => {
        showNotification('Wallet balances updated successfully!', 'success');
        // In real implementation, this would fetch fresh data from the server
    }, 1500);
}

// Live Chat Integration
function startLiveChat() {
    showNotification('Connecting to live chat...', 'info');
    
    // In real implementation, this would integrate with a chat service
    setTimeout(() => {
        showNotification('Live chat is currently unavailable. Please create a support ticket.', 'warning');
    }, 1000);
}
