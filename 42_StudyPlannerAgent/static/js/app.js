/**
 * StudyPlannerAgent - Frontend JavaScript
 * Handles all UI interactions, API calls, and dynamic content updates
 */

// Global variables
let currentPlan = null;
let savedPlans = [];

// DOM elements
const elements = {
    // Form elements
    form: document.getElementById('study-plan-form'),
    goalInput: document.getElementById('goal'),
    daysInput: document.getElementById('days-available'),
    hoursInput: document.getElementById('hours-per-day'),
    subjectInput: document.getElementById('subject'),
    
    // Buttons
    generateBtn: document.getElementById('generate-btn'),
    viewPlansBtn: document.getElementById('view-plans-btn'),
    helpBtn: document.getElementById('help-btn'),
    downloadMdBtn: document.getElementById('download-md'),
    downloadJsonBtn: document.getElementById('download-json'),
    downloadPdfBtn: document.getElementById('download-pdf'),
    
    // Modals
    plansModal: document.getElementById('plans-modal'),
    helpModal: document.getElementById('help-modal'),
    closePlansModal: document.getElementById('close-plans-modal'),
    closeHelpModal: document.getElementById('close-help-modal'),
    
    // Content areas
    loadingState: document.getElementById('loading-state'),
    studyPlanDisplay: document.getElementById('study-plan-display'),
    planContent: document.getElementById('plan-content'),
    plansList: document.getElementById('plans-list'),
    toastContainer: document.getElementById('toast-container')
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Set up event listeners
    setupEventListeners();
    
    // Load saved plans
    loadSavedPlans();
    
    // Show welcome message
    showToast('Welcome to StudyPlannerAgent! 🎓', 'success');
}

function setupEventListeners() {
    // Form submission
    elements.form.addEventListener('submit', handleFormSubmit);
    
    // Navigation buttons
    elements.viewPlansBtn.addEventListener('click', showPlansModal);
    elements.helpBtn.addEventListener('click', showHelpModal);
    
    // Modal controls
    elements.closePlansModal.addEventListener('click', hidePlansModal);
    elements.closeHelpModal.addEventListener('click', hideHelpModal);
    
    // Download buttons
    elements.downloadMdBtn.addEventListener('click', () => downloadPlan('markdown'));
    elements.downloadJsonBtn.addEventListener('click', () => downloadPlan('json'));
    elements.downloadPdfBtn.addEventListener('click', () => downloadPlan('pdf'));
    
    // Close modals when clicking outside
    elements.plansModal.addEventListener('click', (e) => {
        if (e.target === elements.plansModal) {
            hidePlansModal();
        }
    });
    
    elements.helpModal.addEventListener('click', (e) => {
        if (e.target === elements.helpModal) {
            hideHelpModal();
        }
    });
    
    // Real-time validation
    elements.goalInput.addEventListener('input', validateForm);
    elements.daysInput.addEventListener('input', validateForm);
    elements.hoursInput.addEventListener('input', validateForm);
}

function validateForm() {
    const goal = elements.goalInput.value.trim();
    const days = parseInt(elements.daysInput.value);
    const hours = parseInt(elements.hoursInput.value);
    
    const isValid = goal.length > 0 && days > 0 && hours > 0;
    
    elements.generateBtn.disabled = !isValid;
    elements.generateBtn.classList.toggle('opacity-50', !isValid);
    elements.generateBtn.classList.toggle('cursor-not-allowed', !isValid);
}

function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(elements.form);
    const planData = {
        goal: formData.get('goal').trim(),
        days_available: parseInt(formData.get('days_available')),
        hours_per_day: parseInt(formData.get('hours_per_day')),
        learning_style: formData.get('learning_style'),
        difficulty: formData.get('difficulty'),
        subject: formData.get('subject').trim(),
        template: formData.get('template')
    };
    
    // Validate form data
    if (!planData.goal) {
        showToast('Please enter a study goal', 'error');
        return;
    }
    
    if (planData.days_available <= 0 || planData.hours_per_day <= 0) {
        showToast('Please enter valid time constraints', 'error');
        return;
    }
    
    // Generate study plan
    generateStudyPlan(planData);
}

