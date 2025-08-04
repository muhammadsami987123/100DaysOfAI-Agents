// EmailWriterAgent - JavaScript for Web Interface

class EmailWriterApp {
    constructor() {
        this.currentEmail = null;
        this.initializeEventListeners();
        this.loadHistory();
    }

    initializeEventListeners() {
        // Form submission
        const emailForm = document.getElementById('emailForm');
        if (emailForm) {
            emailForm.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }

        // Clear button
        const clearBtn = document.getElementById('clearBtn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearForm());
        }

        // Copy button
        const copyBtn = document.getElementById('copyBtn');
        if (copyBtn) {
            copyBtn.addEventListener('click', () => this.copyEmail());
        }

        // Download button
        const downloadBtn = document.getElementById('downloadBtn');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', () => this.downloadEmail());
        }

        // Regenerate button
        const regenerateBtn = document.getElementById('regenerateBtn');
        if (regenerateBtn) {
            regenerateBtn.addEventListener('click', () => this.regenerateEmail());
        }

        // Edit button
        const editBtn = document.getElementById('editBtn');
        if (editBtn) {
            editBtn.addEventListener('click', () => this.toggleEditMode());
        }

        // Template selection
        const templateItems = document.querySelectorAll('.template-item');
        templateItems.forEach(item => {
            item.addEventListener('click', () => this.selectTemplate(item));
        });

