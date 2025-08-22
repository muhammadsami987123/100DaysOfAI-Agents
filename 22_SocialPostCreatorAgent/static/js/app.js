// Global variables to store current post data
let currentPost = null;
let originalPostText = null; // Store original post text for editing

// DOM elements
const postForm = document.getElementById('postForm');
const generateBtn = document.getElementById('generateBtn');
const generateBtnText = document.getElementById('generateBtnText');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsSection = document.getElementById('resultsSection');
const postContent = document.getElementById('postContent');
const charCountDisplay = document.getElementById('charCountDisplay');
const charCountText = document.getElementById('charCountText');
const statusMessage = document.getElementById('statusMessage');

// Form submission handler
postForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Get form data
    const formData = new FormData(postForm);
    const platform = formData.get('platform');
    const topic = formData.get('topic');
    const tone = formData.get('tone');
    const saveToFile = formData.get('save_to_file') === 'on';
    
    // Validate form
    if (!platform || !topic || !tone) {
        showStatus('Please fill in all required fields.', 'error');
        return;
    }
    
    // Show loading state
    setLoadingState(true);
    
    try {
        // Make API call to generate post
        const response = await fetch('/generate', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Store current post data
            currentPost = {
                post_text: data.post_text,
                platform: data.platform,
                topic: data.topic,
                tone: data.tone
            };
            
            // Store original post text for editing
            originalPostText = data.post_text;
            
            // Display the generated post
            displayPost(data);
            
            // Show success message if saved to file
            if (data.saved_to) {
                showStatus(`Post saved to: ${data.saved_to}`, 'success');
            }
            
        } else {
            showStatus(data.error || 'Failed to generate post.', 'error');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showStatus('An error occurred while generating the post.', 'error');
    } finally {
        setLoadingState(false);
    }
});

