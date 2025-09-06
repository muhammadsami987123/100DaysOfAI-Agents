// StoryWriterAgent - Stories Management JavaScript

class StoriesManager {
    constructor() {
        this.stories = [];
        this.favorites = [];
        this.currentFilter = 'all';
        this.currentView = 'grid';
        this.init();
    }

    async init() {
        await this.loadStories();
        this.setupEventListeners();
        this.updateStats();
    }

    setupEventListeners() {
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => this.handleSearch(e.target.value));
        }

        // Filter buttons
        const filterBtns = document.querySelectorAll('.filter-btn');
        filterBtns.forEach(btn => {
            btn.addEventListener('click', (e) => this.handleFilter(e.target.dataset.filter));
        });

        // View controls
        const viewBtns = document.querySelectorAll('.view-btn');
        viewBtns.forEach(btn => {
            btn.addEventListener('click', (e) => this.handleViewChange(e.target.dataset.view));
        });

        // Story actions
        document.addEventListener('click', (e) => {
            if (e.target.closest('.favorite-btn')) {
                this.handleFavoriteToggle(e.target.closest('.favorite-btn'));
            } else if (e.target.closest('.download-btn')) {
                this.handleDownload(e.target.closest('.download-btn'));
            } else if (e.target.closest('.delete-btn')) {
                this.handleDelete(e.target.closest('.delete-btn'));
            } else if (e.target.closest('.read-more-btn')) {
                this.handleReadMore(e.target.closest('.read-more-btn'));
            }
        });

        // Modal controls
        const modal = document.getElementById('storyModal');
        const closeModal = document.getElementById('closeModal');
        const modalClose = document.getElementById('modalClose');

        if (closeModal) {
            closeModal.addEventListener('click', () => this.closeModal());
        }
        if (modalClose) {
            modalClose.addEventListener('click', () => this.closeModal());
        }
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal();
                }
            });
        }

        // Modal actions
        const modalFavorite = document.getElementById('modalFavorite');
        const modalDownload = document.getElementById('modalDownload');

        if (modalFavorite) {
            modalFavorite.addEventListener('click', () => this.handleModalFavorite());
        }
        if (modalDownload) {
            modalDownload.addEventListener('click', () => this.handleModalDownload());
        }
    }

    async loadStories() {
        try {
            const response = await fetch('/api/stories');
            const result = await response.json();

            if (result.success) {
                this.stories = result.stories;
                this.renderStories();
            } else {
                throw new Error(result.error || 'Failed to load stories');
            }

            // Load favorites
            const favResponse = await fetch('/api/favorites');
            const favResult = await favResponse.json();

            if (favResult.success) {
                this.favorites = favResult.favorites.map(f => f.id);
            }

        } catch (error) {
            console.error('Error loading stories:', error);
            this.showToast(`Error loading stories: ${error.message}`, 'error');
        }
    }

    renderStories() {
        const storiesGrid = document.getElementById('storiesGrid');
        const emptyState = document.getElementById('emptyState');

        if (!storiesGrid) return;

        // Filter stories based on current filter
        let filteredStories = this.stories;

        if (this.currentFilter === 'favorites') {
            filteredStories = this.stories.filter(story => this.favorites.includes(story.id));
        } else if (this.currentFilter === 'recent') {
            // Show stories from last 7 days
            const weekAgo = new Date();
            weekAgo.setDate(weekAgo.getDate() - 7);
            filteredStories = this.stories.filter(story => 
                new Date(story.created_at) > weekAgo
            );
        }

        if (filteredStories.length === 0) {
            storiesGrid.style.display = 'none';
            if (emptyState) {
                emptyState.style.display = 'block';
            }
            return;
        }

        storiesGrid.style.display = 'grid';
        if (emptyState) {
            emptyState.style.display = 'none';
        }

        // Render stories
        storiesGrid.innerHTML = filteredStories.map(story => this.createStoryCard(story)).join('');

        // Update stats
        this.updateStats();
    }

    createStoryCard(story) {
        const isFavorited = this.favorites.includes(story.id);
        const createdDate = new Date(story.created_at).toLocaleDateString();

        return `
            <div class="story-card" data-story-id="${story.id}" data-genre="${story.genre}" data-tone="${story.tone}">
                <div class="story-card-header">
                    <h3 class="story-title">${story.title}</h3>
                    <div class="story-actions">
                        <button class="action-btn favorite-btn ${isFavorited ? 'favorited' : ''}" data-story-id="${story.id}" title="Toggle Favorite">
                            <i class="fas fa-heart"></i>
                        </button>
                        <button class="action-btn download-btn" data-story-id="${story.id}" title="Download">
                            <i class="fas fa-download"></i>
                        </button>
                        <button class="action-btn delete-btn" data-story-id="${story.id}" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
                
                <div class="story-meta">
                    <span class="meta-tag genre">${story.genre}</span>
                    <span class="meta-tag tone">${story.tone}</span>
                    <span class="meta-tag length">${story.length}</span>
                    <span class="meta-tag language">${story.language}</span>
                </div>
                
                <div class="story-preview">
                    ${story.content.substring(0, 200)}${story.content.length > 200 ? '...' : ''}
                </div>
                
                <div class="story-footer">
                    <div class="story-stats">
                        <span><i class="fas fa-words"></i> ${story.word_count} words</span>
                        <span><i class="fas fa-calendar"></i> ${createdDate}</span>
                    </div>
                    <button class="read-more-btn" data-story-id="${story.id}">Read More</button>
                </div>
            </div>
        `;
    }

    handleSearch(query) {
        if (!query.trim()) {
            this.renderStories();
            return;
        }

        // Filter stories by search query
        const filteredStories = this.stories.filter(story => 
            story.title.toLowerCase().includes(query.toLowerCase()) ||
            story.content.toLowerCase().includes(query.toLowerCase()) ||
            story.prompt.toLowerCase().includes(query.toLowerCase())
        );

        this.renderFilteredStories(filteredStories);
    }

    renderFilteredStories(stories) {
        const storiesGrid = document.getElementById('storiesGrid');
        const emptyState = document.getElementById('emptyState');

        if (!storiesGrid) return;

        if (stories.length === 0) {
            storiesGrid.style.display = 'none';
            if (emptyState) {
                emptyState.style.display = 'block';
            }
            return;
        }

        storiesGrid.style.display = 'grid';
        if (emptyState) {
            emptyState.style.display = 'none';
        }

        storiesGrid.innerHTML = stories.map(story => this.createStoryCard(story)).join('');
    }

    handleFilter(filter) {
        this.currentFilter = filter;

        // Update filter button states
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-filter="${filter}"]`).classList.add('active');

        // Clear search
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.value = '';
        }

        this.renderStories();
    }

    handleViewChange(view) {
        this.currentView = view;

        // Update view button states
        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-view="${view}"]`).classList.add('active');

        // Update grid layout
        const storiesGrid = document.getElementById('storiesGrid');
        if (storiesGrid) {
            if (view === 'list') {
                storiesGrid.style.gridTemplateColumns = '1fr';
            } else {
                storiesGrid.style.gridTemplateColumns = 'repeat(auto-fill, minmax(350px, 1fr))';
            }
        }
    }

    async handleFavoriteToggle(btn) {
        const storyId = btn.dataset.storyId;
        const isFavorited = btn.classList.contains('favorited');

        try {
            const response = await fetch(`/api/favorites/${storyId}`, {
                method: isFavorited ? 'DELETE' : 'POST'
            });

            const result = await response.json();

            if (result.success) {
                if (isFavorited) {
                    btn.classList.remove('favorited');
                    this.favorites = this.favorites.filter(id => id !== storyId);
                    this.showToast('Removed from favorites', 'success');
                } else {
                    btn.classList.add('favorited');
                    this.favorites.push(storyId);
                    this.showToast('Added to favorites', 'success');
                }
                this.updateStats();
            } else {
                throw new Error(result.error || 'Failed to toggle favorite');
            }

        } catch (error) {
            console.error('Error toggling favorite:', error);
            this.showToast(`Error: ${error.message}`, 'error');
        }
    }

    async handleDownload(btn) {
        const storyId = btn.dataset.storyId;

        try {
            const response = await fetch(`/api/download/${storyId}?format=txt`);
            
            if (response.ok) {
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `story_${storyId}.txt`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);

                this.showToast('Story downloaded!', 'success');
            } else {
                throw new Error('Failed to download story');
            }

        } catch (error) {
            console.error('Error downloading story:', error);
            this.showToast(`Error: ${error.message}`, 'error');
        }
    }

    async handleDelete(btn) {
        const storyId = btn.dataset.storyId;
        const storyTitle = btn.closest('.story-card').querySelector('.story-title').textContent;

        if (!confirm(`Are you sure you want to delete "${storyTitle}"? This action cannot be undone.`)) {
            return;
        }

        try {
            const response = await fetch(`/api/stories/${storyId}`, {
                method: 'DELETE'
            });

            const result = await response.json();

            if (result.success) {
                // Remove from local arrays
                this.stories = this.stories.filter(story => story.id !== storyId);
                this.favorites = this.favorites.filter(id => id !== storyId);

                // Re-render
                this.renderStories();
                this.updateStats();

                this.showToast('Story deleted successfully', 'success');
            } else {
                throw new Error(result.error || 'Failed to delete story');
            }

        } catch (error) {
            console.error('Error deleting story:', error);
            this.showToast(`Error: ${error.message}`, 'error');
        }
    }

    async handleReadMore(btn) {
        const storyId = btn.dataset.storyId;
        const story = this.stories.find(s => s.id === storyId);

        if (!story) {
            this.showToast('Story not found', 'error');
            return;
        }

        this.showModal(story);
    }

    showModal(story) {
        const modal = document.getElementById('storyModal');
        const modalTitle = document.getElementById('modalTitle');
        const modalMeta = document.getElementById('modalMeta');
        const modalContent = document.getElementById('modalContent');
        const modalFavorite = document.getElementById('modalFavorite');

        if (!modal) return;

        // Update modal content
        modalTitle.textContent = story.title;
        modalMeta.innerHTML = `
            <span class="meta-tag genre">${story.genre}</span>
            <span class="meta-tag tone">${story.tone}</span>
            <span class="meta-tag length">${story.length}</span>
            <span class="meta-tag language">${story.language}</span>
        `;
        modalContent.textContent = story.content;

        // Update favorite button
        const isFavorited = this.favorites.includes(story.id);
        modalFavorite.innerHTML = `<i class="fas fa-heart"></i> ${isFavorited ? 'Remove from' : 'Add to'} Favorites`;
        modalFavorite.dataset.storyId = story.id;

        // Show modal
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }

    closeModal() {
        const modal = document.getElementById('storyModal');
        if (modal) {
            modal.classList.remove('show');
            document.body.style.overflow = '';
        }
    }

    async handleModalFavorite() {
        const btn = document.getElementById('modalFavorite');
        const storyId = btn.dataset.storyId;
        const isFavorited = this.favorites.includes(storyId);

        try {
            const response = await fetch(`/api/favorites/${storyId}`, {
                method: isFavorited ? 'DELETE' : 'POST'
            });

            const result = await response.json();

            if (result.success) {
                if (isFavorited) {
                    this.favorites = this.favorites.filter(id => id !== storyId);
                    btn.innerHTML = '<i class="fas fa-heart"></i> Add to Favorites';
                    this.showToast('Removed from favorites', 'success');
                } else {
                    this.favorites.push(storyId);
                    btn.innerHTML = '<i class="fas fa-heart"></i> Remove from Favorites';
                    this.showToast('Added to favorites', 'success');
                }
                this.updateStats();
            } else {
                throw new Error(result.error || 'Failed to toggle favorite');
            }

        } catch (error) {
            console.error('Error toggling favorite:', error);
            this.showToast(`Error: ${error.message}`, 'error');
        }
    }

    async handleModalDownload() {
        const btn = document.getElementById('modalDownload');
        const storyId = btn.dataset.storyId;

        try {
            const response = await fetch(`/api/download/${storyId}?format=txt`);
            
            if (response.ok) {
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `story_${storyId}.txt`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);

                this.showToast('Story downloaded!', 'success');
            } else {
                throw new Error('Failed to download story');
            }

        } catch (error) {
            console.error('Error downloading story:', error);
            this.showToast(`Error: ${error.message}`, 'error');
        }
    }

    updateStats() {
        const totalStories = document.getElementById('totalStories');
        const totalFavorites = document.getElementById('totalFavorites');
        const totalWords = document.getElementById('totalWords');

        if (totalStories) {
            totalStories.textContent = this.stories.length;
        }
        if (totalFavorites) {
            totalFavorites.textContent = this.favorites.length;
        }
        if (totalWords) {
            const wordCount = this.stories.reduce((sum, story) => sum + (story.word_count || 0), 0);
            totalWords.textContent = wordCount.toLocaleString();
        }
    }

    showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        if (!toast) return;

        toast.textContent = message;
        toast.className = `toast ${type}`;
        toast.classList.add('show');

        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
}

// Initialize stories manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new StoriesManager();
});
