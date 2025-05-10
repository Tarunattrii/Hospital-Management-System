// Admit.js - JavaScript for the Bed Vacancy page

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

    // Get filter elements
    const wardFilter = document.getElementById('wardFilter');
    const statusFilter = document.getElementById('statusFilter');
    const bedTypeFilter = document.getElementById('bedTypeFilter');
    
    // Add event listeners to filters
    wardFilter.addEventListener('change', applyFilters);
    statusFilter.addEventListener('change', applyFilters);
    bedTypeFilter.addEventListener('change', applyFilters);
    
    // Initialize detail buttons
    initializeDetailButtons();
    
    /**
     * Apply filters to bed list
     */
    function applyFilters() {
        const wardValue = wardFilter.value;
        const statusValue = statusFilter.value;
        const bedTypeValue = bedTypeFilter.value;
        
        console.log('Filtering by:', { ward: wardValue, status: statusValue, bedType: bedTypeValue });
        
        // Filter ward sections
        const wardSections = document.querySelectorAll('.ward-section');
        wardSections.forEach(section => {
            const wardType = section.getAttribute('data-ward');
            
            if (wardValue === 'all' || wardType === wardValue) {
                section.style.display = 'block';
            } else {
                section.style.display = 'none';
                return; // Skip processing beds in hidden wards
            }
            
            // Filter individual beds within visible ward sections
            const bedRows = section.querySelectorAll('.bed-row');
            let visibleBeds = 0;
            
            bedRows.forEach(row => {
                const rowStatus = row.getAttribute('data-status');
                const rowType = row.getAttribute('data-type');
                
                const statusMatches = statusValue === 'all' || rowStatus === statusValue;
                const typeMatches = bedTypeValue === 'all' || rowType === bedTypeValue;
                
                if (statusMatches && typeMatches) {
                    row.style.display = 'table-row';
                    visibleBeds++;
                } else {
                    row.style.display = 'none';
                }
            });
            
            // If no beds are visible in this section after filtering, hide the section
            if (visibleBeds === 0) {
                section.style.display = 'none';
            } else {
                // Update the count of visible beds in the header
                const badgeElement = section.querySelector('.badge');
                if (badgeElement) {
                    // Only count available beds that are visible
                    const visibleAvailableBeds = Array.from(bedRows)
                        .filter(row => row.style.display !== 'none' && row.getAttribute('data-status') === 'available')
                        .length;
                    
                    badgeElement.textContent = `${visibleAvailableBeds} Available`;
                    
                    // Update badge color based on availability
                    badgeElement.className = 'badge px-3 py-2';
                    if (visibleAvailableBeds > 0) {
                        badgeElement.classList.add('bg-success');
                    } else {
                        badgeElement.classList.add('bg-danger');
                    }
                }
            }
        });
        
        // Update summary cards based on filtered data
        updateSummaryCards();
    }
    
    /**
     * Update summary statistics based on filtered beds
     */
    function updateSummaryCards() {
        // Only count beds that are currently visible (after filtering)
        const visibleBedRows = Array.from(document.querySelectorAll('.bed-row')).filter(row => row.style.display !== 'none');
        
        const totalBeds = visibleBedRows.length;
        const occupiedBeds = visibleBedRows.filter(row => row.getAttribute('data-status') === 'occupied').length;
        const vacantBeds = totalBeds - occupiedBeds;
        const occupancyRate = totalBeds > 0 ? Math.round((occupiedBeds / totalBeds) * 100) : 0;
        
        // Update the summary cards
        const summaryCards = document.querySelectorAll('.card .display-4');
        if (summaryCards.length >= 4) {
            summaryCards[0].textContent = vacantBeds;
            summaryCards[1].textContent = occupiedBeds;
            summaryCards[2].textContent = totalBeds;
            summaryCards[3].textContent = `${occupancyRate}%`;
        }
    }
    
    /**
     * Initialize bed detail buttons
     */
    function initializeDetailButtons() {
        const detailButtons = document.querySelectorAll('.btn-outline-info');
        
        detailButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.stopPropagation(); // Prevent row click event from firing
                
                // Get bed information from the row
                const row = this.closest('tr');
                const bedNumber = row.cells[0].textContent.trim();
                const bedType = row.cells[1].textContent.trim();
                const status = row.cells[2].textContent.trim();
                const location = row.cells[3].textContent.trim();
                
                // Determine bed type-specific features
                let typeFeaturesHTML = '';
                
                if (bedType.toLowerCase() === 'standard') {
                    typeFeaturesHTML = `
                        <li>Manual adjustable height</li>
                        <li>Standard side rails</li>
                        <li>Nurse call button</li>
                        <li>Basic IV pole</li>
                    `;
                } else if (bedType.toLowerCase() === 'electric') {
                    typeFeaturesHTML = `
                        <li>Electric adjustable height, back, and leg positions</li>
                        <li>Enhanced side rails with controls</li>
                        <li>Advanced nurse call system</li>
                        <li>Integrated IV pole</li>
                        <li>Pressure relief mattress</li>
                    `;
                } else if (bedType.toLowerCase() === 'bariatric') {
                    typeFeaturesHTML = `
                        <li>Reinforced frame with higher weight capacity</li>
                        <li>Extra width for patient comfort</li>
                        <li>Electric adjustable height and positions</li>
                        <li>Special pressure-reducing mattress</li>
                        <li>Enhanced side rails</li>
                    `;
                } else if (bedType.toLowerCase() === 'pediatric') {
                    typeFeaturesHTML = `
                        <li>Child-appropriate size and height</li>
                        <li>Colorful, kid-friendly design</li>
                        <li>Extra-safe high side rails</li>
                        <li>Space for parent/guardian</li>
                        <li>Entertainment options</li>
                    `;
                } else {
                    // Generic features
                    typeFeaturesHTML = `
                        <li>Adjustable height</li>
                        <li>Side rails</li>
                        <li>IV pole</li>
                        <li>Nurse call button</li>
                    `;
                }
                
                // Create modal with bed details (using Bootstrap modal)
                const modalHTML = `
                <div class="modal fade" id="bedDetailModal" tabindex="-1" aria-labelledby="bedDetailModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="bedDetailModalLabel">Bed Details: ${bedNumber}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <div class="mb-3">
                                    <strong>Bed Number:</strong> ${bedNumber}
                                </div>
                                <div class="mb-3">
                                    <strong>Bed Type:</strong> ${bedType}
                                </div>
                                <div class="mb-3">
                                    <strong>Status:</strong> ${status}
                                </div>
                                <div class="mb-3">
                                    <strong>Location:</strong> ${location}
                                </div>
                                <div class="mb-3">
                                    <strong>Features:</strong>
                                    <ul>
                                        ${typeFeaturesHTML}
                                    </ul>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                ${status.includes('Available') ? 
                                    '<button type="button" class="btn btn-primary">Reserve Bed</button>' : 
                                    ''}
                            </div>
                        </div>
                    </div>
                </div>
                `;
                
                // Remove any existing modals
                const existingModal = document.getElementById('bedDetailModal');
                if (existingModal) {
                    existingModal.remove();
                }
                
                // Add the modal to the DOM
                document.body.insertAdjacentHTML('beforeend', modalHTML);
                
                // Initialize and show the modal
                const modal = new bootstrap.Modal(document.getElementById('bedDetailModal'));
                modal.show();
            });
        });
    }
});
