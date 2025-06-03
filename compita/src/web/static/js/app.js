/**
 * Cyber8 Report Generator Web Interface
 * Main application entry point
 */

// Global API URL
let API_URL = "http://localhost:8000/api/v1";

// Global variables for DOM elements
let currentTaskId = null;

// Generate Reports elements
let generateAllBtn, checkStatusBtn, dateInput;
let taskStatusContainer, taskIdElement, statusElement, messageElement, timestampElement;

// Upload elements
let uploadCSVBtn, uploadDateInput, fileTypeSelect, parserTypeSelect, csvFileInput;
let uploadStatusContainer, uploadStatusText, uploadMessage;

// Reports elements
let loadReportsBtn, reportDateInput, reportsContainer;

// Setup Project elements
let setupDateInput, classNameInput, currentModuleInput;
let setupGradebookCheck, setupStudyhistoryCheck, setupTimeperresourceCheck;
let createProjectBtn, validateProjectBtn, setupStatusContainer;
let setupStatusText, setupMessage, projectStructureContainer, structureTree;

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Fetch API URL from server
    fetchApiUrl();
    
    // Initialize DOM elements
    initDOMElements();
    
    // Initialize page-specific functionality based on current page
    initCurrentPage();
    
    // Initialize navigation menu
    initNavigation();
});

/**
 * Initialize DOM element references
 */
function initDOMElements() {
    // Generate Reports elements
    generateAllBtn = document.getElementById('generate-all');
    checkStatusBtn = document.getElementById('check-status');
    dateInput = document.getElementById('date');
    taskStatusContainer = document.getElementById('task-status');
    taskIdElement = document.getElementById('task-id');
    statusElement = document.getElementById('status');
    messageElement = document.getElementById('message');
    timestampElement = document.getElementById('timestamp');
    
    // Upload elements
    uploadCSVBtn = document.getElementById('upload-csv');
    uploadDateInput = document.getElementById('upload-date');
    fileTypeSelect = document.getElementById('file-type');
    parserTypeSelect = document.getElementById('parser-type');
    csvFileInput = document.getElementById('csv-file');
    uploadStatusContainer = document.getElementById('upload-status');
    uploadStatusText = document.getElementById('upload-status-text');
    uploadMessage = document.getElementById('upload-message');
    
    // Reports elements
    loadReportsBtn = document.getElementById('load-reports');
    reportDateInput = document.getElementById('report-date');
    reportsContainer = document.getElementById('reports-list');
    
    // Setup Project elements
    setupDateInput = document.getElementById('setup-date');
    classNameInput = document.getElementById('class-name');
    currentModuleInput = document.getElementById('current-module');
    setupGradebookCheck = document.getElementById('setup-gradebook');
    setupStudyhistoryCheck = document.getElementById('setup-studyhistory');
    setupTimeperresourceCheck = document.getElementById('setup-timeperresource');
    createProjectBtn = document.getElementById('create-project');
    validateProjectBtn = document.getElementById('validate-project');
    setupStatusContainer = document.getElementById('setup-status');
    setupStatusText = document.getElementById('setup-status-text');
    setupMessage = document.getElementById('setup-message');
    projectStructureContainer = document.getElementById('project-structure');
    structureTree = document.getElementById('structure-tree');
    
    // Add event listeners if elements exist
    if (generateAllBtn) generateAllBtn.addEventListener('click', generateAllReports);
    if (checkStatusBtn) checkStatusBtn.addEventListener('click', checkTaskStatus);
    if (uploadCSVBtn) uploadCSVBtn.addEventListener('click', uploadCSV);
    if (loadReportsBtn) loadReportsBtn.addEventListener('click', loadReports);
    if (createProjectBtn) createProjectBtn.addEventListener('click', createProject);
    if (validateProjectBtn) validateProjectBtn.addEventListener('click', validateProject);
}

/**
 * Fetch API URL from server
 */
