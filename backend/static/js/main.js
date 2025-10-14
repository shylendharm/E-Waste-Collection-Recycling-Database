// JavaScript for e-waste management system

document.addEventListener('DOMContentLoaded', function() {
    // Modal functionality for editing
    const modal = document.getElementById('edit-modal');
    const closeBtn = document.querySelector('.close');
    const editForm = document.getElementById('edit-form');
    
    // Function to fetch record details and populate the edit form
    async function populateEditForm(recordId) {
        try {
            const response = await fetch(`/ewaste_records/${recordId}`);
            const record = await response.json();
            
            if (record) {
                document.getElementById('edit-record-id').value = record.record_id;
                document.getElementById('edit-item-type').value = record.item_type;
                document.getElementById('edit-quantity').value = record.quantity;
                document.getElementById('edit-location').value = record.location;
                document.getElementById('edit-date').value = record.collection_date;
                document.getElementById('edit-status').value = record.status;
            }
        } catch (error) {
            console.error('Error fetching record:', error);
            alert('Error fetching record details');
        }
    }
    
    // Open modal when edit button is clicked
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', function() {
            const recordId = this.getAttribute('data-id');
            populateEditForm(recordId);
            modal.style.display = 'block';
        });
    });
    
    // Close modal when X is clicked
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    
    // Close modal when clicking outside of it
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    // Delete button functionality
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', async function() {
            const recordId = this.getAttribute('data-id');
            if (confirm('Are you sure you want to delete this record?')) {
                try {
                    const response = await fetch(`/api/delete_record/${recordId}`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        // Remove the row from the table
                        const row = this.closest('tr');
                        row.remove();
                        
                        // Show a success message
                        alert('Record deleted successfully');
                    } else {
                        alert('Error deleting record: ' + (result.error || 'Unknown error'));
                    }
                } catch (error) {
                    console.error('Error deleting record:', error);
                    alert('Error deleting record');
                }
            }
        });
    });
    
    // Handle form submission for editing
    editForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const recordId = document.getElementById('edit-record-id').value;
        const formData = {
            item_type: document.getElementById('edit-item-type').value,
            quantity: parseInt(document.getElementById('edit-quantity').value),
            location: document.getElementById('edit-location').value,
            collection_date: document.getElementById('edit-date').value,
            status: document.getElementById('edit-status').value
        };
        
        try {
            const response = await fetch(`/api/update_record/${recordId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Close modal
                modal.style.display = 'none';
                
                // Show success message
                alert('Record updated successfully');
                
                // Reload the page to reflect changes
                location.reload();
            } else {
                alert('Error updating record: ' + (result.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error updating record:', error);
            alert('Error updating record');
        }
    });
});