async function generateStudyPlan(planData) {
    try {
        // Show loading state
        showLoadingState();
        
        // Make API call
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(planData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success) {
            currentPlan = result.plan;
            displayStudyPlan(result.plan);
            showToast('Study plan generated successfully! 🎉', 'success');
        } else {
            throw new Error(result.error || 'Failed to generate study plan');
        }
        
    } catch (error) {
        console.error('Error generating study plan:', error);
        showToast(`Error: ${error.message}`, 'error');
    } finally {
        hideLoadingState();
    }
}

function showLoadingState() {
    elements.form.style.display = 'none';
    elements.loadingState.classList.remove('hidden');
    elements.studyPlanDisplay.classList.add('hidden');
    elements.generateBtn.disabled = true;
}

function hideLoadingState() {
    elements.loadingState.classList.add('hidden');
    elements.generateBtn.disabled = false;
}

function displayStudyPlan(plan) {
    // Update plan content
    elements.planContent.innerHTML = formatPlanContent(plan);
    
    // Show the plan display
    elements.studyPlanDisplay.classList.remove('hidden');
    
    // Scroll to the plan
    elements.studyPlanDisplay.scrollIntoView({ behavior: 'smooth' });
}

function formatPlanContent(plan) {
    // Convert markdown-like content to HTML
    let content = plan.content;
    
    // Convert headers
    content = content.replace(/^# (.*$)/gim, '<h1 class="text-3xl font-bold text-white mb-4">$1</h1>');
    content = content.replace(/^## (.*$)/gim, '<h2 class="text-2xl font-bold text-white mb-3">$1</h2>');
    content = content.replace(/^### (.*$)/gim, '<h3 class="text-xl font-bold text-white mb-2">$1</h3>');
    
    // Convert bold text
    content = content.replace(/\*\*(.*?)\*\*/g, '<strong class="text-white font-semibold">$1</strong>');
    
    // Convert bullet points
    content = content.replace(/^[\s]*[-*+] (.*$)/gim, '<li class="text-white/80 mb-1">$1</li>');
    content = content.replace(/(<li.*<\/li>)/gs, '<ul class="list-disc list-inside mb-4 space-y-1">$1</ul>');
    
    // Convert numbered lists
    content = content.replace(/^[\s]*\d+\. (.*$)/gim, '<li class="text-white/80 mb-1">$1</li>');
    
    // Convert paragraphs
    content = content.replace(/^(?!<[h|u|l])(.*$)/gim, '<p class="text-white/80 mb-3">$1</p>');
    
    // Clean up empty paragraphs
    content = content.replace(/<p class="text-white\/80 mb-3"><\/p>/g, '');
    
    return content;
}

async function downloadPlan(format) {
    if (!currentPlan) {
        showToast('No plan to download', 'error');
        return;
    }
    
    try {
        showToast(`Preparing ${format.toUpperCase()} download...`, 'info');
        
        const response = await fetch(`/api/download/${currentPlan.id}/${format}`, {
            method: 'GET'
        });
        
        if (!response.ok) {
            if (response.status === 404) {
                // Plan not found, try to save it first
                showToast('Plan not found, saving it first...', 'warning');
                
                // Save the current plan in the requested format
                const saveResponse = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        goal: currentPlan.goal,
                        days_available: currentPlan.days_available,
                        hours_per_day: currentPlan.hours_per_day,
                        learning_style: currentPlan.learning_style,
                        difficulty: currentPlan.difficulty,
                        subject: currentPlan.subject,
                        template: currentPlan.template
                    })
                });
                
                if (saveResponse.ok) {
                    // Retry download
                    const retryResponse = await fetch(`/api/download/${currentPlan.id}/${format}`, {
                        method: 'GET'
                    });
                    
                    if (retryResponse.ok) {
                        const blob = await retryResponse.blob();
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `study_plan_${currentPlan.id}.${format === 'markdown' ? 'md' : format}`;
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(url);
                        document.body.removeChild(a);
                        
                        showToast(`Plan downloaded as ${format.toUpperCase()}! 📥`, 'success');
                        return;
                    }
                }
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `study_plan_${currentPlan.id}.${format === 'markdown' ? 'md' : format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showToast(`Plan downloaded as ${format.toUpperCase()}! 📥`, 'success');
        
    } catch (error) {
        console.error('Error downloading plan:', error);
        showToast(`Error downloading plan: ${error.message}`, 'error');
    }
}

async function loadSavedPlans() {
    try {
        const response = await fetch('/api/plans');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success) {
            savedPlans = result.plans;
            updatePlansList();
        }
        
    } catch (error) {
        console.error('Error loading saved plans:', error);
    }
}

function updatePlansList() {
    if (savedPlans.length === 0) {
        elements.plansList.innerHTML = `
            <div class="text-center py-8">
                <i class="fas fa-inbox text-4xl text-white/40 mb-4"></i>
                <p class="text-white/60">No saved study plans found.</p>
                <p class="text-white/60">Generate a new plan to get started!</p>
            </div>
        `;
        return;
    }
    
    elements.plansList.innerHTML = savedPlans.map(plan => `
        <div class="glass-card rounded-lg p-6 hover:bg-white/20 transition-all duration-200">
            <div class="flex items-center justify-between">
                <div class="flex-1">
                    <h4 class="text-xl font-bold text-white mb-2">${plan.goal}</h4>
                    <div class="flex items-center space-x-4 text-white/70 text-sm">
                        <span><i class="fas fa-calendar mr-1"></i>${plan.days_available} days</span>
                        <span><i class="fas fa-clock mr-1"></i>${plan.hours_per_day} hrs/day</span>
                        <span><i class="fas fa-palette mr-1"></i>${plan.learning_style}</span>
                        <span><i class="fas fa-chart-line mr-1"></i>${plan.difficulty}</span>
                    </div>
                    <p class="text-white/60 text-sm mt-2">Created: ${new Date(plan.created_at).toLocaleDateString()}</p>
                </div>
                <div class="flex space-x-2">
                    <button onclick="loadPlan('${plan.id}')" class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-2 rounded-lg transition-all duration-200">
                        <i class="fas fa-eye mr-1"></i>View
                    </button>
                    <button onclick="deletePlan('${plan.id}')" class="bg-red-500 hover:bg-red-600 text-white px-3 py-2 rounded-lg transition-all duration-200">
                        <i class="fas fa-trash mr-1"></i>Delete
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

async function loadPlan(planId) {
    try {
        const response = await fetch(`/api/plans/${planId}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success) {
            currentPlan = result.plan;
            displayStudyPlan(result.plan);
            hidePlansModal();
            showToast('Plan loaded successfully! 📚', 'success');
        } else {
            throw new Error(result.error || 'Failed to load plan');
        }
        
    } catch (error) {
        console.error('Error loading plan:', error);
        showToast(`Error loading plan: ${error.message}`, 'error');
    }
}

async function deletePlan(planId) {
    if (!confirm('Are you sure you want to delete this study plan?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/plans/${planId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success) {
            // Remove from local list
            savedPlans = savedPlans.filter(plan => plan.id !== planId);
            updatePlansList();
            showToast('Plan deleted successfully! 🗑️', 'success');
        } else {
            throw new Error(result.error || 'Failed to delete plan');
        }
        
    } catch (error) {
        console.error('Error deleting plan:', error);
        showToast(`Error deleting plan: ${error.message}`, 'error');
    }
}

function showPlansModal() {
    elements.plansModal.classList.remove('hidden');
    loadSavedPlans();
}

function hidePlansModal() {
    elements.plansModal.classList.add('hidden');
}

function showHelpModal() {
    elements.helpModal.classList.remove('hidden');
}

function hideHelpModal() {
    elements.helpModal.classList.add('hidden');
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `glass-card rounded-lg p-4 mb-2 fade-in ${
        type === 'success' ? 'border-green-500/50' :
        type === 'error' ? 'border-red-500/50' :
        type === 'warning' ? 'border-yellow-500/50' :
        'border-blue-500/50'
    }`;
    
    const icon = type === 'success' ? 'fas fa-check-circle text-green-400' :
                 type === 'error' ? 'fas fa-exclamation-circle text-red-400' :
                 type === 'warning' ? 'fas fa-exclamation-triangle text-yellow-400' :
                 'fas fa-info-circle text-blue-400';
    
    toast.innerHTML = `
        <div class="flex items-center">
            <i class="${icon} mr-3"></i>
            <span class="text-white">${message}</span>
        </div>
    `;
    
    elements.toastContainer.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// Utility functions
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function formatTime(hours) {
    if (hours < 1) {
        return `${Math.round(hours * 60)} minutes`;
    } else if (hours === 1) {
        return '1 hour';
    } else {
        return `${hours} hours`;
    }
}

// Export functions for global access
window.loadPlan = loadPlan;
window.deletePlan = deletePlan;
