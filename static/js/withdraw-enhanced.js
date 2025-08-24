/**
 * Enhanced Withdrawal Page JavaScript
 * Provides interactive features and better user experience
 */

console.log('withdraw-enhanced.js loaded successfully');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded - Starting initialization');
    initializeWithdrawPage();
});

function initializeWithdrawPage() {
    console.log('initializeWithdrawPage called');
    
    // Initialize all components
    initializeWalletSelection();
    initializeFormValidation();
    initializeBalanceToggle();
    initializeCounterAnimations();
    initializeFeeCalculator();
    initializeCharts();
    
    // Simple test: Check if we can find the submit button
    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn) {
        console.log('Found submit button:', submitBtn);
        console.log('Submit button disabled state:', submitBtn.disabled);
        
        // Add a test button to manually enable submit button
        const testButton = document.createElement('button');
        testButton.type = 'button';
        testButton.className = 'btn btn-info btn-sm ms-2';
        testButton.textContent = 'TEST: Enable Submit';
        testButton.onclick = function() {
            submitBtn.disabled = false;
            console.log('Manually enabled submit button');
        };
        
        // Insert test button after submit button
        submitBtn.parentNode.insertBefore(testButton, submitBtn.nextSibling);
    } else {
        console.error('Submit button not found!');
    }
    
    console.log('Enhanced withdrawal page initialized');
}

// Wallet Selection Functionality
function initializeWalletSelection() {
    const walletCards = document.querySelectorAll('.crypto-balance-card.interactive-card');
    const cryptoSelect = document.getElementById('cryptoType');
    const amountInput = document.getElementById('withdrawAmount');
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
    const cryptoSelect = document.getElementById('cryptoType');
    const amountInput = document.getElementById('withdrawAmount');
    const availableBalanceText = document.getElementById('availableBalance');
    const networkSelect = document.getElementById('network');
    
    // Update form fields
    if (cryptoSelect) {
        cryptoSelect.value = crypto;
        cryptoSelect.dispatchEvent(new Event('change'));
    }
    
    // Update network field based on selected crypto
    if (networkSelect) {
        updateNetworkChoices(crypto);
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

// Update network choices based on selected cryptocurrency
function updateNetworkChoices(cryptoType) {
    const networkSelect = document.getElementById('network');
    if (!networkSelect) return;
    
    // Define network mappings for each crypto type
    const networkMappings = {
        'BTC': ['BTC'],
        'ETH': ['ETH', 'ERC-20'],
        'USDT': ['ERC-20', 'BEP-20', 'TRC-20'],
        'LTC': ['LTC'],
        'BCH': ['BCH'],
        'XRP': ['XRP'],
        'ADA': ['ADA'],
        'DOT': ['DOT'],
        'LINK': ['ERC-20'],
        'BNB': ['BEP-20'],
        'SOL': ['SOL'],
        'MATIC': ['MATIC'],
        'AVAX': ['AVAX'],
        'UNI': ['ERC-20'],
        'ATOM': ['ATOM']
    };
    
    // Get available networks for selected crypto
    const availableNetworks = networkMappings[cryptoType] || ['ERC-20', 'BEP-20', 'TRC-20'];
    
    // Clear current options
    networkSelect.innerHTML = '';
    
    // Add new options
    availableNetworks.forEach(network => {
        const option = document.createElement('option');
        option.value = network;
        
        // Get display name for network
        const networkNames = {
            'BTC': 'Bitcoin Network (BTC)',
            'ETH': 'Ethereum Network (ETH)',
            'ERC-20': 'Ethereum ERC-20 (Tokens)',
            'BEP-20': 'Binance Smart Chain (BEP-20)',
            'TRC-20': 'Tron Network (TRC-20)',
            'LTC': 'Litecoin Network (LTC)',
            'BCH': 'Bitcoin Cash Network (BCH)',
            'XRP': 'Ripple Network (XRP)',
            'ADA': 'Cardano Network (ADA)',
            'DOT': 'Polkadot Network (DOT)',
            'SOL': 'Solana Network (SOL)',
            'MATIC': 'Polygon Network (MATIC)',
            'AVAX': 'Avalanche Network (AVAX)',
            'ATOM': 'Cosmos Network (ATOM)'
        };
        
        option.textContent = networkNames[network] || network;
        networkSelect.appendChild(option);
    });
    
    // Set default selection
    if (availableNetworks.length > 0) {
        networkSelect.value = availableNetworks[0];
    }
}

// Form Validation
function initializeFormValidation() {
    console.log('initializeFormValidation called');
    
    const form = document.getElementById('withdrawForm');
    const submitBtn = document.getElementById('submitBtn');
    const confirmCheckbox = document.getElementById('confirmWithdrawal');
    
    console.log('Basic elements found:', {
        form: !!form,
        submitBtn: !!submitBtn,
        confirmCheckbox: !!confirmCheckbox
    });
    
    // Simple approach: Just enable button when checkbox is checked
    if (confirmCheckbox && submitBtn) {
        confirmCheckbox.addEventListener('change', function() {
            console.log('Checkbox changed, checked:', this.checked);
            submitBtn.disabled = !this.checked;
            console.log('Submit button disabled:', submitBtn.disabled);
        });
        
        // Initial state
        submitBtn.disabled = !confirmCheckbox.checked;
        console.log('Initial submit button state - disabled:', submitBtn.disabled);
        
        // Add a manual enable button for testing
        const manualEnableBtn = document.createElement('button');
        manualEnableBtn.type = 'button';
        manualEnableBtn.className = 'btn btn-success btn-sm ms-2';
        manualEnableBtn.textContent = 'Enable Submit';
        manualEnableBtn.onclick = function() {
            submitBtn.disabled = false;
            console.log('Manually enabled submit button');
        };
        
        // Insert manual enable button after submit button
        submitBtn.parentNode.insertBefore(manualEnableBtn, submitBtn.nextSibling);
    }
    
    // Add form submission handler
    if (form) {
        form.addEventListener('submit', function(e) {
            console.log('Form submission attempted');
            // Allow submission if checkbox is checked
            if (!confirmCheckbox.checked) {
                e.preventDefault();
                console.log('Checkbox not checked, preventing submission');
                return false;
            }
            console.log('Form submission allowed');
        });
    }
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
    const amountInput = document.getElementById('withdrawAmount');
    const cryptoSelect = document.getElementById('cryptoType');
    
    if (amountInput) {
        amountInput.addEventListener('input', calculateFees);
    }
    
    if (cryptoSelect) {
        cryptoSelect.addEventListener('change', calculateFees);
    }
}

function calculateFees() {
    const amount = parseFloat(document.getElementById('withdrawAmount')?.value) || 0;
    const crypto = document.getElementById('cryptoType')?.value;
    
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