async function fetchApiUrl() {
    try {
        const response = await fetch('/api_url');
        if (response.ok) {
            const data = await response.json();
            if (data.api_url) {
                API_URL = data.api_url;
                console.log(`API URL set to: ${API_URL}`);
            }
        }
    } catch (error) {
        console.error('Error fetching API URL:', error);
    }
}

/**
 * Initialize the current page based on URL or active navigation item
 */
function initCurrentPage() {
    // Get current page from URL path
    const path = window.location.pathname;
    const page = path.split('/').pop() || 'home';
    
    // Initialize page-specific functionality
    switch (page) {
        case 'home':
        case '':
        case 'index.html':
            // Home page doesn't need specific initialization
            break;
        case 'generate':
        case 'generate.html':
            if (typeof initGenerateReports === 'function') {
                initGenerateReports();
            } else {
                // Fallback initialization if module isn't loaded
                if (generateAllBtn && checkStatusBtn) {
                    console.log('Using fallback initialization for generate page');
                }
            }
            break;
        case 'upload':
        case 'upload.html':
            if (typeof initUploadCSV === 'function') {
                initUploadCSV();
            } else {
                // Fallback initialization if module isn't loaded
                if (uploadCSVBtn) {
                    console.log('Using fallback initialization for upload page');
                }
            }
            break;
        case 'reports':
        case 'reports.html':
            if (typeof initReportsList === 'function') {
                initReportsList();
            } else {
                // Fallback initialization if module isn't loaded
                if (loadReportsBtn) {
                    console.log('Using fallback initialization for reports page');
                }
            }
            break;
        case 'flexible':
        case 'flexible.html':
            if (typeof initFlexibleReports === 'function') {
                initFlexibleReports();
            } else {
                console.log('Using fallback initialization for flexible reports page');
            }
            break;
        case 'setup':
        case 'setup.html':
            if (typeof initSetupProject === 'function') {
                initSetupProject();
            } else {
                // Fallback initialization if module isn't loaded
                if (createProjectBtn && validateProjectBtn) {
                    console.log('Using fallback initialization for setup page');
                }
            }
            break;
        default:
            console.log(`No specific initialization for page: ${page}`);
    }
}

/**
 * Initialize navigation menu
 */
function initNavigation() {
    // Highlight current navigation item
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (currentPath === href || 
            (currentPath === '/' && href === '/') || 
            (currentPath.includes(href) && href !== '/')) {
            link.classList.add('active');
        }
    });
}

/**
 * Validates a date string in YY-MM-DD format
 * @param {string} dateStr - Date string to validate
 * @returns {boolean} - Whether the date is valid
 */
function isValidDate(dateStr) {
    if (!dateStr) return false;
    
    // Check format YY-MM-DD
    const regex = /^\d{2}-\d{2}-\d{2}$/;
    if (!regex.test(dateStr)) return false;
    
    // Parse date parts
    const parts = dateStr.split('-');
    const year = parseInt('20' + parts[0]); // Assuming 20xx
    const month = parseInt(parts[1]) - 1; // Months are 0-indexed
    const day = parseInt(parts[2]);
    
    // Create date object and check if it's valid
    const date = new Date(year, month, day);
    return date.getFullYear() === year &&
           date.getMonth() === month &&
           date.getDate() === day;
}

/**
 * Formats a file size in bytes to a human-readable format
 * @param {number} bytes - File size in bytes
 * @returns {string} - Formatted file size
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}
    
/**
 * Poll for task status updates
 * @param {string} taskId - ID of the task to poll for
 */
function startStatusPolling(taskId) {
    // Poll for status updates every 3 seconds
    const pollInterval = setInterval(async () => {
        try {
            const response = await fetch(`${API_URL}/status/${taskId}`);
            const data = await response.json();
            
            if (response.ok) {
                updateTaskStatus(data);
                
                // Stop polling if the task is completed or failed
                if (data.status === 'completed' || data.status === 'failed') {
                    clearInterval(pollInterval);
                }
            } else {
                console.error('Error polling task status:', data);
                clearInterval(pollInterval);
            }
        } catch (error) {
            console.error('Error polling task status:', error);
            clearInterval(pollInterval);
        }
    }, 3000);
}

