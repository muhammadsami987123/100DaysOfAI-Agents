// MemoryNotesBot Web Application JavaScript
function memoryBot() {
    return {
        // State
        activeTab: 'save',
        newMemory: {
            content: '',
            memory_type: 'long_term',
            priority: 'medium',
            category: '',
            tags: [],
            expires_in_hours: null
        },
        newTag: '',
        searchQuery: '',
        searchResults: [],
        forgetQuery: '',
        forgetResults: [],
        historyResults: [],
        historyTitle: '',
        statistics: null,
        showStats: false,
        showExport: false,
        showEditModal: false,
        editingMemory: {},
        editTag: '',
        exportFormat: 'json',
        exportTags: '',
        exportCategory: '',
        notification: {
            show: false,
            message: '',
            type: 'success'
        },

        // Initialize
        init() {
            this.loadStatistics();
            this.setupAutoSave();
        },

        // Utility functions
        showNotification(message, type = 'success') {
            this.notification = {
                show: true,
                message: message,
                type: type
            };
            setTimeout(() => {
                this.notification.show = false;
            }, 5000);
        },

        formatDate(dateString) {
            if (!dateString) return 'Never';
            const date = new Date(dateString);
            return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        },

        getPriorityClass(priority) {
            const classes = {
                'critical': 'priority-critical',
                'high': 'priority-high',
                'medium': 'priority-medium',
                'low': 'priority-low'
            };
            return classes[priority] || 'priority-medium';
        },

        getTypeClass(type) {
            const classes = {
                'short_term': 'type-short_term',
                'long_term': 'type-long_term',
                'reminder': 'type-reminder',
                'password': 'type-password',
                'idea': 'type-idea',
                'task': 'type-task',
                'contact': 'type-contact',
                'project': 'type-project'
            };
            return classes[type] || 'type-long_term';
        },

        // Tag management
        addTag() {
            if (this.newTag.trim() && !this.newMemory.tags.includes(this.newTag.trim())) {
                this.newMemory.tags.push(this.newTag.trim());
                this.newTag = '';
            }
        },

        removeTag(tag) {
            this.newMemory.tags = this.newMemory.tags.filter(t => t !== tag);
        },

        addEditTag() {
            if (this.editTag.trim() && !this.editingMemory.tags.includes(this.editTag.trim())) {
                this.editingMemory.tags.push(this.editTag.trim());
                this.editTag = '';
            }
        },

        removeEditTag(tag) {
            this.editingMemory.tags = this.editingMemory.tags.filter(t => t !== tag);
        },

        // Memory operations
        async saveMemory() {
            if (!this.newMemory.content.trim()) {
                this.showNotification('Please enter memory content', 'error');
                return;
            }

            try {
                const response = await fetch('/api/memories', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.newMemory)
                });

                const result = await response.json();

                if (result.success) {
                    this.showNotification('Memory saved successfully!', 'success');
                    this.resetNewMemory();
                    // Switch to recall tab to show the new memory
                    this.activeTab = 'recall';
                    this.searchQuery = this.newMemory.content;
                    this.searchMemories();
                } else {
                    this.showNotification('Error saving memory: ' + result.error, 'error');
                }
            } catch (error) {
                this.showNotification('Error saving memory: ' + error.message, 'error');
            }
        },

        resetNewMemory() {
            this.newMemory = {
                content: '',
                memory_type: 'long_term',
                priority: 'medium',
                category: '',
                tags: [],
                expires_in_hours: null
            };
        },

        async enhanceWithAI() {
            if (!this.newMemory.content.trim()) {
                this.showNotification('Please enter memory content first', 'error');
                return;
            }

            try {
                const response = await fetch('/api/ai/enhance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ content: this.newMemory.content })
                });

                const result = await response.json();

                if (result.success && result.enhancement.enhanced) {
                    const suggestions = result.enhancement.suggestions;
                    
                    // Apply AI suggestions
                    this.newMemory.tags = suggestions.tags || [];
                    this.newMemory.category = suggestions.category || '';
                    this.newMemory.priority = suggestions.priority || 'medium';
                    this.newMemory.memory_type = suggestions.memory_type || 'long_term';
                    
                    this.showNotification('AI enhancement applied!', 'success');
                } else {
                    this.showNotification('AI enhancement not available', 'error');
                }
            } catch (error) {
                this.showNotification('Error enhancing memory: ' + error.message, 'error');
            }
        },

        async searchMemories() {
            if (!this.searchQuery.trim()) {
                this.showNotification('Please enter a search query', 'error');
                return;
            }

            try {
                const response = await fetch('/api/memories/search', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: this.searchQuery })
                });

                const result = await response.json();

                if (result.success) {
                    this.searchResults = result.memories;
                    if (result.search_enhancement && result.search_enhancement.enhanced) {
                        this.showNotification('Search enhanced with AI suggestions', 'success');
                    }
                } else {
                    this.showNotification('Error searching memories: ' + result.error, 'error');
                }
            } catch (error) {
                this.showNotification('Error searching memories: ' + error.message, 'error');
            }
        },

        async searchForForget() {
            if (!this.forgetQuery.trim()) {
                this.showNotification('Please enter a search query', 'error');
                return;
            }

            try {
                const response = await fetch('/api/memories/search', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: this.forgetQuery })
                });

                const result = await response.json();

                if (result.success) {
                    this.forgetResults = result.memories;
                } else {
                    this.showNotification('Error searching memories: ' + result.error, 'error');
                }
            } catch (error) {
                this.showNotification('Error searching memories: ' + error.message, 'error');
            }
        },

        async loadRecentMemories() {
            try {
                const response = await fetch('/api/memories/recent?limit=20');
                const result = await response.json();

                if (result.success) {
                    this.historyResults = result.memories;
                    this.historyTitle = 'Recent Memories';
                } else {
                    this.showNotification('Error loading recent memories: ' + result.error, 'error');
                }
            } catch (error) {
                this.showNotification('Error loading recent memories: ' + error.message, 'error');
            }
        },

        async loadFrequentMemories() {
            try {
                const response = await fetch('/api/memories/frequent?limit=20');
                const result = await response.json();

                if (result.success) {
                    this.historyResults = result.memories;
                    this.historyTitle = 'Frequently Accessed Memories';
                } else {
                    this.showNotification('Error loading frequent memories: ' + result.error, 'error');
                }
            } catch (error) {
                this.showNotification('Error loading frequent memories: ' + error.message, 'error');
            }
        },

        async loadMemoriesByTag() {
            const tag = prompt('Enter tag to search for:');
            if (!tag) return;

            try {
                const response = await fetch(`/api/memories/tags/${encodeURIComponent(tag)}`);
                const result = await response.json();

                if (result.success) {
                    this.historyResults = result.memories;
                    this.historyTitle = `Memories tagged '${tag}'`;
                } else {
                    this.showNotification('Error loading memories by tag: ' + result.error, 'error');
                }
            } catch (error) {
                this.showNotification('Error loading memories by tag: ' + error.message, 'error');
            }
        },

        async loadStatistics() {
            try {
                const response = await fetch('/api/statistics');
                const result = await response.json();

                if (result.success) {
                    this.statistics = result.statistics;
                }
            } catch (error) {
                console.error('Error loading statistics:', error);
            }
        },

        async deleteMemory(memoryId) {
            if (!confirm('Are you sure you want to delete this memory?')) {
                return;
            }

            try {
                const response = await fetch(`/api/memories/${memoryId}`, {
                    method: 'DELETE'
                });

                const result = await response.json();

                if (result.success) {
                    this.showNotification('Memory deleted successfully', 'success');
                    
                    // Remove from current results
                    this.searchResults = this.searchResults.filter(m => m.id !== memoryId);
                    this.forgetResults = this.forgetResults.filter(m => m.id !== memoryId);
                    this.historyResults = this.historyResults.filter(m => m.id !== memoryId);
                    
                    // Reload statistics
                    this.loadStatistics();
                } else {
                    this.showNotification('Error deleting memory: ' + result.error, 'error');
                }
            } catch (error) {
                this.showNotification('Error deleting memory: ' + error.message, 'error');
            }
        },

        editMemory(memory) {
            this.editingMemory = { ...memory };
            this.showEditModal = true;
        },

        async updateMemory() {
            try {
                const response = await fetch(`/api/memories/${this.editingMemory.id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.editingMemory)
                });

                const result = await response.json();

                if (result.success) {
                    this.showNotification('Memory updated successfully', 'success');
                    this.showEditModal = false;
                    
                    // Update in current results
                    this.updateMemoryInResults(this.editingMemory);
                } else {
                    this.showNotification('Error updating memory: ' + result.error, 'error');
                }
            } catch (error) {
                this.showNotification('Error updating memory: ' + error.message, 'error');
            }
        },

        updateMemoryInResults(updatedMemory) {
            // Update in search results
            const searchIndex = this.searchResults.findIndex(m => m.id === updatedMemory.id);
            if (searchIndex !== -1) {
                this.searchResults[searchIndex] = updatedMemory;
            }

            // Update in forget results
            const forgetIndex = this.forgetResults.findIndex(m => m.id === updatedMemory.id);
            if (forgetIndex !== -1) {
                this.forgetResults[forgetIndex] = updatedMemory;
            }

            // Update in history results
            const historyIndex = this.historyResults.findIndex(m => m.id === updatedMemory.id);
            if (historyIndex !== -1) {
                this.historyResults[historyIndex] = updatedMemory;
            }
        },

        async exportMemories() {
            try {
                const response = await fetch('/api/export', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        format: this.exportFormat,
                        tags: this.exportTags ? this.exportTags.split(',').map(t => t.trim()) : [],
                        category: this.exportCategory || null
                    })
                });

                const result = await response.json();

                if (result.success) {
                    this.showNotification('Memories exported successfully', 'success');
                    
                    // Download the file
                    const downloadUrl = `/api/export/download/${result.filename}`;
                    const link = document.createElement('a');
                    link.href = downloadUrl;
                    link.download = result.filename;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                    
                    this.showExport = false;
                } else {
                    this.showNotification('Error exporting memories: ' + result.error, 'error');
                }
            } catch (error) {
                this.showNotification('Error exporting memories: ' + error.message, 'error');
            }
        },

        async testVoice() {
            try {
                const response = await fetch('/api/voice/test', {
                    method: 'POST'
                });

                const result = await response.json();

                if (result.success) {
                    const testResult = result.test_result;
                    if (testResult.tts_test && testResult.stt_test) {
                        this.showNotification('Voice test successful!', 'success');
                    } else {
                        this.showNotification('Voice test failed: ' + (testResult.error || 'Unknown error'), 'error');
                    }
                } else {
                    this.showNotification('Error testing voice: ' + result.error, 'error');
                }
            } catch (error) {
                this.showNotification('Error testing voice: ' + error.message, 'error');
            }
        },

        // Auto-save functionality
        setupAutoSave() {
            let autoSaveTimer;
            
            // Auto-save content every 30 seconds
            this.$watch('newMemory.content', (value) => {
                if (value.trim()) {
                    clearTimeout(autoSaveTimer);
                    autoSaveTimer = setTimeout(() => {
                        // Save to localStorage as draft
                        localStorage.setItem('memoryBot_draft', JSON.stringify(this.newMemory));
                    }, 30000);
                }
            });
        },

        // Load draft from localStorage
        loadDraft() {
            const draft = localStorage.getItem('memoryBot_draft');
            if (draft) {
                try {
                    this.newMemory = JSON.parse(draft);
                    this.showNotification('Draft loaded from previous session', 'success');
                } catch (error) {
                    console.error('Error loading draft:', error);
                }
            }
        },

        // Clear draft
        clearDraft() {
            localStorage.removeItem('memoryBot_draft');
            this.showNotification('Draft cleared', 'success');
        },

        // Keyboard shortcuts
        setupKeyboardShortcuts() {
            document.addEventListener('keydown', (e) => {
                // Ctrl/Cmd + S to save
                if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                    e.preventDefault();
                    this.saveMemory();
                }
                
                // Ctrl/Cmd + K to focus search
                if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                    e.preventDefault();
                    this.activeTab = 'recall';
                    this.$nextTick(() => {
                        document.querySelector('input[placeholder*="looking for"]').focus();
                    });
                }
                
                // Ctrl/Cmd + N for new memory
                if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
                    e.preventDefault();
                    this.activeTab = 'save';
                    this.$nextTick(() => {
                        document.querySelector('textarea[placeholder*="remember"]').focus();
                    });
                }
            });
        }
    };
}

// Initialize keyboard shortcuts when Alpine.js is ready
document.addEventListener('alpine:init', () => {
    Alpine.data('memoryBot', memoryBot);
});

// Additional utility functions
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

// Search suggestions (if needed)
function setupSearchSuggestions() {
    const searchInput = document.querySelector('input[placeholder*="looking for"]');
    if (searchInput) {
        const debouncedSearch = debounce((query) => {
            // Implement search suggestions here
            console.log('Search suggestion for:', query);
        }, 300);
        
        searchInput.addEventListener('input', (e) => {
            debouncedSearch(e.target.value);
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    setupSearchSuggestions();
});
