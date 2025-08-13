// Transactions Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializeTransactions();
});

function initializeTransactions() {
    // Initialize filter handlers
    const typeFilter = document.getElementById('typeFilter');
    const statusFilter = document.getElementById('statusFilter');
    const dateFilter = document.getElementById('dateFilter');
    const searchFilter = document.getElementById('searchFilter');
    
    if (typeFilter) {
        typeFilter.addEventListener('change', filterTransactions);
    }
    
    if (statusFilter) {
        statusFilter.addEventListener('change', filterTransactions);
    }
    
    if (dateFilter) {
        dateFilter.addEventListener('change', filterTransactions);
    }
    
    if (searchFilter) {
        searchFilter.addEventListener('input', filterTransactions);
    }
}

function filterTransactions() {
    const typeFilter = document.getElementById('typeFilter');
    const statusFilter = document.getElementById('statusFilter');
    const dateFilter = document.getElementById('dateFilter');
    const searchFilter = document.getElementById('searchFilter');
    
    const typeValue = typeFilter ? typeFilter.value.toLowerCase() : '';
    const statusValue = statusFilter ? statusFilter.value.toLowerCase() : '';
    const dateValue = dateFilter ? dateFilter.value.toLowerCase() : '';
    const searchValue = searchFilter ? searchFilter.value.toLowerCase() : '';
    
    const tableRows = document.querySelectorAll('.transaction-table tbody tr');
    
    tableRows.forEach(row => {
        const type = row.querySelector('.transaction-type span').textContent.toLowerCase();
        const status = row.querySelector('.badge').textContent.toLowerCase();
        const description = row.cells[2].textContent.toLowerCase();
        const date = row.querySelector('.transaction-date div').textContent.toLowerCase();
        
        let showRow = true;
        
        // Type filter
        if (typeValue && !type.includes(typeValue)) {
            showRow = false;
        }
        
        // Status filter
        if (statusValue && !status.includes(statusValue)) {
            showRow = false;
        }
        
        // Search filter
        if (searchValue && !description.includes(searchValue) && !type.includes(searchValue)) {
            showRow = false;
        }
        
        // Date filter (simplified - in real app would use actual date comparison)
        if (dateValue && dateValue !== 'all') {
            // This is a simplified implementation
            // In a real app, you'd parse dates and compare properly
        }
        
        row.style.display = showRow ? '' : 'none';
    });
}

function viewTransaction(transactionId) {
    // Show transaction details modal
    const modal = new bootstrap.Modal(document.getElementById('transactionModal'));
    modal.show();
    
    // In a real app, you'd fetch transaction details by ID
    console.log('Viewing transaction:', transactionId);
}

function exportTransactions() {
    // Simulate export functionality
    if (window.dashboardUtils) {
        window.dashboardUtils.showNotification(
            'Transaction export started. You will receive an email when ready.',
            'info'
        );
    }
    
    // In a real app, you'd trigger the actual export
    console.log('Exporting transactions...');
}