/**
 * Update the task status display with the provided data
 * @param {Object} data - Task status data from the API
 */
function updateTaskStatus(data) {
    if (!taskIdElement || !statusElement || !messageElement || !timestampElement) {
        console.error('Task status elements not found in the DOM');
        return;
    }
    
    taskIdElement.textContent = data.task_id || currentTaskId;
    statusElement.textContent = data.status || 'Unknown';
    messageElement.textContent = data.message || 'No message';
    timestampElement.textContent = data.timestamp || new Date().toISOString();
    
    // Add status indicator class
    statusElement.className = '';
    statusElement.classList.add('status-indicator', `status-${data.status}`);
}

/**
 * Generate all reports for the specified date
 */
async function generateAllReports() {
    if (!dateInput || !taskStatusContainer) {
        console.error('Generate reports elements not found in the DOM');
        return;
    }
    
    const date = dateInput.value.trim();
    
    if (!date || !isValidDate(date)) {
        alert('Please enter a valid date in YY-MM-DD format');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/api/v1/generate-all`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ date })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentTaskId = data.task_id;
            updateTaskStatus(data);
            taskStatusContainer.classList.remove('hidden');
            
            // Start polling for status updates
            startStatusPolling(data.task_id);
        } else {
            alert(`Error: ${data.detail || 'Failed to start report generation'}`);
        }
    } catch (error) {
        console.error('Error generating reports:', error);
        alert('Failed to connect to the API. Please check if the server is running.');
    }
}

/**
 * Check the status of the current task
 */
async function checkTaskStatus() {
    if (!currentTaskId) {
        alert('No active task. Please generate reports first.');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/api/v1/status/${currentTaskId}`);
        const data = await response.json();
        
        if (response.ok) {
            updateTaskStatus(data);
            if (taskStatusContainer) {
                taskStatusContainer.classList.remove('hidden');
            }
        } else {
            alert(`Error: ${data.detail || 'Failed to check task status'}`);
        }
    } catch (error) {
        console.error('Error checking task status:', error);
        alert('Failed to connect to the API. Please check if the server is running.');
    }
}

/**
 * Upload and parse a CSV file
 */