        // Form field changes
        const formFields = ['prompt', 'template', 'tone', 'recipient', 'sender', 'signature'];
        formFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('change', () => this.updateFormState());
            }
        });
    }

    async handleFormSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const emailData = {
            prompt: formData.get('prompt'),
            template: formData.get('template'),
            recipient: formData.get('recipient'),
            sender: formData.get('sender'),
            signature: formData.get('signature'),
            tone: formData.get('tone') || null
        };

        if (!emailData.prompt.trim()) {
            this.showNotification('Please enter a prompt for the email', 'error');
            return;
        }

        await this.generateEmail(emailData);
    }

    async generateEmail(emailData) {
        try {
            this.showLoading(true);
            
            const response = await fetch('/api/generate-email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(emailData)
            });

            const result = await response.json();

            if (result.success) {
                this.currentEmail = result.email;
                this.displayEmail(result.email);
                this.showNotification('Email generated successfully!', 'success');
                this.loadHistory(); // Refresh history
            } else {
                this.showNotification(result.error || 'Failed to generate email', 'error');
            }
        } catch (error) {
            console.error('Error generating email:', error);
            this.showNotification('Network error. Please try again.', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    displayEmail(email) {
        const preview = document.getElementById('emailPreview');
        const subject = document.getElementById('previewSubject');
        const to = document.getElementById('previewTo');
        const from = document.getElementById('previewFrom');
        const body = document.getElementById('previewBody');

        if (preview && subject && to && from && body) {
            subject.value = email.subject || 'No subject';
            to.value = email.to || 'No recipient';
            from.value = email.from || 'No sender';
            body.value = email.body || 'No content';

            // Ensure all fields start in readonly mode (view mode)
            subject.readOnly = true;
            to.readOnly = true;
            from.readOnly = true;
            body.readOnly = true;

            preview.style.display = 'block';
            preview.classList.add('fade-in');
            
            // Scroll to preview
            preview.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            
            // Reset edit button to "Edit Email" state
            const editBtn = document.getElementById('editBtn');
            if (editBtn) {
                editBtn.innerHTML = '<i class="fas fa-edit"></i> Edit Email';
                editBtn.className = 'btn btn-primary';
            }
            
            // Ensure preview container is not in edit mode
            preview.classList.remove('editing');
        }
    }

    async regenerateEmail() {
        if (!this.currentEmail) {
            this.showNotification('No email to regenerate', 'error');
            return;
        }

        // Get current form data
        const form = document.getElementById('emailForm');
        const formData = new FormData(form);
        
        const emailData = {
            prompt: formData.get('prompt'),
            template: formData.get('template'),
            recipient: formData.get('recipient'),
            sender: formData.get('sender'),
            signature: formData.get('signature'),
            tone: formData.get('tone') || null
        };

        await this.generateEmail(emailData);
    }

    copyEmail() {
        if (!this.currentEmail) {
            this.showNotification('No email to copy', 'error');
            return;
        }

        // Get current edited content
        const subject = document.getElementById('previewSubject')?.value || this.currentEmail.subject;
        const to = document.getElementById('previewTo')?.value || this.currentEmail.to;
        const from = document.getElementById('previewFrom')?.value || this.currentEmail.from;
        const body = document.getElementById('previewBody')?.value || this.currentEmail.body;

        const emailText = `Subject: ${subject}
To: ${to}
From: ${from}

${body}`;

        navigator.clipboard.writeText(emailText).then(() => {
            this.showNotification('Email copied to clipboard!', 'success');
        }).catch(() => {
            this.showNotification('Failed to copy email', 'error');
        });
    }

    downloadEmail() {
        if (!this.currentEmail) {
            this.showNotification('No email to download', 'error');
            return;
        }

        // Get current edited content
        const subject = document.getElementById('previewSubject')?.value || this.currentEmail.subject;
        const to = document.getElementById('previewTo')?.value || this.currentEmail.to;
        const from = document.getElementById('previewFrom')?.value || this.currentEmail.from;
        const body = document.getElementById('previewBody')?.value || this.currentEmail.body;

        const emailText = `Subject: ${subject}
To: ${to}
From: ${from}

${body}`;

        const blob = new Blob([emailText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `email_${Date.now()}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        this.showNotification('Email downloaded!', 'success');
    }

    clearForm() {
        const form = document.getElementById('emailForm');
        if (form) {
            form.reset();
        }

        const preview = document.getElementById('emailPreview');
        if (preview) {
            preview.style.display = 'none';
        }

        this.currentEmail = null;
        this.showNotification('Form cleared', 'info');
    }

    selectTemplate(templateItem) {
        // Remove active class from all templates
        document.querySelectorAll('.template-item').forEach(item => {
            item.classList.remove('active');
        });

        // Add active class to selected template
        templateItem.classList.add('active');

        // Update form template selection
        const templateKey = templateItem.dataset.template;
        const templateSelect = document.getElementById('template');
        if (templateSelect) {
            templateSelect.value = templateKey;
        }

        this.showNotification(`Template selected: ${templateItem.querySelector('h4').textContent}`, 'info');
    }

    async loadHistory() {
        try {
            const response = await fetch('/api/history');
            const result = await response.json();

            if (result.success) {
                this.displayHistory(result.history);
            }
        } catch (error) {
            console.error('Error loading history:', error);
        }
    }

    displayHistory(history) {
        const historyList = document.getElementById('historyList');
        if (!historyList) return;

        if (!history || history.length === 0) {
            historyList.innerHTML = '<p class="no-history">No emails generated yet</p>';
            return;
        }

        const historyHTML = history.slice(-5).reverse().map(entry => `
            <div class="history-item" onclick="app.loadHistoryItem('${entry.prompt}')">
                <h4>${entry.prompt.substring(0, 50)}${entry.prompt.length > 50 ? '...' : ''}</h4>
                <p>Template: ${entry.template}</p>
            </div>
        `).join('');

        historyList.innerHTML = historyHTML;
    }

    loadHistoryItem(prompt) {
        const promptField = document.getElementById('prompt');
        if (promptField) {
            promptField.value = prompt;
        }
        this.showNotification('Prompt loaded from history', 'info');
    }

    showLoading(show) {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.style.display = show ? 'flex' : 'none';
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-message">${message}</span>
                <button class="notification-close">&times;</button>
            </div>
        `;

        // Add to page
        document.body.appendChild(notification);

        // Add close button functionality
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        });

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.style.animation = 'slideOut 0.3s ease-out';
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.remove();
                    }
                }, 300);
            }
        }, 5000);
    }

    toggleEditMode() {
        const editBtn = document.getElementById('editBtn');
        const subject = document.getElementById('previewSubject');
        const to = document.getElementById('previewTo');
        const from = document.getElementById('previewFrom');
        const body = document.getElementById('previewBody');

        if (!editBtn || !subject || !to || !from || !body) return;

        const isEditing = editBtn.textContent.includes('Save');
        
        if (isEditing) {
            // Save mode - switch back to view mode
            subject.readOnly = true;
            to.readOnly = true;
            from.readOnly = true;
            body.readOnly = true;
            
            // Remove edit mode styling
            subject.classList.remove('editing');
            to.classList.remove('editing');
            from.classList.remove('editing');
            body.classList.remove('editing');
            
            // Remove edit mode from preview container
            const preview = document.getElementById('emailPreview');
            if (preview) {
                preview.classList.remove('editing');
            }
            
            editBtn.innerHTML = '<i class="fas fa-edit"></i> Edit Email';
            editBtn.className = 'btn btn-primary';
            
            this.showNotification('Changes saved! Email is now in view mode.', 'success');
        } else {
            // View mode - switch to edit mode
            subject.readOnly = false;
            to.readOnly = false;
            from.readOnly = false;
            body.readOnly = false;
            
            // Add edit mode styling
            subject.classList.add('editing');
            to.classList.add('editing');
            from.classList.add('editing');
            body.classList.add('editing');
            
            // Add edit mode to preview container
            const preview = document.getElementById('emailPreview');
            if (preview) {
                preview.classList.add('editing');
            }
            
            editBtn.innerHTML = '<i class="fas fa-save"></i> Save Changes';
            editBtn.className = 'btn btn-success';
            
            // Focus on the body for immediate editing
            body.focus();
            
            this.showNotification('Edit mode enabled. Make your changes and click "Save Changes" when done.', 'info');
        }
    }

    updateFormState() {
        // This method can be used to update form state based on field changes
        // For example, enabling/disabling buttons, updating preview, etc.
    }
}

// Add CSS for notifications
const notificationStyles = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }
    
    .notification-close {
        background: none;
        border: none;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        padding: 0;
        line-height: 1;
    }
    
    .notification-close:hover {
        opacity: 0.8;
    }
`;

// Add styles to head
const styleSheet = document.createElement('style');
styleSheet.textContent = notificationStyles;
document.head.appendChild(styleSheet);

// Initialize app when DOM is loaded
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new EmailWriterApp();
});

// Make app globally available for history item clicks
window.app = app; 