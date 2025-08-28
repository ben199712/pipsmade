// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initScrollAnimations();
    initTradingViewWidget();
    initCalculator();
    initChatSimulation();
    initSmoothScrolling();
    initNavbarScroll();
});

// Smooth Scrolling for Navigation Links
function initSmoothScrolling() {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 80; // Account for fixed navbar
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Navbar Scroll Effect
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(31, 41, 55, 0.98)';
            navbar.style.backdropFilter = 'blur(15px)';
        } else {
            navbar.style.background = 'rgba(31, 41, 55, 0.95)';
            navbar.style.backdropFilter = 'blur(10px)';
        }
    });
}

// Scroll Animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Add fade-in-up class to elements that should animate
    const animateElements = document.querySelectorAll('.feature-card, .step-card, .pricing-card');
    animateElements.forEach(el => {
        el.classList.add('fade-in-up');
        observer.observe(el);
    });
}

// TradingView Widget
function initTradingViewWidget() {
    if (typeof TradingView !== 'undefined') {
        new TradingView.widget({
            "width": "100%",
            "height": 400,
            "symbol": "BINANCE:BTCUSDT",
            "interval": "15",
            "timezone": "Etc/UTC",
            "theme": "light",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#f1f3f6",
            "enable_publishing": false,
            "hide_top_toolbar": false,
            "hide_legend": false,
            "save_image": false,
            "container_id": "tradingview_chart",
            "studies": [
                "MASimple@tv-basicstudies",
                "RSI@tv-basicstudies"
            ]
        });
    }
}

// Investment Calculator
function initCalculator() {
    const inputs = ['investmentAmount', 'investmentPeriod', 'riskLevel', 'compounding'];
    
    inputs.forEach(inputId => {
        const element = document.getElementById(inputId);
        if (element) {
            element.addEventListener('change', calculateReturns);
            element.addEventListener('input', calculateReturns);
        }
    });
    
    // Initial calculation
    calculateReturns();
}

function calculateReturns() {
    const amount = parseFloat(document.getElementById('investmentAmount')?.value) || 5000;
    const period = parseInt(document.getElementById('investmentPeriod')?.value) || 12;
    const riskLevel = document.getElementById('riskLevel')?.value || 'medium';
    const compounding = document.getElementById('compounding')?.value || 'monthly';
    
    // Risk level returns (annual percentage)
    const riskReturns = {
        'low': { min: 5, max: 8 },
        'medium': { min: 8, max: 12 },
        'high': { min: 12, max: 18 }
    };
    
    // Use average return for calculation
    const annualReturn = (riskReturns[riskLevel].min + riskReturns[riskLevel].max) / 2;
    
    // Compounding frequency
    const compoundingFreq = {
        'monthly': 12,
        'quarterly': 4,
        'annually': 1
    };
    
    const n = compoundingFreq[compounding];
    const r = annualReturn / 100;
    const t = period / 12; // Convert months to years
    
    // Compound interest formula: A = P(1 + r/n)^(nt)
    const totalReturn = amount * Math.pow(1 + r/n, n * t);
    const profit = totalReturn - amount;
    const roi = (profit / amount) * 100;
    
    // Update display
    updateCalculatorDisplay(totalReturn, profit, roi);
}

function updateCalculatorDisplay(totalReturn, profit, roi) {
    const totalElement = document.getElementById('totalReturn');
    const profitElement = document.getElementById('profit');
    const roiElement = document.getElementById('roi');
    
    if (totalElement) {
        totalElement.textContent = '$' + totalReturn.toLocaleString('en-US', { maximumFractionDigits: 0 });
    }
    
    if (profitElement) {
        profitElement.textContent = '$' + profit.toLocaleString('en-US', { maximumFractionDigits: 0 });
    }
    
    if (roiElement) {
        roiElement.textContent = roi.toFixed(1) + '%';
    }
}

// Chat Simulation
function initChatSimulation() {
    const chatMessages = document.querySelector('.chat-messages');
    const chatInput = document.querySelector('.chat-input input');
    const chatButton = document.querySelector('.chat-input button');
    
    if (!chatMessages || !chatInput || !chatButton) return;
    
    // Simulate new messages
    const simulatedMessages = [
        {
            sender: 'Market Alert',
            content: '🔥 ETH breaking $4,500 resistance level!',
            delay: 15000
        },
        {
            sender: 'Portfolio Manager',
            content: '📊 Your portfolio is up 3.2% today. Great performance!',
            delay: 30000
        },
        {
            sender: 'Trading Bot',
            content: '⚡ Executing buy order for AAPL at $230.50',
            delay: 45000
        }
    ];
    
    simulatedMessages.forEach(msg => {
        setTimeout(() => {
            addChatMessage(msg.sender, msg.content);
        }, msg.delay);
    });
    
    // Handle user input
    function handleChatInput() {
        const message = chatInput.value.trim();
        if (message) {
            addChatMessage('You', message);
            chatInput.value = '';
            
            // Simulate response
            setTimeout(() => {
                const responses = [
                    'Thanks for your question! Our team will get back to you shortly.',
                    'Great question! Let me connect you with our trading expert.',
                    'I\'ve noted your request. You\'ll receive a detailed response within 5 minutes.',
                    'Your inquiry has been forwarded to our analysis team.'
                ];
                const randomResponse = responses[Math.floor(Math.random() * responses.length)];
                addChatMessage('Support Team', randomResponse);
            }, 2000);
        }
    }
    
    chatButton.addEventListener('click', handleChatInput);
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleChatInput();
        }
    });
}

function addChatMessage(sender, content) {
    const chatMessages = document.querySelector('.chat-messages');
    if (!chatMessages) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message';
    
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    
    messageDiv.innerHTML = `
        <div class="message-header">
            <strong>${sender}</strong>
            <span class="time">${timeString}</span>
        </div>
        <div class="message-content">${content}</div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Add animation
    messageDiv.style.opacity = '0';
    messageDiv.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        messageDiv.style.transition = 'all 0.3s ease';
        messageDiv.style.opacity = '1';
        messageDiv.style.transform = 'translateY(0)';
    }, 100);
}

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

function formatPercentage(value) {
    return (value * 100).toFixed(1) + '%';
}

// Loading States
function showLoading(element) {
    element.classList.add('loading');
}

function hideLoading(element) {
    element.classList.remove('loading');
}

// Error Handling
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
});

// Performance Monitoring
window.addEventListener('load', function() {
    const loadTime = performance.now();
    console.log(`Page loaded in ${loadTime.toFixed(2)}ms`);
});
