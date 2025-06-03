/**
 * Generate Reports Module
 * Handles the functionality for generating all reports
 */

function initGenerateReports() {
    // DOM Elements
    const generateAllBtn = document.getElementById('generate-all');
    const checkStatusBtn = document.getElementById('check-status');
    const dateInput = document.getElementById('date');
    const taskStatusContainer = document.getElementById('task-status');
    const taskIdElement = document.getElementById('task-id');
    const statusElement = document.getElementById('status');
    const messageElement = document.getElementById('message');
    const timestampElement = document.getElementById('timestamp');
    
    // Current task ID
    let currentTaskId = null;
    
    // Event Listeners
    if (generateAllBtn) {
        generateAllBtn.addEventListener('click', generateAllReports);
    }
    
    if (checkStatusBtn) {
        checkStatusBtn.addEventListener('click', checkTaskStatus);
    }
    
    // Functions
    async function generateAllReports() {
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
                taskStatusContainer.classList.remove('hidden');
            } else {
                alert(`Error: ${data.detail || 'Failed to check task status'}`);
            }
        } catch (error) {
            console.error('Error checking task status:', error);
            alert('Failed to connect to the API. Please check if the server is running.');
        }
    }
    
    function updateTaskStatus(data) {
        taskIdElement.textContent = data.task_id || currentTaskId;
        statusElement.textContent = data.status || 'Unknown';
        messageElement.textContent = data.message || '';
        timestampElement.textContent = data.timestamp || new Date().toISOString();
        
        // Update status color
        statusElement.className = '';
        if (data.status === 'completed') {
            statusElement.classList.add('success');
        } else if (data.status === 'failed') {
            statusElement.classList.add('error');
        } else if (data.status === 'running') {
            statusElement.classList.add('warning');
        }
    }
    
    function startStatusPolling(taskId) {
        const interval = setInterval(async () => {
            try {
                const response = await fetch(`${API_URL}/api/v1/status/${taskId}`);
                const data = await response.json();
                
                if (response.ok) {
                    updateTaskStatus(data);
                    
                    if (data.status === 'completed' || data.status === 'failed') {
                        clearInterval(interval);
                    }
                } else {
                    console.error('Error polling task status:', data);
                    clearInterval(interval);
                }
            } catch (error) {
                console.error('Error polling task status:', error);
                clearInterval(interval);
            }
        }, 2000);
    }
}
