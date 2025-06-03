/**
 * Setup Project Module
 * Handles the functionality for setting up new projects
 */

function initSetupProject() {
    // DOM Elements
    const setupDateInput = document.getElementById('setup-date');
    const classNameInput = document.getElementById('class-name');
    const currentModuleInput = document.getElementById('current-module');
    const setupGradebookCheck = document.getElementById('setup-gradebook');
    const setupStudyhistoryCheck = document.getElementById('setup-studyhistory');
    const setupTimeperresourceCheck = document.getElementById('setup-timeperresource');
    const createProjectBtn = document.getElementById('create-project');
    const validateProjectBtn = document.getElementById('validate-project');
    const setupStatusContainer = document.getElementById('setup-status');
    const setupStatusText = document.getElementById('setup-status-text');
    const setupMessage = document.getElementById('setup-message');
    const projectStructureContainer = document.getElementById('project-structure');
    const structureTree = document.getElementById('structure-tree');
    
    // Event Listeners
    if (createProjectBtn) {
        createProjectBtn.addEventListener('click', createProject);
    }
    
    if (validateProjectBtn) {
        validateProjectBtn.addEventListener('click', validateProject);
    }
    
    // Functions
    async function createProject() {
        const date = setupDateInput.value.trim();
        const className = classNameInput.value.trim();
        const currentModule = currentModuleInput.value.trim();
        
        if (!date || !isValidDate(date)) {
            showError('Please enter a valid date in YY-MM-DD format');
            setupDateInput.focus();
            return;
        }
        
        // Class name is now optional
        
        if (!currentModule || isNaN(parseInt(currentModule))) {
            showError('Please enter a valid current module number');
            currentModuleInput.focus();
            return;
        }
        
        // Get required files
        const requiredFiles = [];
        if (setupGradebookCheck.checked) requiredFiles.push('classgradebook');
        if (setupStudyhistoryCheck.checked) requiredFiles.push('studyhistory');
        if (setupTimeperresourceCheck.checked) requiredFiles.push('timeperresource');
        
        if (requiredFiles.length === 0) {
            showError('Please select at least one required file type');
            setupGradebookCheck.focus();
            return;
        }
        
        try {
            // Show loading spinner and status
            showStatus('running', 'Creating project structure...');
            setupStatusContainer.classList.remove('hidden');
            projectStructureContainer.classList.add('hidden');
            
            // Disable buttons while processing
            createProjectBtn.disabled = true;
            validateProjectBtn.disabled = true;
            
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
                showStatus('completed', data.message || 'Project structure created successfully');
                
                // Display project structure
                structureTree.textContent = data.structure || '';
                projectStructureContainer.classList.remove('hidden');
                
                // Start polling for status updates if there's a task ID
                if (data.task_id) {
                    pollSetupStatus(data.task_id);
                }
            } else {
                showStatus('failed', data.detail || 'Failed to create project structure');
            }
            
            // Re-enable buttons
            createProjectBtn.disabled = false;
            validateProjectBtn.disabled = false;
        } catch (error) {
            console.error('Error creating project:', error);
            showStatus('failed', 'Failed to connect to the API. Please check if the server is running.');
            
            // Re-enable buttons
            createProjectBtn.disabled = false;
            validateProjectBtn.disabled = false;
        }
    }
    
    async function validateProject() {
        const date = setupDateInput.value.trim();
        
        if (!date || !isValidDate(date)) {
            showError('Please enter a valid date in YY-MM-DD format');
            setupDateInput.focus();
            return;
        }
        
        try {
            // Show loading spinner and status
            showStatus('running', 'Validating project structure...');
            setupStatusContainer.classList.remove('hidden');
            projectStructureContainer.classList.add('hidden');
            
            // Disable buttons while processing
            createProjectBtn.disabled = true;
            validateProjectBtn.disabled = true;
            
            const response = await fetch(`${API_URL}/api/v1/validate-project/${date}`);
            const data = await response.json();
            
            if (response.ok) {
                // Show appropriate status based on validation result
                const statusType = data.status === 'complete' ? 'completed' : 'running';
                showStatus(statusType, data.message);
                
                // Display project structure
                structureTree.textContent = data.structure || '';
                projectStructureContainer.classList.remove('hidden');
            } else {
                showStatus('failed', data.detail || 'Failed to validate project');
            }
            
            // Re-enable buttons
            createProjectBtn.disabled = false;
            validateProjectBtn.disabled = false;
        } catch (error) {
            console.error('Error validating project:', error);
            showStatus('failed', 'Failed to connect to the API. Please check if the server is running.');
            
            // Re-enable buttons
            createProjectBtn.disabled = false;
            validateProjectBtn.disabled = false;
        }
    }
    
    function pollSetupStatus(taskId) {
        const interval = setInterval(async () => {
            try {
                const response = await fetch(`${API_URL}/api/v1/status/${taskId}`);
                const data = await response.json();
                
                if (response.ok) {
                    showStatus(data.status, data.message);
                    
                    if (data.status === 'completed') {
                        // Update structure tree if available
                        if (data.result && data.result.structure) {
                            structureTree.textContent = data.result.structure;
                            projectStructureContainer.classList.remove('hidden');
                        }
                        clearInterval(interval);
                        
                        // Re-enable buttons
                        createProjectBtn.disabled = false;
                        validateProjectBtn.disabled = false;
                    } else if (data.status === 'failed') {
                        clearInterval(interval);
                        
                        // Re-enable buttons
                        createProjectBtn.disabled = false;
                        validateProjectBtn.disabled = false;
                    }
                } else {
                    showStatus('failed', data.detail || 'Failed to check task status');
                    clearInterval(interval);
                    
                    // Re-enable buttons
                    createProjectBtn.disabled = false;
                    validateProjectBtn.disabled = false;
                }
            } catch (error) {
                console.error('Error checking setup status:', error);
                showStatus('failed', 'Failed to connect to the API');
                clearInterval(interval);
                
                // Re-enable buttons
                createProjectBtn.disabled = false;
                validateProjectBtn.disabled = false;
            }
        }, 2000);
    }
    
    // Helper functions for showing status and errors
    function showStatus(status, message) {
        // Clear previous status
        setupStatusText.innerHTML = '';
        setupMessage.textContent = message;
        
        // Create status indicator with appropriate class
        const statusIndicator = document.createElement('div');
        statusIndicator.className = `status-indicator ${status}`;
        
        if (status === 'running') {
            // Add spinner for running status
            const spinner = document.createElement('div');
            spinner.className = 'spinner';
            statusIndicator.appendChild(spinner);
            statusIndicator.appendChild(document.createTextNode('Running'));
        } else if (status === 'completed') {
            statusIndicator.textContent = 'Completed';
        } else if (status === 'failed') {
            statusIndicator.textContent = 'Failed';
        } else {
            statusIndicator.textContent = status.charAt(0).toUpperCase() + status.slice(1);
        }
        
        setupStatusText.appendChild(statusIndicator);
    }
    
    function showError(message) {
        // Show error message in a more user-friendly way
        setupStatusContainer.classList.remove('hidden');
        showStatus('failed', message);
        
        // Automatically hide the error after 5 seconds
        setTimeout(() => {
            if (setupStatusText.querySelector('.status-indicator.failed') && 
                setupMessage.textContent === message) {
                setupStatusContainer.classList.add('hidden');
            }
        }, 5000);
    }
}
