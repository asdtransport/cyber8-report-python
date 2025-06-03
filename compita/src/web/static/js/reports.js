/**
 * Reports Module
 * Handles the functionality for viewing and downloading available reports
 */

function initReportsList() {
    // DOM Elements
    const loadReportsBtn = document.getElementById('load-reports');
    const reportDateInput = document.getElementById('report-date');
    const reportsContainer = document.getElementById('reports-list');
    const tabButtons = document.querySelectorAll('.tab-btn:not(.main-tab):not(.report-type-tab)');
    const tabContents = document.querySelectorAll('.tab-content:not(.main-tab-content):not(.report-tab-content)');
    
    // Event Listeners
    if (loadReportsBtn) {
        loadReportsBtn.addEventListener('click', loadReports);
    }
    
    // Tab switching
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.getAttribute('data-tab');
            
            // Update active tab button
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Show active tab content
            tabContents.forEach(content => content.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Functions
    async function loadReports() {
        const date = reportDateInput.value.trim();
        
        if (!date || !isValidDate(date)) {
            alert('Please enter a valid date in YY-MM-DD format');
            return;
        }
        
        try {
            // Clear previous reports
            document.querySelector('#student-reports .report-list').innerHTML = '';
            document.querySelector('#class-reports .report-list').innerHTML = '';
            document.querySelector('#flexible-reports .report-list').innerHTML = '';
            
            // Show loading message
            document.querySelector('#student-reports .report-list').innerHTML = '<p>Loading reports...</p>';
            document.querySelector('#class-reports .report-list').innerHTML = '<p>Loading reports...</p>';
            document.querySelector('#flexible-reports .report-list').innerHTML = '<p>Loading reports...</p>';
            
            reportsContainer.classList.remove('hidden');
            
            // Fetch available reports from the API
            const response = await fetch(`${API_URL}/api/v1/available-reports/${date}`);
            
            if (!response.ok) {
                throw new Error(`Failed to fetch reports: ${response.status} ${response.statusText}`);
            }
            
            const data = await response.json();
            
            // Categorize reports
            const studentReports = data.reports.filter(report => 
                report.filename.toLowerCase().includes('student') ||
                report.path.toLowerCase().includes('student')
            );
            
            const classReports = data.reports.filter(report => 
                report.filename.toLowerCase().includes('class') ||
                report.path.toLowerCase().includes('class')
            );
            
            const flexibleReports = data.reports.filter(report => 
                report.filename.toLowerCase().includes('module') ||
                report.filename.toLowerCase().includes('assessment') ||
                report.filename.toLowerCase().includes('grade') ||
                report.path.toLowerCase().includes('flexible')
            );
            
            // Render reports
            renderReports('#student-reports .report-list', studentReports, date);
            renderReports('#class-reports .report-list', classReports, date);
            renderReports('#flexible-reports .report-list', flexibleReports, date);
        } catch (error) {
            console.error('Error loading reports:', error);
            alert('Failed to load reports. Please check if the server is running.');
        }
    }
    
    function renderReports(selector, reports, date) {
        const container = document.querySelector(selector);
        container.innerHTML = '';
        
        if (reports.length === 0) {
            container.innerHTML = '<p>No reports found for this date.</p>';
            return;
        }
        
        reports.forEach(report => {
            const reportItem = document.createElement('div');
            reportItem.className = 'report-item';
            
            // Extract a display name from the filename
            let displayName = report.filename;
            // Remove extension
            displayName = displayName.replace(/\.[^/.]+$/, '');
            // Replace underscores with spaces
            displayName = displayName.replace(/_/g, ' ');
            // Title case
            displayName = displayName.split(' ')
                .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                .join(' ');
            
            const title = document.createElement('h4');
            title.textContent = displayName;
            
            const type = document.createElement('p');
            type.textContent = `Type: ${report.type.toUpperCase()}`;
            
            const size = document.createElement('p');
            size.textContent = `Size: ${formatFileSize(report.size)}`;
            
            const downloadBtn = document.createElement('button');
            downloadBtn.className = 'btn primary';
            downloadBtn.textContent = 'Download';
            downloadBtn.addEventListener('click', () => {
                // Create download URL
                const downloadUrl = `${API_URL}/api/v1/download-report/${date}/${report.report_type}/${report.filename}`;
                window.open(downloadUrl, '_blank');
            });
            
            reportItem.appendChild(title);
            reportItem.appendChild(type);
            reportItem.appendChild(size);
            reportItem.appendChild(downloadBtn);
            
            container.appendChild(reportItem);
        });
    }
}
