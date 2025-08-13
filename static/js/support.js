// Support Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializeSupport();
});

function initializeSupport() {
    // Initialize FAQ search
    const faqSearch = document.getElementById('faqSearch');
    if (faqSearch) {
        faqSearch.addEventListener('input', searchFAQ);
    }
    
    // Initialize form handlers
    const emailForm = document.getElementById('emailSupportForm');
    if (emailForm) {
        emailForm.addEventListener('submit', handleEmailSupport);
    }
    
    const ticketForm = document.getElementById('newTicketForm');
    if (ticketForm) {
        ticketForm.addEventListener('submit', handleNewTicket);
    }
}

function startLiveChat() {
    // Simulate starting live chat
    if (window.dashboardUtils) {
        window.dashboardUtils.showNotification(
            'Connecting you to a support agent...',
            'info'
        );
    }
    
    // In a real app, this would open a chat widget
    setTimeout(() => {
        if (window.dashboardUtils) {
            window.dashboardUtils.showNotification(
                'Connected! A support agent will be with you shortly.',
                'success'
            );
        }
    }, 2000);
}

function searchFAQ() {
    const searchTerm = document.getElementById('faqSearch').value.toLowerCase();
    const faqItems = document.querySelectorAll('.accordion-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.accordion-button').textContent.toLowerCase();
        const answer = item.querySelector('.accordion-body').textContent.toLowerCase();
        
        if (question.includes(searchTerm) || answer.includes(searchTerm) || searchTerm === '') {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
}

function handleEmailSupport(e) {
    e.preventDefault();
    
    const form = e.target;
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    // Show loading state
    const submitBtn = form.closest('.modal').querySelector('.btn-primary');
    const originalText = submitBtn.textContent;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
    submitBtn.disabled = true;
    
    // Simulate sending email
    setTimeout(() => {
        // Hide modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('emailSupportModal'));
        modal.hide();
        
        // Show success message
        if (window.dashboardUtils) {
            window.dashboardUtils.showNotification(
                'Your message has been sent successfully! We\'ll respond within 2-4 hours.',
                'success'
            );
        }
        
        // Reset form
        form.reset();
        
        // Reset button
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }, 2000);
}

function handleNewTicket(e) {
    e.preventDefault();
    
    const form = e.target;
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    // Show loading state
    const submitBtn = form.closest('.modal').querySelector('.btn-primary');
    const originalText = submitBtn.textContent;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Creating...';
    submitBtn.disabled = true;
    
    // Simulate creating ticket
    setTimeout(() => {
        // Hide modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('newTicketModal'));
        modal.hide();
        
        // Generate ticket ID
        const ticketId = '#SP-' + Math.random().toString(36).substr(2, 6).toUpperCase();
        
        // Show success message
        if (window.dashboardUtils) {
            window.dashboardUtils.showNotification(
                `Support ticket ${ticketId} created successfully! You'll receive updates via email.`,
                'success'
            );
        }
        
        // Reset form
        form.reset();
        
        // Reset button
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }, 2000);
}
