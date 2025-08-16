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
    
    // Initialize email support form
    const emailForm = document.getElementById('emailSupportForm');
    if (emailForm) {
        emailForm.addEventListener('submit', handleEmailSupport);
    }
    
    // Initialize new ticket form
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
    const submitBtn = document.getElementById('emailSubmitBtn');
    
    // Validate form
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    // Show loading state
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
    submitBtn.disabled = true;
    
    // Create FormData for file uploads
    const formData = new FormData(form);
    
    // Send AJAX request
    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Hide modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('emailSupportModal'));
            modal.hide();
            
            // Show success message
            if (window.dashboardUtils && window.dashboardUtils.showNotification) {
                window.dashboardUtils.showNotification(data.message, 'success');
            } else {
                // Fallback notification
                alert(data.message);
            }
            
            // Reset form
            form.reset();
            
            // Show ticket created message
            setTimeout(() => {
                if (window.dashboardUtils && window.dashboardUtils.showNotification) {
                    window.dashboardUtils.showNotification(
                        `Support ticket #${data.ticket_id} has been created. You can track it in your tickets.`,
                        'info'
                    );
                }
            }, 1000);
            
        } else {
            // Show error message
            if (window.dashboardUtils && window.dashboardUtils.showNotification) {
                window.dashboardUtils.showNotification(data.message, 'error');
            } else {
                alert(data.message);
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (window.dashboardUtils && window.dashboardUtils.showNotification) {
            window.dashboardUtils.showNotification('An error occurred while sending your email. Please try again.', 'error');
        } else {
            alert('An error occurred while sending your email. Please try again.');
        }
    })
    .finally(() => {
        // Reset button
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    });
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
