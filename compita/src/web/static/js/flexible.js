/**
 * Flexible Reports Module
 * Handles the functionality for generating flexible reports
 */

function initFlexibleReports() {
    // DOM Elements
    const reportTypeTabs = document.querySelectorAll('.report-type-tab');
    const reportTabContents = document.querySelectorAll('.report-tab-content');
    
    // Module Report Elements
    const moduleDate = document.getElementById('module-date');
    const moduleCurrent = document.getElementById('module-current');
    const moduleSelection = document.getElementById('module-selection');
    const moduleCountPartial = document.getElementById('module-count-partial');
    const moduleOutputPrefix = document.getElementById('module-output-prefix');
    const generateModuleReportBtn = document.getElementById('generate-module-report');
    
    // Assessment Report Elements
    const assessmentDate = document.getElementById('assessment-date');
    const assessmentQuiz = document.getElementById('assessment-quiz');
    const assessmentTest = document.getElementById('assessment-test');
    const assessmentExam = document.getElementById('assessment-exam');
    const assessmentModuleSelection = document.getElementById('assessment-module-selection');
    const assessmentOutputPrefix = document.getElementById('assessment-output-prefix');
    const generateAssessmentReportBtn = document.getElementById('generate-assessment-report');
    
    // Grades Report Elements
    const gradesDate = document.getElementById('grades-date');
    const gradesQuiz = document.getElementById('grades-quiz');
    const gradesTest = document.getElementById('grades-test');
    const gradesExam = document.getElementById('grades-exam');
    const gradesHomework = document.getElementById('grades-homework');
    const gradesParticipation = document.getElementById('grades-participation');
    const weightQuiz = document.getElementById('weight-quiz');
    const weightTest = document.getElementById('weight-test');
    const weightExam = document.getElementById('weight-exam');
    const weightHomework = document.getElementById('weight-homework');
    const weightParticipation = document.getElementById('weight-participation');
    const gradesModuleSelection = document.getElementById('grades-module-selection');
    const gradesOutputPrefix = document.getElementById('grades-output-prefix');
    const generateGradesReportBtn = document.getElementById('generate-grades-report');
    
    // CSV Reports Elements
    const csvDate = document.getElementById('csv-date');
    const csvType = document.getElementById('csv-type');
    const csvModuleNumber = document.getElementById('csv-module-number');
    const csvStudentName = document.getElementById('csv-student-name');
    const generateCSVReportBtn = document.getElementById('generate-csv-report');
    
    // Markdown to PDF Elements
    const pdfDate = document.getElementById('pdf-date');
    const pdfType = document.getElementById('pdf-type');
    const pdfOutputDir = document.getElementById('pdf-output-dir');
    const convertToPDFBtn = document.getElementById('convert-to-pdf');
    
    // Status Elements
    const flexibleStatusContainer = document.getElementById('flexible-status');
    const flexibleTaskId = document.getElementById('flexible-task-id');
    const flexibleStatusText = document.getElementById('flexible-status-text');
    const flexibleMessage = document.getElementById('flexible-message');
    const flexibleTimestamp = document.getElementById('flexible-timestamp');
    
    // Current task ID
    let currentTaskId = null;
    
    // Initialize
    populateModuleSelections();
    
    // Event Listeners
    // Tab switching
    reportTypeTabs.forEach(button => {
        if (button) {
            button.addEventListener('click', () => {
                const tabId = button.getAttribute('data-report-tab');
                
                // Update active tab button
                reportTypeTabs.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                
                // Show active tab content
                reportTabContents.forEach(content => content.classList.remove('active'));
                document.getElementById(tabId).classList.add('active');
            });
        }
    });
    
    // CSV type change
    if (csvType) {
        csvType.addEventListener('change', () => {
            const selectedType = csvType.value;
            const moduleOptions = document.querySelector('.csv-module-options');
            const studentOptions = document.querySelector('.csv-student-options');
            
            if (selectedType === 'module') {
                moduleOptions.classList.add('active');
                studentOptions.classList.remove('active');
            } else if (selectedType === 'student') {
                moduleOptions.classList.remove('active');
                studentOptions.classList.add('active');
            } else {
                moduleOptions.classList.remove('active');
                studentOptions.classList.remove('active');
            }
        });
    }
    
    // Generate buttons
    if (generateModuleReportBtn) {
        generateModuleReportBtn.addEventListener('click', generateModuleReport);
    }
    
    if (generateAssessmentReportBtn) {
        generateAssessmentReportBtn.addEventListener('click', generateAssessmentReport);
    }
    
    if (generateGradesReportBtn) {
        generateGradesReportBtn.addEventListener('click', generateGradesReport);
    }
    
    if (generateCSVReportBtn) {
        generateCSVReportBtn.addEventListener('click', generateCSVReport);
    }
    
    if (convertToPDFBtn) {
        convertToPDFBtn.addEventListener('click', convertToPDF);
    }
    
    // Functions
    function populateModuleSelections() {
        // Create module checkboxes for all module selections
        const moduleSelections = [moduleSelection, assessmentModuleSelection, gradesModuleSelection];
        
        // Add the new subset and exclude module selections
        const additionalSelections = [document.getElementById('module-subset-selection'), document.getElementById('module-exclude-selection')];
        
        // Combine all module selection containers
        const allSelections = [...moduleSelections, ...additionalSelections.filter(item => item !== null)];
        
        allSelections.forEach(container => {
            if (container) {
                // Clear existing content
                container.innerHTML = '';
                
                // Add checkboxes for modules 1-14
                for (let i = 1; i <= 14; i++) {
                    const checkboxItem = document.createElement('div');
                    checkboxItem.className = 'checkbox-item';
                    
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.id = `${container.id}-module-${i}`;
                    checkbox.value = i;
                    
                    // Only check boxes by default for the main module selection
                    checkbox.checked = container.id === 'module-selection';
                    
                    const label = document.createElement('label');
                    label.htmlFor = `${container.id}-module-${i}`;
                    label.textContent = `Module ${i}`;
                    
                    checkboxItem.appendChild(checkbox);
                    checkboxItem.appendChild(label);
                    container.appendChild(checkboxItem);
                }
            }
        });
    }
    
    function getSelectedModules(container) {
        if (!container) return [];
        
        const checkboxes = container.querySelectorAll('input[type="checkbox"]:checked');
        return Array.from(checkboxes).map(cb => parseInt(cb.value));
    }
    
    async function generateModuleReport() {
        const date = moduleDate.value.trim();
        
        if (!date || !isValidDate(date)) {
            alert('Please enter a valid date in YY-MM-DD format');
            return;
        }
        
        // Get selected modules for all three options
        const allModules = getSelectedModules(moduleSelection);
        const subsetModules = getSelectedModules(document.getElementById('module-subset-selection'));
        const excludeModules = getSelectedModules(document.getElementById('module-exclude-selection'));
        
        if (allModules.length === 0) {
            alert('Please select at least one module in the All Modules section');
            return;
        }
        
        // Build request data to match CLI command format
        const requestData = {
            date: date,
            all_modules: allModules,
            count_partial: moduleCountPartial.checked
        };
        
        // Add subset modules if selected
        if (subsetModules.length > 0) {
            requestData.subset_modules = subsetModules;
        }
        
        // Add exclude modules if selected
        if (excludeModules.length > 0) {
            requestData.exclude_modules = excludeModules;
        }
        
        // Add output prefix if provided
        if (moduleOutputPrefix.value.trim()) {
            requestData.output_prefix = moduleOutputPrefix.value.trim();
        }
        
        // Build CLI command for logging
        let cliCommand = `compita flexible-module --date ${date} --all-modules ${allModules.join(' ')}`;
        
        if (subsetModules.length > 0) {
            cliCommand += ` --subset-modules ${subsetModules.join(' ')}`;
        }
        
        if (excludeModules.length > 0) {
            cliCommand += ` --exclude-modules ${excludeModules.join(' ')}`;
        }
        
        if (moduleCountPartial.checked) {
            cliCommand += ' --count-partial';
        }
        
        if (moduleOutputPrefix.value.trim()) {
            cliCommand += ` --output-prefix ${moduleOutputPrefix.value.trim()}`;
        }
        
        // Log equivalent CLI command for reference
        console.log(`Equivalent CLI command: ${cliCommand}`);
        
        // Send request to API
        await generateFlexibleReport('flexible-module', requestData);
    }
    
    async function generateAssessmentReport() {
        const date = assessmentDate.value.trim();
        
        if (!date || !isValidDate(date)) {
            alert('Please enter a valid date in YY-MM-DD format');
            return;
        }
        
        const assessmentTypes = [];
        if (assessmentQuiz.checked) assessmentTypes.push('quiz');
        if (assessmentTest.checked) assessmentTypes.push('test');
        if (assessmentExam.checked) assessmentTypes.push('exam');
        
        if (assessmentTypes.length === 0) {
            alert('Please select at least one assessment type');
            return;
        }
        
        const selectedModules = getSelectedModules(assessmentModuleSelection);
        
        const requestData = {
            date: date,
            assessment_types: assessmentTypes
        };
        
        if (selectedModules.length > 0) {
            requestData.modules = selectedModules;
        }
        
        if (assessmentOutputPrefix.value.trim()) {
            requestData.output_prefix = assessmentOutputPrefix.value.trim();
        }
        
        await generateFlexibleReport('flexible-assessment', requestData);
    }
    
    async function generateGradesReport() {
        const date = gradesDate.value.trim();
        
        if (!date || !isValidDate(date)) {
            alert('Please enter a valid date in YY-MM-DD format');
            return;
        }
        
        const gradeCategories = [];
        if (gradesQuiz.checked) gradeCategories.push('quiz');
        if (gradesTest.checked) gradeCategories.push('test');
        if (gradesExam.checked) gradeCategories.push('exam');
        if (gradesHomework.checked) gradeCategories.push('homework');
        if (gradesParticipation.checked) gradeCategories.push('participation');
        
        if (gradeCategories.length === 0) {
            alert('Please select at least one grade category');
            return;
        }
        
        const gradeWeights = {};
        if (gradesQuiz.checked) gradeWeights.quiz = parseFloat(weightQuiz.value) / 100;
        if (gradesTest.checked) gradeWeights.test = parseFloat(weightTest.value) / 100;
        if (gradesExam.checked) gradeWeights.exam = parseFloat(weightExam.value) / 100;
        if (gradesHomework.checked) gradeWeights.homework = parseFloat(weightHomework.value) / 100;
        if (gradesParticipation.checked) gradeWeights.participation = parseFloat(weightParticipation.value) / 100;
        
        const selectedModules = getSelectedModules(gradesModuleSelection);
        
        const requestData = {
            date: date,
            grade_categories: gradeCategories,
            grade_weights: gradeWeights
        };
        
        if (selectedModules.length > 0) {
            requestData.modules = selectedModules;
        }
        
        if (gradesOutputPrefix.value.trim()) {
            requestData.output_prefix = gradesOutputPrefix.value.trim();
        }
        
        await generateFlexibleReport('flexible-grades', requestData);
    }
    
    async function generateCSVReport() {
        const date = csvDate.value.trim();
        const type = csvType.value;
        
        if (!date || !isValidDate(date)) {
            alert('Please enter a valid date in YY-MM-DD format');
            return;
        }
        
        let endpoint = '';
        const requestData = { date };
        
        switch (type) {
            case 'module':
                endpoint = 'csv-module';
                if (csvModuleNumber.value.trim()) {
                    requestData.module = parseInt(csvModuleNumber.value.trim());
                } else {
                    alert('Please enter a module number');
                    return;
                }
                break;
            case 'student':
                endpoint = 'csv-student';
                if (csvStudentName.value.trim()) {
                    requestData.student = csvStudentName.value.trim();
                } else {
                    alert('Please enter a student name');
                    return;
                }
                break;
            case 'class':
                endpoint = 'csv-class';
                break;
            case 'all':
                endpoint = 'csv-all';
                break;
            default:
                alert('Please select a valid report type');
                return;
        }
        
        await generateFlexibleReport(endpoint, requestData);
    }
    
    async function convertToPDF() {
        const date = pdfDate.value.trim();
        const type = pdfType.value;
        
        if (!date || !isValidDate(date)) {
            alert('Please enter a valid date in YY-MM-DD format');
            return;
        }
        
        const requestData = {
            date: date
        };
        
        if (type !== 'all') {
            requestData.type = type;
        }
        
        if (pdfOutputDir.value.trim()) {
            requestData.output_dir = pdfOutputDir.value.trim();
        } else {
            requestData.output_dir = `reports/${date}/executive_reports`;
        }
        
        await generateFlexibleReport('markdown-to-pdf', requestData);
    }
    
    async function generateFlexibleReport(endpoint, requestData) {
        try {
            flexibleStatusText.textContent = 'Generating...';
            flexibleMessage.textContent = `Generating ${endpoint} report...`;
            flexibleStatusContainer.classList.remove('hidden');
            
            const response = await fetch(`${API_URL}/api/v1/${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });
            
            const data = await response.json();
            
            if (response.ok) {
                currentTaskId = data.task_id;
                updateFlexibleStatus(data);
                
                // Start polling for status updates
                pollFlexibleStatus(data.task_id);
            } else {
                flexibleStatusText.textContent = 'Error';
                flexibleMessage.textContent = data.detail || `Failed to generate ${endpoint} report`;
            }
        } catch (error) {
            console.error(`Error generating ${endpoint} report:`, error);
            flexibleStatusText.textContent = 'Error';
            flexibleMessage.textContent = 'Failed to connect to the API. Please check if the server is running.';
        }
    }
    
    function updateFlexibleStatus(data) {
        flexibleTaskId.textContent = data.task_id || currentTaskId;
        flexibleStatusText.textContent = data.status || 'Unknown';
        flexibleMessage.textContent = data.message || '';
        flexibleTimestamp.textContent = data.timestamp || new Date().toISOString();
        
        // Update status color
        flexibleStatusText.className = '';
        if (data.status === 'completed') {
            flexibleStatusText.classList.add('success');
        } else if (data.status === 'failed') {
            flexibleStatusText.classList.add('error');
        } else if (data.status === 'running') {
            flexibleStatusText.classList.add('warning');
        }
    }
    
    function pollFlexibleStatus(taskId) {
        const interval = setInterval(async () => {
            try {
                const response = await fetch(`${API_URL}/api/v1/status/${taskId}`);
                const data = await response.json();
                
                if (response.ok) {
                    updateFlexibleStatus(data);
                    
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