// Display the generated post
function displayPost(data) {
    const { post_text, platform, topic, tone, char_count, char_limit } = data;
    
    // Create post content HTML
    const postHTML = `
        <div class="bg-gray-50 rounded-lg p-6 border-l-4 border-purple-500">
            <div class="flex items-center justify-between mb-4">
                <div class="flex items-center">
                    <i class="fas fa-${getPlatformIcon(platform)} text-2xl text-purple-600 mr-3"></i>
                    <div>
                        <h4 class="text-lg font-semibold text-gray-800">${platform}</h4>
                        <p class="text-sm text-gray-600">${topic} • ${tone}</p>
                    </div>
                </div>
                <div class="text-right">
                    <div class="text-sm text-gray-600">Character Count</div>
                    <div class="text-lg font-bold ${char_count <= char_limit ? 'text-green-600' : 'text-red-600'}">
                        ${char_count}/${char_limit}
                    </div>
                </div>
            </div>
            
            <div class="bg-white rounded-lg p-4 border">
                <p class="text-gray-800 text-lg leading-relaxed whitespace-pre-wrap">${post_text}</p>
            </div>
            
            <div class="mt-4 flex items-center text-sm text-gray-600">
                <i class="fas fa-info-circle mr-2"></i>
                <span>${char_count <= char_limit ? '✅ Within character limit' : '⚠️ Exceeds character limit'}</span>
            </div>
        </div>
    `;
    
    postContent.innerHTML = postHTML;
    
            // Show results section with animation
        resultsSection.classList.remove('hidden');
        resultsSection.classList.add('fade-in-up');
        
        // Show character count display with animation
        charCountDisplay.classList.remove('hidden');
        charCountDisplay.classList.add('slide-in-right');
        charCountText.textContent = `${char_count} / ${char_limit} characters`;
        
        // Update character count indicator styling
        const charCountIndicator = document.getElementById('charCountIndicator');
        charCountIndicator.className = 'char-count-indicator';
        
        if (char_count <= char_limit) {
            charCountIndicator.classList.add('success');
        } else if (char_count <= char_limit + 50) {
            charCountIndicator.classList.add('warning');
        } else {
            charCountIndicator.classList.add('danger');
        }
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Get platform icon
function getPlatformIcon(platform) {
    const icons = {
        'Twitter': 'twitter',
        'Facebook': 'facebook',
        'Instagram': 'instagram',
        'LinkedIn': 'linkedin',
        'TikTok': 'music',
        'YouTube': 'youtube'
    };
    return icons[platform] || 'globe';
}

// Copy post to clipboard
async function copyToClipboard() {
    if (!currentPost) {
        showStatus('No post to copy.', 'error');
        return;
    }
    
    try {
        await navigator.clipboard.writeText(currentPost.post_text);
        showStatus('Post copied to clipboard!', 'success');
        
        // Visual feedback
        const copyBtn = document.getElementById('copyBtn');
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = '<i class="fas fa-check mr-2"></i>Copied!';
        copyBtn.classList.add('bg-green-600');
        
        setTimeout(() => {
            copyBtn.innerHTML = originalText;
            copyBtn.classList.remove('bg-green-600');
        }, 2000);
        
    } catch (error) {
        console.error('Failed to copy:', error);
        showStatus('Failed to copy to clipboard. Please copy manually.', 'error');
    }
}

// Save post to file
async function savePost() {
    if (!currentPost) {
        showStatus('No post to save.', 'error');
        return;
    }
    
    try {
        const response = await fetch('/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(currentPost)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showStatus(data.message, 'success');
            
            // Visual feedback
            const saveBtn = document.getElementById('saveBtn');
            const originalText = saveBtn.innerHTML;
            saveBtn.innerHTML = '<i class="fas fa-check mr-2"></i>Saved!';
            saveBtn.classList.add('bg-green-600');
            
            setTimeout(() => {
                saveBtn.innerHTML = originalText;
                saveBtn.classList.remove('bg-green-600');
            }, 2000);
            
        } else {
            showStatus(data.error || 'Failed to save post.', 'error');
        }
        
    } catch (error) {
        console.error('Error saving post:', error);
        showStatus('An error occurred while saving the post.', 'error');
    }
}

// Reset form and hide results
function resetForm() {
    postForm.reset();
    resultsSection.classList.add('hidden');
    charCountDisplay.classList.add('hidden');
    statusMessage.classList.add('hidden');
    
    // Hide edit section
    const editSection = document.getElementById('editSection');
    if (editSection) {
        editSection.classList.add('hidden');
    }
    
    // Reset edit-related variables
    currentPost = null;
    originalPostText = null;
    
    // Show action buttons again
    const actionButtons = document.querySelector('.flex.flex-wrap.gap-4');
    if (actionButtons) {
        actionButtons.style.opacity = '1';
        actionButtons.style.pointerEvents = 'auto';
    }
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Set loading state
function setLoadingState(loading) {
    if (loading) {
        generateBtn.disabled = true;
        generateBtnText.textContent = 'Generating...';
        loadingSpinner.classList.remove('hidden');
        generateBtn.classList.add('opacity-75');
    } else {
        generateBtn.disabled = false;
        generateBtnText.textContent = 'Generate Post';
        loadingSpinner.classList.add('hidden');
        generateBtn.classList.remove('opacity-75');
    }
}

// Show status message
function showStatus(message, type = 'info') {
    const statusDiv = document.getElementById('statusMessage');
    
    // Set message and styling based on type
    statusDiv.textContent = message;
    statusDiv.className = `mt-4 p-4 rounded-lg ${getStatusClasses(type)}`;
    
    // Show the message
    statusDiv.classList.remove('hidden');
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        statusDiv.classList.add('hidden');
    }, 5000);
}

// Get status message styling classes
function getStatusClasses(type) {
    switch (type) {
        case 'success':
            return 'status-message success';
        case 'error':
            return 'status-message error';
        case 'warning':
            return 'status-message warning';
        default:
            return 'status-message';
    }
}

// Platform change handler to show character limit
document.getElementById('platform').addEventListener('change', function() {
    const platform = this.value;
    const charLimit = getCharacterLimit(platform);
    
    // Update character limit display if results are shown
    if (charCountDisplay && !charCountDisplay.classList.contains('hidden')) {
        const currentCharCount = currentPost ? currentPost.post_text.length : 0;
        charCountText.textContent = `${currentCharCount} / ${charLimit} characters`;
    }
});

