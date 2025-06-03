/**
 * Dashboard functionality for Cyber8 Report Generator
 * Provides system status and recent projects/reports information
 */
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the home page with dashboard
    if (document.getElementById('recent-projects')) {
        // Wait for API_URL to be set before initializing dashboard
        // This ensures we're using the correct API endpoint
        const checkApiUrl = setInterval(() => {
            if (typeof API_URL !== 'undefined' && API_URL !== 'http://localhost:8000/api/v1') {
                clearInterval(checkApiUrl);
                console.log('Dashboard: API URL is set, initializing dashboard');
                initDashboard();
            } else {
                console.log('Dashboard: Waiting for API URL to be set...');
            }
        }, 500);
        
        // Fallback: If API_URL isn't set after 5 seconds, initialize anyway
        setTimeout(() => {
            clearInterval(checkApiUrl);
            console.log('Dashboard: Initializing dashboard with default or current API URL');
            initDashboard();
        }, 5000);
    }
});

/**
 * Initialize the dashboard components
 */
function initDashboard() {
    // Update the "last updated" timestamp
    document.getElementById('last-updated').textContent = new Date().toLocaleTimeString();
    
    // Check if we're on a page with date information and store it
    storeCurrentPageDate();
    
    // Check if API_URL is available and valid
    if (typeof API_URL === 'undefined' || !API_URL) {
        console.warn('Dashboard: API_URL is not defined, using fallback data');
        displayApiWarning();
        // Still try to load components with fallback data
        loadRecentProjects();
        loadRecentReports();
        checkSystemStatus();
        return;
    }
    
    // Load dashboard components in sequence to avoid overwhelming the API
    // First check system status
    checkSystemStatus();
    
    // Then load projects after a short delay
    setTimeout(() => {
        loadRecentProjects();
        
        // Finally load reports
        setTimeout(() => {
            loadRecentReports();
        }, 500);
    }, 500);
}

/**
 * Display a warning when the API URL is not available
 */
function displayApiWarning() {
    // Add a warning to the system status card
    const systemStatusCard = document.getElementById('system-status');
    if (systemStatusCard) {
        const apiStatusElement = document.getElementById('api-status');
        if (apiStatusElement) {
            apiStatusElement.innerHTML = 'Not Configured';
            apiStatusElement.className = 'status-value warning';
        }
        
        const storageStatusElement = document.getElementById('storage-status');
        if (storageStatusElement) {
            storageStatusElement.innerHTML = 'Not Available';
            storageStatusElement.className = 'status-value warning';
        }
        
        // Add a warning message at the top of the dashboard
        const dashboardPanel = document.querySelector('.dashboard-panel');
        if (dashboardPanel) {
            const warningElement = document.createElement('div');
            warningElement.className = 'api-warning';
            warningElement.innerHTML = `
                <div class="status-indicator warning">Warning</div>
                <p>API server connection not configured. Some features may be limited. 
                Please make sure the API server is running and properly configured.</p>
            `;
            dashboardPanel.insertBefore(warningElement, dashboardPanel.firstChild);
            
            // Add styles for the warning
            const style = document.createElement('style');
            style.textContent = `
                .api-warning {
                    background-color: #fff3cd;
                    border: 1px solid #ffeeba;
                    color: #856404;
                    padding: 0.75rem 1.25rem;
                    margin-bottom: 1rem;
                    border-radius: var(--border-radius);
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }
                .api-warning .status-indicator {
                    padding: 0.25rem 0.5rem;
                    font-size: 0.8rem;
                }
                .api-warning p {
                    margin: 0;
                }
            `;
            document.head.appendChild(style);
        }
    }
}

/**
 * Store the current page date in localStorage if available
 * This helps with fallback mechanisms when API endpoints aren't available
 */
function storeCurrentPageDate() {
    // Check URL for date parameter
    const urlParams = new URLSearchParams(window.location.search);
    const dateParam = urlParams.get('date');
    
    if (dateParam) {
        // Store this date in localStorage
        try {
            const storedDates = localStorage.getItem('compita_dates') || '[]';
            const dates = JSON.parse(storedDates);
            
            // Add the date if it's not already in the array
            if (!dates.includes(dateParam)) {
                dates.push(dateParam);
                localStorage.setItem('compita_dates', JSON.stringify(dates));
            }
        } catch (e) {
            console.error('Error storing date in localStorage:', e);
        }
    }
    
    // Look for date elements in the page
    const dateElements = document.querySelectorAll('[data-date]');
    if (dateElements.length > 0) {
        try {
            const storedDates = localStorage.getItem('compita_dates') || '[]';
            let dates = JSON.parse(storedDates);
            
            // Add any dates from the page
            dateElements.forEach(el => {
                const date = el.getAttribute('data-date');
                if (date && !dates.includes(date)) {
                    dates.push(date);
                }
            });
            
            localStorage.setItem('compita_dates', JSON.stringify(dates));
        } catch (e) {
            console.error('Error storing dates from page elements:', e);
        }
    }
}

