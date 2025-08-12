// JobApplicationAgent Frontend JavaScript

class JobApplicationAgent {
    constructor() {
        this.selectedFile = null;
        this.generatedData = null;
        this.currentInputMode = 'text';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateGenerateButton();
    }

    setupEventListeners() {
        // File upload
        const uploadZone = document.getElementById('uploadZone');
        const resumeFile = document.getElementById('resumeFile');

        uploadZone.addEventListener('click', () => resumeFile.click());
        uploadZone.addEventListener('dragover', this.handleDragOver.bind(this));
        uploadZone.addEventListener('drop', this.handleDrop.bind(this));
        resumeFile.addEventListener('change', this.handleFileSelect.bind(this));

        // Job description input modes
        const inputModeRadios = document.querySelectorAll('input[name="inputMode"]');
        inputModeRadios.forEach(radio => {
            radio.addEventListener('change', this.handleInputModeChange.bind(this));
        });

        // Job description
        const jobDescription = document.getElementById('jobDescription');
        jobDescription.addEventListener('input', this.handleJobDescriptionInput.bind(this));

        // URL extraction
        const extractUrlBtn = document.getElementById('extractUrlBtn');
        extractUrlBtn.addEventListener('click', this.extractJobFromUrl.bind(this));

        // Extracted job description
        const extractedJobDescription = document.getElementById('extractedJobDescription');
        extractedJobDescription.addEventListener('input', this.handleJobDescriptionInput.bind(this));

        // Additional documents checkboxes
        const additionalDocCheckboxes = document.querySelectorAll('input[name="additionalDocs"]');
        additionalDocCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', this.handleAdditionalDocsChange.bind(this));
        });

        // Generate button
        const generateBtn = document.getElementById('generateBtn');
        generateBtn.addEventListener('click', this.generateApplication.bind(this));

        // Download buttons
        document.getElementById('downloadResumePdf').addEventListener('click', () => this.downloadDocument('resume', 'pdf'));
        document.getElementById('downloadResumeDocx').addEventListener('click', () => this.downloadDocument('resume', 'docx'));
        document.getElementById('downloadCoverLetterPdf').addEventListener('click', () => this.downloadDocument('cover-letter', 'pdf'));
        document.getElementById('downloadCoverLetterDocx').addEventListener('click', () => this.downloadDocument('cover-letter', 'docx'));
    }

    handleInputModeChange(e) {
        this.currentInputMode = e.target.value;
        
        if (this.currentInputMode === 'text') {
            document.getElementById('manualInputMode').classList.remove('hidden');
            document.getElementById('urlInputMode').classList.add('hidden');
        } else {
            document.getElementById('manualInputMode').classList.add('hidden');
            document.getElementById('urlInputMode').classList.remove('hidden');
        }
        
        this.updateGenerateButton();
    }

    async extractJobFromUrl() {
        const url = document.getElementById('jobUrl').value.trim();
        
        if (!url) {
            this.showError('Please enter a job posting URL.');
            return;
        }

        // Show loading state
        document.getElementById('urlExtractionStatus').classList.remove('hidden');
        document.getElementById('extractedContent').classList.add('hidden');
        this.hideError();

        try {
            const formData = new FormData();
            formData.append('url', url);

            const response = await fetch('/api/extract-job-from-url', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok && result.success) {
                // Populate the extracted content
                document.getElementById('extractedJobDescription').value = result.content;
                document.getElementById('extractedContent').classList.remove('hidden');
                this.updateGenerateButton();
                this.showSuccess('Job description extracted successfully!');
            } else {
                const message = result.error || result.detail || 'Failed to extract job description';
                throw new Error(message);
            }
        } catch (error) {
            console.error('URL extraction error:', error);
            this.showError(error.message || 'Failed to extract job description from URL.');
        } finally {
            document.getElementById('urlExtractionStatus').classList.add('hidden');
        }
    }

    handleDragOver(e) {
        e.preventDefault();
        e.currentTarget.classList.add('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        e.currentTarget.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.processFile(files[0]);
        }
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            this.processFile(file);
        }
    }

    processFile(file) {
        // Validate file type
        const allowedTypes = ['.pdf', '.docx', '.doc'];
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
        
        if (!allowedTypes.includes(fileExtension)) {
            this.showError('Please select a PDF or DOCX file.');
            return;
        }

        // Validate file size (10MB)
        if (file.size > 10 * 1024 * 1024) {
            this.showError('File size must be less than 10MB.');
            return;
        }

        this.selectedFile = file;
        this.updateFileInfo(file);
        this.updateGenerateButton();
        this.hideError();
    }

    updateFileInfo(file) {
        const fileInfo = document.getElementById('fileInfo');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');

        fileName.textContent = file.name;
        fileSize.textContent = this.formatFileSize(file.size);
        fileInfo.classList.remove('hidden');
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    handleJobDescriptionInput(e) {
        const text = e.target.value;
        const charCount = document.getElementById('charCount');
        charCount.textContent = `${text.length} characters`;
        
        this.updateGenerateButton();
    }

    updateGenerateButton() {
        const generateBtn = document.getElementById('generateBtn');
        let jobDescription = '';
        
        if (this.currentInputMode === 'text') {
            jobDescription = document.getElementById('jobDescription').value.trim();
        } else {
            jobDescription = document.getElementById('extractedJobDescription').value.trim();
        }
        
        const isValid = this.selectedFile && jobDescription.length >= 50;
        generateBtn.disabled = !isValid;
    }

    getSelectedAdditionalDocuments() {
        const checkboxes = document.querySelectorAll('input[name="additionalDocs"]:checked');
        return Array.from(checkboxes).map(cb => cb.value);
    }

    async generateApplication() {
        if (!this.selectedFile) {
            this.showError('Please upload a resume file.');
            return;
        }

        let jobDescription = '';
        if (this.currentInputMode === 'text') {
            jobDescription = document.getElementById('jobDescription').value.trim();
        } else {
            jobDescription = document.getElementById('extractedJobDescription').value.trim();
        }

        if (jobDescription.length < 50) {
            this.showError('Please enter a job description (minimum 50 characters).');
            return;
        }

        this.showLoading();
        this.hideError();
        this.hideResults();

        try {
            const formData = new FormData();
            formData.append('resume_file', this.selectedFile);
            formData.append('job_description', jobDescription);
            formData.append('language', document.getElementById('language').value);
            formData.append('cover_letter_length', document.getElementById('coverLetterLength').value);
            
            // Add additional documents
            const additionalDocs = this.getSelectedAdditionalDocuments();
            if (additionalDocs.length > 0) {
                formData.append('additional_documents', additionalDocs.join(','));
            }

            const response = await fetch('/api/generate-application', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok && result.success) {
                this.generatedData = result.data;
                this.displayResults(result.data);
                this.showSuccess();
            } else {
                throw new Error(result.error || 'Failed to generate application');
            }
        } catch (error) {
            console.error('Generation error:', error);
            this.showError(error.message || 'An error occurred while generating your application.');
        } finally {
            this.hideLoading();
        }
    }

    displayResults(data) {
        // Display fit summary
        this.displayFitSummary(data.fit_summary);

        // Display customized resume
        document.getElementById('customizedResume').textContent = data.customized_resume;

        // Display cover letter
        document.getElementById('coverLetter').textContent = data.cover_letter;

        // Display additional documents
        this.displayAdditionalDocuments(data.additional_documents || {});

        // Show results section
        document.getElementById('resultsSection').classList.remove('hidden');
        
        // Scroll to results
        document.getElementById('resultsSection').scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }

    displayAdditionalDocuments(additionalDocs) {
        if (Object.keys(additionalDocs).length === 0) {
            return;
        }

        // Show additional documents section
        document.getElementById('additionalDocumentsSection').classList.remove('hidden');

        // Display each additional document
        const docMappings = {
            'personal_statement': { element: 'personalStatement', card: 'personalStatementCard' },
            'reference_page': { element: 'referencePage', card: 'referencePageCard' },
            'thank_you_note': { element: 'thankYouNote', card: 'thankYouNoteCard' },
            'motivation_letter': { element: 'motivationLetter', card: 'motivationLetterCard' },
            'linkedin_bio': { element: 'linkedinBio', card: 'linkedinBioCard' }
        };

        for (const [docType, content] of Object.entries(additionalDocs)) {
            if (docMappings[docType]) {
                const { element, card } = docMappings[docType];
                document.getElementById(element).textContent = content;
                document.getElementById(card).classList.remove('hidden');
            }
        }
    }

    displayFitSummary(fitSummary) {
        const fitSummaryDiv = document.getElementById('fitSummary');
        
        const html = `
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Match Percentage -->
                <div class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-6">
                    <div class="text-center">
                        <div class="text-3xl font-bold text-gray-900 mb-2">${fitSummary.match_percentage}%</div>
                        <div class="text-sm text-gray-600">Match Score</div>
                        <div class="w-full bg-gray-200 rounded-full h-2 mt-3">
                            <div class="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full" style="width: ${fitSummary.match_percentage}%"></div>
                        </div>
                    </div>
                </div>

                <!-- Key Strengths -->
                <div class="bg-green-50 rounded-xl p-6">
                    <h4 class="font-semibold text-green-800 mb-3 flex items-center">
                        <i class="fas fa-check-circle mr-2"></i>
                        Key Strengths
                    </h4>
                    <ul class="space-y-2">
                        ${fitSummary.key_strengths.map(strength => `
                            <li class="text-sm text-green-700 flex items-start">
                                <i class="fas fa-star text-yellow-500 mr-2 mt-0.5"></i>
                                ${strength}
                            </li>
                        `).join('')}
                    </ul>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
                <!-- Gap Areas -->
                <div class="bg-yellow-50 rounded-xl p-6">
                    <h4 class="font-semibold text-yellow-800 mb-3 flex items-center">
                        <i class="fas fa-exclamation-triangle mr-2"></i>
                        Areas for Improvement
                    </h4>
                    <ul class="space-y-2">
                        ${fitSummary.gap_areas.map(gap => `
                            <li class="text-sm text-yellow-700 flex items-start">
                                <i class="fas fa-lightbulb text-yellow-500 mr-2 mt-0.5"></i>
                                ${gap}
                            </li>
                        `).join('')}
                    </ul>
                </div>

                <!-- Recommendations -->
                <div class="bg-blue-50 rounded-xl p-6">
                    <h4 class="font-semibold text-blue-800 mb-3 flex items-center">
                        <i class="fas fa-lightbulb mr-2"></i>
                        Recommendations
                    </h4>
                    <ul class="space-y-2">
                        ${fitSummary.recommendations.map(rec => `
                            <li class="text-sm text-blue-700 flex items-start">
                                <i class="fas fa-arrow-right text-blue-500 mr-2 mt-0.5"></i>
                                ${rec}
                            </li>
                        `).join('')}
                    </ul>
                </div>
            </div>
        `;
        
        fitSummaryDiv.innerHTML = html;
    }

    async downloadDocument(type, format) {
        if (!this.generatedData) {
            this.showError('No generated content available for download.');
            return;
        }

        try {
            const content = type === 'resume' ? this.generatedData.customized_resume : this.generatedData.cover_letter;
            
            const formData = new FormData();
            formData.append('content', content);

            const response = await fetch(`/api/download/${type}/${format}`, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${type === 'resume' ? 'customized_resume' : 'cover_letter'}.${format}`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } else {
                throw new Error('Download failed');
            }
        } catch (error) {
            console.error('Download error:', error);
            this.showError('Failed to download document.');
        }
    }

    async downloadAdditionalDocument(docType, format) {
        if (!this.generatedData || !this.generatedData.additional_documents) {
            this.showError('No additional documents available for download.');
            return;
        }

        const content = this.generatedData.additional_documents[docType];
        if (!content) {
            this.showError('Document not found.');
            return;
        }

        try {
            const formData = new FormData();
            formData.append('content', content);

            const response = await fetch(`/api/download/additional-document/${docType}/${format}`, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                
                const docNames = {
                    'personal_statement': 'personal_statement',
                    'reference_page': 'reference_page',
                    'thank_you_note': 'thank_you_note',
                    'motivation_letter': 'motivation_letter',
                    'linkedin_bio': 'linkedin_bio'
                };
                
                a.download = `${docNames[docType] || docType}.${format}`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } else {
                throw new Error('Download failed');
            }
        } catch (error) {
            console.error('Download error:', error);
            this.showError('Failed to download document.');
        }
    }

    showLoading() {
        document.getElementById('loadingSection').classList.remove('hidden');
        document.getElementById('generateBtn').disabled = true;
        
        // Reset progress
        this.resetProgress();
        
        // Check if additional documents are selected
        const additionalDocs = this.getSelectedAdditionalDocuments();
        if (additionalDocs.length > 0) {
            this.showDocumentCount(additionalDocs.length);
        }
        
        // Start progress simulation
        this.startProgressSimulation(additionalDocs.length);
    }

    resetProgress() {
        // Reset progress bar
        document.getElementById('progressBar').style.width = '0%';
        
        // Reset progress steps
        document.querySelectorAll('.progress-step').forEach(step => {
            const icon = step.querySelector('i');
            const circle = step.querySelector('div');
            
            // Reset CSS classes
            step.classList.remove('active', 'completed', 'loading');
            
            // Reset icons based on step type
            const stepType = step.getAttribute('data-step');
            if (stepType === 'resume') {
                icon.className = 'fas fa-file-alt text-gray-500';
            } else if (stepType === 'cover') {
                icon.className = 'fas fa-envelope text-gray-500';
            } else if (stepType === 'additional') {
                icon.className = 'fas fa-file-plus text-gray-500';
            }
            
            circle.className = 'flex items-center justify-center w-8 h-8 bg-gray-200 rounded-full mx-auto mb-2';
        });
        
        // Reset current step text
        document.getElementById('currentStepText').textContent = 'Analyzing resume...';
        
        // Hide document count
        document.getElementById('documentCount').classList.add('hidden');
    }

    showDocumentCount(count) {
        const documentCount = document.getElementById('documentCount');
        const documentCountText = document.getElementById('documentCountText');
        
        const docNames = {
            'personal_statement': 'Personal Statement',
            'reference_page': 'Reference Page',
            'thank_you_note': 'Thank You Note',
            'motivation_letter': 'Motivation Letter',
            'linkedin_bio': 'LinkedIn Bio'
        };
        
        const selectedDocs = this.getSelectedAdditionalDocuments();
        const docList = selectedDocs.map(doc => docNames[doc] || doc).join(', ');
        
        documentCountText.textContent = `Generating ${count} additional document${count > 1 ? 's' : ''}: ${docList}`;
        documentCount.classList.remove('hidden');
    }

    startProgressSimulation(additionalDocCount) {
        const totalSteps = 3 + (additionalDocCount > 0 ? additionalDocCount : 0);
        let currentStep = 0;
        
        const steps = [
            { name: 'Analyzing resume...', step: 'resume', duration: 2000 },
            { name: 'Generating cover letter...', step: 'cover', duration: 3000 },
            { name: 'Generating additional documents...', step: 'additional', duration: 2000 + (additionalDocCount * 1000) }
        ];
        
        this.progressInterval = setInterval(() => {
            if (currentStep < steps.length) {
                this.updateProgressStep(steps[currentStep]);
                currentStep++;
            } else {
                clearInterval(this.progressInterval);
            }
        }, 1000);
        
        // Update progress bar
        let progress = 0;
        this.progressBarInterval = setInterval(() => {
            progress += 2;
            if (progress <= 100) {
                document.getElementById('progressBar').style.width = progress + '%';
            } else {
                clearInterval(this.progressBarInterval);
            }
        }, 100);
    }

    updateProgressStep(stepInfo) {
        // Update current step text
        document.getElementById('currentStepText').textContent = stepInfo.name;
        
        // Update progress step visual
        const stepElement = document.querySelector(`[data-step="${stepInfo.step}"]`);
        if (stepElement) {
            const icon = stepElement.querySelector('i');
            const circle = stepElement.querySelector('div');
            
            // Remove previous states
            stepElement.classList.remove('active', 'completed', 'loading');
            
            // Add active state
            stepElement.classList.add('active');
            
            // Update icon and circle
            if (stepInfo.step === 'resume') {
                icon.className = 'fas fa-file-alt text-blue-500';
                circle.className = 'flex items-center justify-center w-8 h-8 bg-blue-100 rounded-full mx-auto mb-2';
            } else if (stepInfo.step === 'cover') {
                icon.className = 'fas fa-envelope text-blue-500';
                circle.className = 'flex items-center justify-center w-8 h-8 bg-blue-100 rounded-full mx-auto mb-2';
            } else if (stepInfo.step === 'additional') {
                icon.className = 'fas fa-file-plus text-blue-500';
                circle.className = 'flex items-center justify-center w-8 h-8 bg-blue-100 rounded-full mx-auto mb-2';
            }
            
            // Mark previous steps as completed
            setTimeout(() => {
                stepElement.classList.remove('active');
                stepElement.classList.add('completed');
                
                // Update icon to checkmark for completed steps
                icon.className = 'fas fa-check text-green-500';
                circle.className = 'flex items-center justify-center w-8 h-8 bg-green-100 rounded-full mx-auto mb-2';
            }, 2000);
        }
    }

    hideLoading() {
        document.getElementById('loadingSection').classList.add('hidden');
        document.getElementById('generateBtn').disabled = false;
        
        // Clear any existing intervals
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
        }
        if (this.progressBarInterval) {
            clearInterval(this.progressBarInterval);
        }
        
        this.updateGenerateButton();
    }

    showResults() {
        document.getElementById('resultsSection').classList.remove('hidden');
    }

    hideResults() {
        document.getElementById('resultsSection').classList.add('hidden');
        document.getElementById('additionalDocumentsSection').classList.add('hidden');
        
        // Hide all additional document cards
        const additionalCards = [
            'personalStatementCard', 'referencePageCard', 'thankYouNoteCard',
            'motivationLetterCard', 'linkedinBioCard'
        ];
        additionalCards.forEach(cardId => {
            document.getElementById(cardId).classList.add('hidden');
        });
    }

    showError(message) {
        const errorSection = document.getElementById('errorSection');
        const errorMessage = document.getElementById('errorMessage');
        
        errorMessage.textContent = message;
        errorSection.classList.remove('hidden');
        errorSection.classList.add('error-shake');
        
        // Remove shake animation after it completes
        setTimeout(() => {
            errorSection.classList.remove('error-shake');
        }, 500);
    }

    hideError() {
        document.getElementById('errorSection').classList.add('hidden');
    }

    showSuccess(message = 'Application generated successfully!') {
        // Add success animation to results
        const resultsSection = document.getElementById('resultsSection');
        resultsSection.classList.add('success-animation');
        
        setTimeout(() => {
            resultsSection.classList.remove('success-animation');
        }, 600);
    }

    handleAdditionalDocsChange() {
        const additionalDocs = this.getSelectedAdditionalDocuments();
        const estimatedTimeElement = document.getElementById('estimatedTime');
        
        // Update estimated time based on number of additional documents
        let baseTime = 30;
        let additionalTime = additionalDocs.length * 10;
        let totalTime = baseTime + additionalTime;
        
        if (additionalDocs.length === 0) {
            estimatedTimeElement.textContent = 'Estimated time: 30-60 seconds';
        } else if (additionalDocs.length === 1) {
            estimatedTimeElement.textContent = `Estimated time: 40-70 seconds (${additionalDocs.length} additional document)`;
        } else {
            estimatedTimeElement.textContent = `Estimated time: ${totalTime}-${totalTime + 30} seconds (${additionalDocs.length} additional documents)`;
        }
        
        this.updateGenerateButton();
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const app = new JobApplicationAgent();
    window.jobAgent = app;
});

// Global function for additional document downloads
window.downloadAdditionalDocument = function(docType, format) {
    if (window.jobAgent) {
        window.jobAgent.downloadAdditionalDocument(docType, format);
    }
};

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add keyboard navigation support
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to generate application
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const generateBtn = document.getElementById('generateBtn');
        if (!generateBtn.disabled) {
            generateBtn.click();
        }
    }
});

// Add copy to clipboard functionality
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Show success message
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50';
        notification.textContent = 'Copied to clipboard!';
        document.body.appendChild(notification);
        
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
    });
}

// Add print functionality
function printDocument(content) {
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
        <html>
            <head>
                <title>Job Application</title>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }
                    pre { white-space: pre-wrap; font-family: inherit; }
                </style>
            </head>
            <body>
                <pre>${content}</pre>
            </body>
        </html>
    `);
    printWindow.document.close();
    printWindow.print();
}