// Get character limit for platform
function getCharacterLimit(platform) {
    const limits = {
        'Twitter': 280,
        'Facebook': 63206,
        'Instagram': 2200,
        'LinkedIn': 3000,
        'TikTok': 150,
        'YouTube': 5000
    };
    return limits[platform] || 280;
}

// Edit post functionality
function editPost() {
    if (!currentPost) {
        showStatus('No post to edit.', 'error');
        return;
    }
    
    // Store original text if not already stored
    if (!originalPostText) {
        originalPostText = currentPost.post_text;
    }
    
    // Show edit section
    const editSection = document.getElementById('editSection');
    const editablePost = document.getElementById('editablePost');
    const editCharCount = document.getElementById('editCharCount');
    
    // Populate textarea with current post text
    editablePost.value = currentPost.post_text;
    
    // Update character count
    updateEditCharCount();
    
    // Show edit section with animation
    editSection.classList.remove('hidden');
    editSection.classList.add('edit-section');
    
    // Focus on textarea
    editablePost.focus();
    
    // Hide action buttons temporarily
    document.querySelector('.flex.flex-wrap.gap-4').style.opacity = '0.5';
    document.querySelector('.flex.flex-wrap.gap-4').style.pointerEvents = 'none';
    
    // Show status
    showStatus('Edit mode activated. Make your changes and click "Save Changes" when done.', 'info');
}

// Save edit changes
function saveEdit() {
    const editablePost = document.getElementById('editablePost');
    const editSection = document.getElementById('editSection');
    const newText = editablePost.value.trim();
    
    if (!newText) {
        showStatus('Post content cannot be empty.', 'error');
        return;
    }
    
    // Update current post data
    currentPost.post_text = newText;
    
    // Update the displayed post
    displayPost({
        post_text: newText,
        platform: currentPost.platform,
        topic: currentPost.topic,
        tone: currentPost.tone,
        char_count: newText.length,
        char_limit: getCharacterLimit(currentPost.platform)
    });
    
    // Hide edit section
    editSection.classList.add('hidden');
    
    // Show action buttons again
    document.querySelector('.flex.flex-wrap.gap-4').style.opacity = '1';
    document.querySelector('.flex.flex-wrap.gap-4').style.pointerEvents = 'auto';
    
    // Show success message
    showStatus('Post updated successfully!', 'success');
}

// Cancel edit
function cancelEdit() {
    const editSection = document.getElementById('editSection');
    const editablePost = document.getElementById('editablePost');
    
    // Restore original text
    if (originalPostText) {
        currentPost.post_text = originalPostText;
        editablePost.value = originalPostText;
    }
    
    // Hide edit section
    editSection.classList.add('hidden');
    
    // Show action buttons again
    document.querySelector('.flex.flex-wrap.gap-4').style.opacity = '1';
    document.querySelector('.flex.flex-wrap.gap-4').style.pointerEvents = 'auto';
    
    // Show status
    showStatus('Edit cancelled. Original post restored.', 'warning');
}

// Update character count in edit mode
function updateEditCharCount() {
    const editablePost = document.getElementById('editablePost');
    const editCharCount = document.getElementById('editCharCount');
    const charLimit = getCharacterLimit(currentPost.platform);
    
    if (editablePost && editCharCount) {
        const currentCount = editablePost.value.length;
        editCharCount.textContent = `${currentCount}/${charLimit}`;
        
        // Update color based on character count
        if (currentCount <= charLimit) {
            editCharCount.className = 'text-sm text-green-600 font-medium';
        } else if (currentCount <= charLimit + 50) {
            editCharCount.className = 'text-sm text-yellow-600 font-medium';
        } else {
            editCharCount.className = 'text-sm text-red-600 font-medium';
        }
    }
}

// Initialize tooltips and other UI enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Add hover effects to form elements
    const formElements = document.querySelectorAll('input, select, textarea');
    formElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.parentElement.classList.add('ring-2', 'ring-purple-200');
        });
        
        element.addEventListener('blur', function() {
            this.parentElement.classList.remove('ring-2', 'ring-purple-200');
        });
    });
    
    // Add real-time character counting for edit mode
    const editablePost = document.getElementById('editablePost');
    if (editablePost) {
        editablePost.addEventListener('input', updateEditCharCount);
    }
});