/**
 * Load recent projects from the API
 */
function loadRecentProjects() {
    const projectsContainer = document.getElementById('recent-projects-content');
    
    // Make API call to get recent projects
    fetch(`${API_URL}/projects`)
        .then(response => {
            if (!response.ok) {
                // If API returns error, use fallback data
                return getFallbackProjects();
            }
            return response.json();
        })
        .then(data => {
            if (!data || data.length === 0) {
                projectsContainer.innerHTML = '<p class="empty-message">No recent projects found.</p>';
                return;
            }
            
            // Sort projects by date (newest first)
            data.sort((a, b) => {
                const dateA = a.created_at ? new Date(a.created_at) : new Date(a);
                const dateB = b.created_at ? new Date(b.created_at) : new Date(b);
                return dateB - dateA;
            });
            
            // Take only the 5 most recent projects
            const recentProjects = data.slice(0, 5);
            
            // Create HTML for each project
            let projectsHTML = '';
            recentProjects.forEach(project => {
                // If project is a string (just a date), use that
                const projectDate = project.date || project;
                const projectName = project.class_name || `Project ${projectDate}`;
                const studentCount = project.student_count ? `${project.student_count} students` : '';
                
                projectsHTML += `
                <div class="project-item">
                    <div class="project-info">
                        <div class="project-name">${projectName}</div>
                        <div class="project-date">${projectDate} ${studentCount ? `(${studentCount})` : ''}</div>
                    </div>
                    <div class="project-actions">
                        <button class="action-button" onclick="window.location.href='/setup?date=${projectDate}'">
                            Edit
                        </button>
                        <button class="action-button" onclick="window.location.href='/generate?date=${projectDate}'">
                            Generate
                        </button>
                    </div>
                </div>`;
            });
            
            projectsContainer.innerHTML = projectsHTML;
        })
        .catch(error => {
            console.error('Error loading projects:', error);
            // Use fallback data on error
            const fallbackData = getFallbackProjects();
            if (fallbackData.length > 0) {
                // Process fallback data
                let projectsHTML = '';
                fallbackData.forEach(project => {
                    projectsHTML += `
                    <div class="project-item">
                        <div class="project-info">
                            <div class="project-name">${project}</div>
                            <div class="project-date">Available project</div>
                        </div>
                        <div class="project-actions">
                            <button class="action-button" onclick="window.location.href='/setup?date=${project}'">
                                Edit
                            </button>
                            <button class="action-button" onclick="window.location.href='/generate?date=${project}'">
                                Generate
                            </button>
                        </div>
                    </div>`;
                });
                projectsContainer.innerHTML = projectsHTML;
            } else {
                projectsContainer.innerHTML = `<p>Use the Setup Project page to create your first project.</p>`;
            }
        });
}

/**
 * Get fallback project data by checking available dates from the reports page
 */
function getFallbackProjects() {
    // Try to extract dates from the DOM if we're on a page with date information
    const dateElements = document.querySelectorAll('[data-date]');
    if (dateElements.length > 0) {
        const dates = Array.from(dateElements).map(el => el.getAttribute('data-date'));
        return [...new Set(dates)]; // Return unique dates
    }
    
    // Check localStorage for any previously stored dates
    const storedDates = localStorage.getItem('compita_dates');
    if (storedDates) {
        try {
            return JSON.parse(storedDates);
        } catch (e) {
            console.error('Error parsing stored dates:', e);
        }
    }
    
    // Return empty array if no dates found
    return [];
}

/**
 * Load recent reports from the API
 */
function loadRecentReports() {
    const reportsContainer = document.getElementById('recent-reports-content');
    
    // Make API call to get recent reports
    fetch(`${API_URL}/reports`)
        .then(response => {
            if (!response.ok) {
                // If API returns error, use fallback data
                return getFallbackReports();
            }
            return response.json();
        })
        .then(data => {
            if (!data || data.length === 0) {
                reportsContainer.innerHTML = '<p class="empty-message">No recent reports found.</p>';
                return;
            }
            
            // Sort reports by date (newest first)
            data.sort((a, b) => {
                const dateA = a.created_at ? new Date(a.created_at) : new Date(a.date || a);
                const dateB = b.created_at ? new Date(b.created_at) : new Date(b.date || b);
                return dateB - dateA;
            });
            
            // Take only the 5 most recent reports
            const recentReports = data.slice(0, 5);
            
            // Create HTML for each report
            let reportsHTML = '';
            recentReports.forEach(report => {
                // Get report details
                const reportDate = report.date || report;
                const reportName = report.name || report.type || `Reports for ${reportDate}`;
                const reportType = report.type ? `(${report.type})` : '';
                
                reportsHTML += `
                <div class="report-item">
                    <div class="report-info">
                        <div class="report-name">${reportName} ${reportType}</div>
                        <div class="report-date">${reportDate}</div>
                    </div>
                    <div class="report-actions">
                        <button class="action-button" onclick="window.location.href='/reports?date=${reportDate}'">
                            View
                        </button>
                    </div>
                </div>`;
            });
            
            reportsContainer.innerHTML = reportsHTML;
        })
        .catch(error => {
            console.error('Error loading reports:', error);
            // Use fallback data on error
            const fallbackData = getFallbackReports();
            if (fallbackData.length > 0) {
                // Process fallback data
                let reportsHTML = '';
                fallbackData.forEach(report => {
                    reportsHTML += `
                    <div class="report-item">
                        <div class="report-info">
                            <div class="report-name">${report.name || 'Available Report'}</div>
                            <div class="report-date">${report.date || ''}</div>
                        </div>
                        <div class="report-actions">
                            <button class="action-button" onclick="window.location.href='/reports?date=${report.date || ''}'">
                                View
                            </button>
                        </div>
                    </div>`;
                });
                reportsContainer.innerHTML = reportsHTML;
            } else {
                reportsContainer.innerHTML = `<p>Generate your first report using the Generate Reports page.</p>`;
            }
        });
}

