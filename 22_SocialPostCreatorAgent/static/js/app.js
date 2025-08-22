// Global variables to store current post data
let currentPost = null;

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
    currentPost = null;
    
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
});
