from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import json
from datetime import datetime
from typing import List, Optional
import logging

from memory_store import MemoryStore
from ai_service import AIService
from voice_service import VoiceService
from models import MemoryType, MemoryPriority, ExportFormat
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize services
memory_store = MemoryStore()
ai_service = AIService()
voice_service = VoiceService()

# Ensure directories exist
Config.create_directories()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/memories', methods=['GET'])
def get_memories():
    """Get all memories with optional filtering"""
    try:
        # Get query parameters
        query = request.args.get('query', '')
        tags = request.args.get('tags', '')
        category = request.args.get('category', '')
        memory_type = request.args.get('memory_type', '')
        limit = int(request.args.get('limit', 50))
        
        # Parse tags
        tag_list = [tag.strip() for tag in tags.split(",")] if tags else None
        
        # Parse memory type
        memory_type_enum = MemoryType(memory_type) if memory_type else None
        
        if query:
            # Search memories
            results = memory_store.search_memories(
                query=query,
                limit=limit,
                tags=tag_list,
                category=category if category else None,
                memory_type=memory_type_enum
            )
            memories = [result.memory.dict() for result in results]
        else:
            # Get recent memories
            memories = [m.dict() for m in memory_store.get_recent_memories(limit)]
        
        return jsonify({
            'success': True,
            'memories': memories,
            'count': len(memories)
        })
        
    except Exception as e:
        logger.error(f"Error getting memories: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/memories', methods=['POST'])
def create_memory():
    """Create a new memory"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'content' not in data:
            return jsonify({
                'success': False,
                'error': 'Content is required'
            }), 400
        
        # Get memory data
        content = data['content']
        memory_type = data.get('memory_type', 'long_term')
        tags = data.get('tags', [])
        category = data.get('category')
        priority = data.get('priority', 'medium')
        expires_in = data.get('expires_in_hours')
        
        # Use AI enhancement if available
        if ai_service.is_available() and data.get('use_ai_enhancement', True):
            ai_enhancement = ai_service.enhance_memory_content(content)
            if ai_enhancement.get('enhanced'):
                suggestions = ai_enhancement['suggestions']
                
                # Handle tags - ensure it's a list
                ai_tags = suggestions.get('tags', tags)
                if isinstance(ai_tags, str):
                    # If AI returned tags as a string, split by comma
                    tags = [tag.strip() for tag in ai_tags.split(',') if tag.strip()]
                elif isinstance(ai_tags, list):
                    tags = ai_tags
                else:
                    tags = tags  # Keep original tags
                
                category = suggestions.get('category', category)
                priority = suggestions.get('priority', priority)
                memory_type = suggestions.get('memory_type', memory_type)
        
        # Create memory
        memory = memory_store.add_memory(
            content=content,
            memory_type=memory_type,
            tags=tags,
            category=category,
            priority=priority,
            expires_in_hours=expires_in
        )
        
        return jsonify({
            'success': True,
            'memory': memory.dict(),
            'message': 'Memory created successfully'
        })
        
    except Exception as e:
        logger.error(f"Error creating memory: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/memories/<memory_id>', methods=['GET'])
def get_memory(memory_id):
    """Get a specific memory by ID"""
    try:
        memory = memory_store.get_memory(memory_id)
        if not memory:
            return jsonify({
                'success': False,
                'error': 'Memory not found'
            }), 404
        
        return jsonify({
            'success': True,
            'memory': memory.dict()
        })
        
    except Exception as e:
        logger.error(f"Error getting memory: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/memories/<memory_id>', methods=['PUT'])
def update_memory(memory_id):
    """Update a memory"""
    try:
        data = request.get_json()
        
        # Update memory
        updated_memory = memory_store.update_memory(memory_id, **data)
        if not updated_memory:
            return jsonify({
                'success': False,
                'error': 'Memory not found'
            }), 404
        
        return jsonify({
            'success': True,
            'memory': updated_memory.dict(),
            'message': 'Memory updated successfully'
        })
        
    except Exception as e:
        logger.error(f"Error updating memory: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/memories/<memory_id>', methods=['DELETE'])
def delete_memory(memory_id):
    """Delete a memory"""
    try:
        success = memory_store.delete_memory(memory_id)
        if not success:
            return jsonify({
                'success': False,
                'error': 'Memory not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Memory deleted successfully'
        })
        
    except Exception as e:
        logger.error(f"Error deleting memory: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/memories/search', methods=['POST'])
def search_memories():
    """Search memories with AI enhancement"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query is required'
            }), 400
        
        # AI search enhancement
        search_enhancement = None
        if ai_service.is_available():
            search_enhancement = ai_service.enhance_search_query(query)
        
        # Perform search
        results = memory_store.search_memories(query, limit=20)
        memories = [result.memory.dict() for result in results]
        
        return jsonify({
            'success': True,
            'memories': memories,
            'count': len(memories),
            'search_enhancement': search_enhancement
        })
        
    except Exception as e:
        logger.error(f"Error searching memories: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/memories/tags/<tag>', methods=['GET'])
def get_memories_by_tag(tag):
    """Get memories by tag"""
    try:
        memories = memory_store.get_memories_by_tag(tag)
        memories_data = [m.dict() for m in memories]
        
        return jsonify({
            'success': True,
            'memories': memories_data,
            'count': len(memories_data),
            'tag': tag
        })
        
    except Exception as e:
        logger.error(f"Error getting memories by tag: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/memories/category/<category>', methods=['GET'])
def get_memories_by_category(category):
    """Get memories by category"""
    try:
        memories = memory_store.get_memories_by_category(category)
        memories_data = [m.dict() for m in memories]
        
        return jsonify({
            'success': True,
            'memories': memories_data,
            'count': len(memories_data),
            'category': category
        })
        
    except Exception as e:
        logger.error(f"Error getting memories by category: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/memories/recent', methods=['GET'])
def get_recent_memories():
    """Get recent memories"""
    try:
        limit = int(request.args.get('limit', 10))
        memories = memory_store.get_recent_memories(limit)
        memories_data = [m.dict() for m in memories]
        
        return jsonify({
            'success': True,
            'memories': memories_data,
            'count': len(memories_data)
        })
        
    except Exception as e:
        logger.error(f"Error getting recent memories: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/memories/frequent', methods=['GET'])
def get_frequent_memories():
    """Get frequently accessed memories"""
    try:
        limit = int(request.args.get('limit', 10))
        memories = memory_store.get_frequently_accessed(limit)
        memories_data = [m.dict() for m in memories]
        
        return jsonify({
            'success': True,
            'memories': memories_data,
            'count': len(memories_data)
        })
        
    except Exception as e:
        logger.error(f"Error getting frequent memories: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get memory statistics"""
    try:
        stats = memory_store.get_stats()
        
        return jsonify({
            'success': True,
            'statistics': {
                'total_memories': stats.total_memories,
                'short_term_count': stats.short_term_count,
                'long_term_count': stats.long_term_count,
                'expired_count': stats.expired_count,
                'total_tags': stats.total_tags,
                'most_used_tags': stats.most_used_tags,
                'storage_size_mb': stats.storage_size_mb
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export', methods=['POST'])
def export_memories():
    """Export memories in various formats"""
    try:
        data = request.get_json()
        format_type = data.get('format', 'json')
        tags = data.get('tags', [])
        category = data.get('category')
        
        # Export memories
        export_data = memory_store.export_memories(
            format_type=format_type,
            tags=tags if tags else None,
            category=category if category else None
        )
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"memories_export_{timestamp}.{format_type}"
        filepath = os.path.join(Config.EXPORT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(export_data)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': filepath,
            'message': 'Memories exported successfully'
        })
        
    except Exception as e:
        logger.error(f"Error exporting memories: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export/download/<filename>', methods=['GET'])
def download_export(filename):
    """Download exported file"""
    try:
        filepath = os.path.join(Config.EXPORT_DIR, filename)
        if not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
        
        return send_file(filepath, as_attachment=True)
        
    except Exception as e:
        logger.error(f"Error downloading export: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ai/enhance', methods=['POST'])
def enhance_memory():
    """Get AI enhancement suggestions for memory content"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        
        if not content:
            return jsonify({
                'success': False,
                'error': 'Content is required'
            }), 400
        
        if not ai_service.is_available():
            return jsonify({
                'success': False,
                'error': 'AI service not available'
            }), 503
        
        # Get AI enhancement
        enhancement = ai_service.enhance_memory_content(content)
        
        return jsonify({
            'success': True,
            'enhancement': enhancement
        })
        
    except Exception as e:
        logger.error(f"Error enhancing memory: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ai/suggest-tags', methods=['POST'])
def suggest_tags():
    """Get AI-suggested tags for content"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        
        if not content:
            return jsonify({
                'success': False,
                'error': 'Content is required'
            }), 400
        
        if not ai_service.is_available():
            return jsonify({
                'success': False,
                'error': 'AI service not available'
            }), 503
        
        # Get tag suggestions
        tags = ai_service.suggest_tags(content)
        
        return jsonify({
            'success': True,
            'tags': tags
        })
        
    except Exception as e:
        logger.error(f"Error suggesting tags: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/voice/status', methods=['GET'])
def get_voice_status():
    """Get voice service status"""
    try:
        status = voice_service.get_voice_status()
        
        return jsonify({
            'success': True,
            'status': status
        })
        
    except Exception as e:
        logger.error(f"Error getting voice status: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/voice/test', methods=['POST'])
def test_voice():
    """Test voice input and output"""
    try:
        test_result = voice_service.test_voice()
        
        return jsonify({
            'success': True,
            'test_result': test_result
        })
        
    except Exception as e:
        logger.error(f"Error testing voice: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/voice/speak', methods=['POST'])
def speak_text():
    """Convert text to speech"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'Text is required'
            }), 400
        
        # Speak text
        voice_service.speak(text, block=False)
        
        return jsonify({
            'success': True,
            'message': 'Text spoken successfully'
        })
        
    except Exception as e:
        logger.error(f"Error speaking text: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cleanup', methods=['POST'])
def cleanup_memories():
    """Clean up expired memories"""
    try:
        # Get stats before cleanup
        stats_before = memory_store.get_stats()
        
        # Cleanup is handled automatically in the memory store
        # Just trigger a manual cleanup check
        memory_store._cleanup_expired_memories()
        
        # Get stats after cleanup
        stats_after = memory_store.get_stats()
        
        cleaned_count = stats_before.total_memories - stats_after.total_memories
        
        return jsonify({
            'success': True,
            'cleaned_count': cleaned_count,
            'stats_before': {
                'total_memories': stats_before.total_memories
            },
            'stats_after': {
                'total_memories': stats_after.total_memories
            },
            'message': f'Cleanup completed. {cleaned_count} memories cleaned up.'
        })
        
    except Exception as e:
        logger.error(f"Error cleaning up memories: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Check if services are working
        memory_count = len(memory_store.memories)
        ai_available = ai_service.is_available()
        voice_available = voice_service.tts_engine is not None
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'services': {
                'memory_store': True,
                'ai_service': ai_available,
                'voice_service': voice_available
            },
            'memory_count': memory_count,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