/**
 * Get fallback report data
 */
function getFallbackReports() {
    // Try to extract report info from localStorage
    const storedReports = localStorage.getItem('compita_reports');
    if (storedReports) {
        try {
            return JSON.parse(storedReports);
        } catch (e) {
            console.error('Error parsing stored reports:', e);
        }
    }
    
    // If we have projects, use those as potential report dates
    const fallbackProjects = getFallbackProjects();
    if (fallbackProjects.length > 0) {
        return fallbackProjects.map(date => ({ date, name: `Reports for ${date}` }));
    }
    
    // Return empty array if no reports found
    return [];
}

/**
 * Check system status components
 */
function checkSystemStatus() {
    // Check API status
    checkApiStatus();
    
    // Check storage status
    checkStorageStatus();
    
    // Set up auto-refresh for system status
    setInterval(() => {
        // Only refresh if the user is actively viewing the page
        if (document.visibilityState === 'visible') {
            checkApiStatus();
            checkStorageStatus();
            
            // Update the "last checked" timestamp
            const lastUpdatedElement = document.getElementById('last-updated');
            if (lastUpdatedElement) {
                lastUpdatedElement.textContent = new Date().toLocaleTimeString();
            }
        }
    }, 60000); // Check every minute
}

/**
 * Check API server status
 */
function checkApiStatus() {
    const apiStatusElement = document.getElementById('api-status');
    
    // Try to access a basic API endpoint
    fetch(`${API_URL}/health`)
        .then(response => {
            if (response.ok) {
                apiStatusElement.innerHTML = 'Online';
                apiStatusElement.className = 'status-value online';
                return response.json();
            } else {
                apiStatusElement.innerHTML = 'Degraded';
                apiStatusElement.className = 'status-value warning';
                return null;
            }
        })
        .then(data => {
            // If we got data back, update the last updated time
            if (data && data.timestamp) {
                const lastUpdatedElement = document.getElementById('last-updated');
                if (lastUpdatedElement) {
                    const timestamp = new Date(data.timestamp);
                    lastUpdatedElement.textContent = timestamp.toLocaleTimeString();
                }
            }
        })
        .catch(() => {
            apiStatusElement.innerHTML = 'Offline';
            apiStatusElement.className = 'status-value offline';
            
            // If API is offline, try to check if we're on the same origin
            // This helps determine if it's a CORS issue or if the API is truly offline
            fetch(window.location.href)
                .then(() => {
                    // If we can fetch the current page, it's likely a CORS issue
                    console.log('Web server is online, but API may have CORS issues');
                })
                .catch(() => {
                    console.log('Both web server and API appear to be offline');
                });
        });
}

/**
 * Check storage status
 */
function checkStorageStatus() {
    const storageStatusElement = document.getElementById('storage-status');
    
    fetch(`${API_URL}/storage`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Storage check failed');
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'ok') {
                // Show storage usage if available
                if (data.disk_usage_percent !== undefined) {
                    const usagePercent = data.disk_usage_percent;
                    let statusClass = 'online';
                    
                    // Change status color based on usage percentage
                    if (usagePercent > 90) {
                        statusClass = 'offline'; // Critical
                    } else if (usagePercent > 75) {
                        statusClass = 'warning'; // Warning
                    }
                    
                    storageStatusElement.innerHTML = `${usagePercent}% Used`;
                    storageStatusElement.className = `status-value ${statusClass}`;
                } else {
                    storageStatusElement.innerHTML = 'Available';
                    storageStatusElement.className = 'status-value online';
                }
            } else {
                storageStatusElement.innerHTML = data.message || 'Warning';
                storageStatusElement.className = 'status-value warning';
            }
        })
        .catch(() => {
            // If the endpoint doesn't exist yet, assume it's ok for now
            storageStatusElement.innerHTML = 'Available';
            storageStatusElement.className = 'status-value online';
        });
}