async function uploadCSV() {
    if (!uploadDateInput || !fileTypeSelect || !parserTypeSelect || !csvFileInput || !uploadStatusContainer || !uploadStatusText || !uploadMessage) {
        console.error('Upload CSV elements not found in the DOM');
        return;
    }
    
    const date = uploadDateInput.value.trim();
    const fileType = fileTypeSelect.value;
    const parserType = parserTypeSelect.value;
    const file = csvFileInput.files[0];
    
    if (!date || !isValidDate(date)) {
        alert('Please enter a valid date in YY-MM-DD format');
        return;
    }
    
    if (!file) {
        alert('Please select a CSV file to upload');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('date', date);
    formData.append('file_type', fileType);
    formData.append('parser_type', parserType);
    
    try {
        uploadStatusText.textContent = 'Uploading...';
        uploadMessage.textContent = 'Uploading and parsing CSV file...';
        uploadStatusContainer.classList.remove('hidden');
        
        const response = await fetch(`${API_URL}/api/v1/upload-csv`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            uploadStatusText.textContent = 'Success';
            uploadMessage.textContent = `File uploaded successfully. Task ID: ${data.task_id}`;
            
            // Start polling for status updates
            pollUploadStatus(data.task_id);
        } else {
            uploadStatusText.textContent = 'Error';
            uploadMessage.textContent = data.detail || 'Failed to upload CSV file';
        }
    } catch (error) {
        console.error('Error uploading CSV:', error);
        uploadStatusText.textContent = 'Error';
        uploadMessage.textContent = 'Failed to connect to the API. Please check if the server is running.';
    }
}

/**
 * Load available reports for the specified date
 */
async function loadReports() {
    if (!reportDateInput || !reportsContainer) {
        console.error('Reports elements not found in the DOM');
        return;
    }
    
    const date = reportDateInput.value.trim();
    
    if (!date || !isValidDate(date)) {
        alert('Please enter a valid date in YY-MM-DD format');
        return;
    }
    
    try {
        // Clear previous reports
        const studentReportsEl = document.querySelector('#student-reports .report-list');
        const classReportsEl = document.querySelector('#class-reports .report-list');
        const flexibleReportsEl = document.querySelector('#flexible-reports .report-list');
        
        if (studentReportsEl) studentReportsEl.innerHTML = '<p>Loading reports...</p>';
        if (classReportsEl) classReportsEl.innerHTML = '<p>Loading reports...</p>';
        if (flexibleReportsEl) flexibleReportsEl.innerHTML = '<p>Loading reports...</p>';
        
        if (reportsContainer) reportsContainer.classList.remove('hidden');
        
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
        if (studentReportsEl) renderReports('#student-reports .report-list', studentReports, date);
        if (classReportsEl) renderReports('#class-reports .report-list', classReports, date);
        if (flexibleReportsEl) renderReports('#flexible-reports .report-list', flexibleReports, date);
    } catch (error) {
        console.error('Error loading reports:', error);
        alert('Failed to load reports. Please check if the server is running.');
    }
}
    
/**
 * Poll for upload task status updates
 * @param {string} taskId - ID of the upload task to poll for
 */
function pollUploadStatus(taskId) {
    const interval = setInterval(async () => {
        try {
            const response = await fetch(`${API_URL}/status/${taskId}`);
            const data = await response.json();
            
            if (response.ok) {
                uploadStatusText.textContent = data.status;
                uploadMessage.textContent = data.message;
                
                if (data.status === 'completed' || data.status === 'failed') {
                    clearInterval(interval);
                }
            } else {
                uploadStatusText.textContent = 'Error';
                uploadMessage.textContent = data.detail || 'Failed to check task status';
                clearInterval(interval);
            }
        } catch (error) {
            console.error('Error checking upload status:', error);
            uploadStatusText.textContent = 'Error';
            uploadMessage.textContent = 'Failed to connect to the API';
            clearInterval(interval);
        }
    }, 2000);
}
    
/**
 * Create a new project with the specified parameters
 */
async function createProject() {
    const date = setupDateInput.value.trim();
    const className = classNameInput.value.trim();
    const currentModule = currentModuleInput.value.trim();
    
    if (!date || !isValidDate(date)) {
        alert('Please enter a valid date in YY-MM-DD format');
        return;
    }
    
    if (!className) {
        alert('Please enter a class name');
        return;
    }
    
    if (!currentModule || isNaN(parseInt(currentModule))) {
        alert('Please enter a valid current module number');
        return;
    }
    
    // Get required files
    const requiredFiles = [];
    if (setupGradebookCheck.checked) requiredFiles.push('classgradebook');
    if (setupStudyhistoryCheck.checked) requiredFiles.push('studyhistory');
    if (setupTimeperresourceCheck.checked) requiredFiles.push('timeperresource');
    
    if (requiredFiles.length === 0) {
        alert('Please select at least one required file type');
        return;
    }
    
    try {
        setupStatusText.textContent = 'Creating...';
        setupMessage.textContent = 'Creating project structure...';
        setupStatusContainer.classList.remove('hidden');
        projectStructureContainer.classList.add('hidden');
        
        const response = await fetch(`${API_URL}/api/v1/setup-project`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                date,
                class_name: className,
                current_module: parseInt(currentModule),
                required_files: requiredFiles
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            setupStatusText.textContent = 'Success';
            setupMessage.textContent = data.message || 'Project structure created successfully';
            
            // Display project structure
            structureTree.textContent = data.structure || '';
            projectStructureContainer.classList.remove('hidden');
            
            // Start polling for status updates if there's a task ID
            if (data.task_id) {
                pollSetupStatus(data.task_id);
            }
        } else {
            setupStatusText.textContent = 'Error';
            setupMessage.textContent = data.detail || 'Failed to create project structure';
        }
    } catch (error) {
        console.error('Error creating project:', error);
        setupStatusText.textContent = 'Error';
        setupMessage.textContent = 'Failed to connect to the API. Please check if the server is running.';
    }
}
    
/**
 * Validate an existing project structure
 */
async function validateProject() {
    const date = setupDateInput.value.trim();
    
    if (!date || !isValidDate(date)) {
        alert('Please enter a valid date in YY-MM-DD format');
        return;
    }
    
    try {
        setupStatusText.textContent = 'Validating...';
        setupMessage.textContent = 'Validating project structure...';
        setupStatusContainer.classList.remove('hidden');
        projectStructureContainer.classList.add('hidden');
        
        const response = await fetch(`${API_URL}/api/v1/validate-project/${date}`);
        const data = await response.json();
        
        if (response.ok) {
            setupStatusText.textContent = data.status;
            setupMessage.textContent = data.message;
            
            // Display project structure
            structureTree.textContent = data.structure || '';
            projectStructureContainer.classList.remove('hidden');
        } else {
            setupStatusText.textContent = 'Error';
            setupMessage.textContent = data.detail || 'Failed to validate project';
        }
    } catch (error) {
        console.error('Error validating project:', error);
        setupStatusText.textContent = 'Error';
        setupMessage.textContent = 'Failed to connect to the API. Please check if the server is running.';
    }
}
    
/**
 * Poll for setup task status updates
 * @param {string} taskId - ID of the setup task to poll for
 */
function pollSetupStatus(taskId) {
    const interval = setInterval(async () => {
        try {
            const response = await fetch(`${API_URL}/status/${taskId}`);
            const data = await response.json();
            
            if (response.ok) {
                setupStatusText.textContent = data.status;
                setupMessage.textContent = data.message;
                
                if (data.status === 'completed') {
                    // Update structure tree if available
                    if (data.result && data.result.structure) {
                        structureTree.textContent = data.result.structure;
                        projectStructureContainer.classList.remove('hidden');
                    }
                    clearInterval(interval);
                } else if (data.status === 'failed') {
                    clearInterval(interval);
                }
            } else {
                setupStatusText.textContent = 'Error';
                setupMessage.textContent = data.detail || 'Failed to check task status';
                clearInterval(interval);
            }
        } catch (error) {
            console.error('Error checking setup status:', error);
            setupStatusText.textContent = 'Error';
            setupMessage.textContent = 'Failed to connect to the API';
            clearInterval(interval);
        }
    }, 2000);
}

/**
 * Render a list of reports in the specified container
 * @param {string} selector - CSS selector for the container
 * @param {Array} reports - Array of report objects
 * @param {string} date - Date string in YY-MM-DD format
 */
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
        type.textContent = `Type: ${report.type ? report.type.toUpperCase() : 'UNKNOWN'}`;
        
        const size = document.createElement('p');
        size.textContent = `Size: ${formatFileSize(report.size || 0)}`;
        
        const downloadBtn = document.createElement('button');
        downloadBtn.className = 'btn primary';
        downloadBtn.textContent = 'Download';
        downloadBtn.addEventListener('click', () => {
            // Create download URL
            const downloadUrl = `${API_URL}/download-report/${date}/${report.report_type || 'unknown'}/${report.filename}`;
            window.open(downloadUrl, '_blank');
        });
        
        // Append elements to report item
        reportItem.appendChild(title);
        reportItem.appendChild(type);
        reportItem.appendChild(size);
        reportItem.appendChild(downloadBtn);
        
        // Append report item to container
        container.appendChild(reportItem);
    });
}
