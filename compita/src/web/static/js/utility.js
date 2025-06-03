/**
 * Utility Module
 * Contains common utility functions used across all modules
 */

// Global API URL
let API_URL = "http://localhost:8000";

// Fetch API URL from server
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

// Initialize API URL
fetchApiUrl();

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
 * Initializes tab switching functionality
 * @param {string} tabBtnSelector - Selector for tab buttons
 * @param {string} tabContentSelector - Selector for tab content
 * @param {string} dataAttribute - Data attribute to match tab content
 */
function initTabSwitching(tabBtnSelector, tabContentSelector, dataAttribute) {
    const tabButtons = document.querySelectorAll(tabBtnSelector);
    const tabContents = document.querySelectorAll(tabContentSelector);
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.getAttribute(dataAttribute);
            
            // Update active tab button
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Show active tab content
            tabContents.forEach(content => content.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
        });
    });
}
