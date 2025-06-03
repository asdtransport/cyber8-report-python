/**
 * Upload CSV Module
 * Handles the functionality for uploading and parsing CSV files
 */

function initUploadCSV() {
    // DOM Elements
    const uploadCSVBtn = document.getElementById('upload-csv');
    const uploadDateInput = document.getElementById('upload-date');
    const fileTypeSelect = document.getElementById('file-type');
    const parserTypeSelect = document.getElementById('parser-type');
    const csvFileInput = document.getElementById('csv-file');
    const uploadStatusContainer = document.getElementById('upload-status');
    const uploadStatusText = document.getElementById('upload-status-text');
    const uploadMessage = document.getElementById('upload-message');
    
    // Event Listeners
    if (uploadCSVBtn) {
        uploadCSVBtn.addEventListener('click', uploadCSV);
    }
    
    // Functions
    async function uploadCSV() {
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
    
    function pollUploadStatus(taskId) {
        const interval = setInterval(async () => {
            try {
                const response = await fetch(`${API_URL}/api/v1/status/${taskId}`);
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
}
