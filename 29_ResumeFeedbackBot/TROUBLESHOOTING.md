# 🔧 Troubleshooting Guide

This guide covers common issues and their solutions for the ResumeFeedbackBot application.

## 🚨 Quick Fixes

### Application Won't Start

**Problem**: `ModuleNotFoundError: No module named 'openai'`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Problem**: `Port 5000 is already in use`
```bash
# Solution: Use different port
python server.py --port 5001
# Or kill the process using port 5000
netstat -ano | findstr :5000  # Windows
lsof -i :5000  # macOS/Linux
```

**Problem**: `Permission denied` errors
```bash
# Solution: Create directories and set permissions
mkdir uploads outputs logs
chmod 755 uploads outputs logs  # Linux/macOS
```

## 🔑 API Key Issues

### OpenAI API Key Problems

**Error**: `openai.AuthenticationError: Invalid API key`
```bash
# Solution: Check your API key
# 1. Verify the key in your .env file
# 2. Make sure there are no extra spaces
# 3. Check if the key is valid at https://platform.openai.com/api-keys
```

**Error**: `openai.RateLimitError: Rate limit exceeded`
```python
# Solution: Implement retry logic or upgrade plan
# Add to your code:
import time
import random

def api_call_with_retry():
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Your API call here
            return response
        except openai.RateLimitError:
            if attempt < max_retries - 1:
                time.sleep(random.uniform(1, 5))
                continue
            raise
```

**Error**: `openai.InvalidRequestError: Request too large`
```python
# Solution: Reduce input size
# 1. Check file size (max 16MB)
# 2. Reduce text content
# 3. Use a smaller model
```

## 📁 File Upload Issues

### File Format Problems

**Error**: `Unsupported file format`
```bash
# Supported formats: PDF, DOCX, DOC
# Convert other formats:
# - RTF: Use LibreOffice or online converters
# - TXT: Convert to PDF or DOCX
# - Images: Extract text first, then convert
```

**Error**: `File too large`
```python
# Solution: Reduce file size
# 1. Compress images in the document
# 2. Remove unnecessary content
# 3. Increase limit in config.py:
MAX_CONTENT_LENGTH = 33554432  # 32MB
```

**Error**: `File upload failed`
```bash
# Solution: Check permissions and disk space
# 1. Ensure uploads/ directory exists
# 2. Check write permissions
# 3. Verify disk space
df -h  # Linux/macOS
dir  # Windows
```

### File Processing Issues

**Error**: `PyPDF2.PdfReadError: File is not a PDF`
```python
# Solution: Check file integrity
# 1. Try opening the PDF in a reader
# 2. Re-save the PDF
# 3. Use a different PDF library:
pip install pdfplumber
```

**Error**: `docx.opc.exceptions.PackageNotFoundError`
```python
# Solution: Check DOCX file
# 1. Verify file is not corrupted
# 2. Try opening in Word/LibreOffice
# 3. Re-save the document
```

## 🌐 Network Issues

### Connection Problems

**Error**: `Connection timeout`
```bash
# Solution: Check network and firewall
# 1. Test internet connection
# 2. Check firewall settings
# 3. Try different network
# 4. Use VPN if needed
```

**Error**: `SSL Certificate error`
```bash
# Solution: Update certificates
# 1. Update Python and pip
# 2. Update system certificates
# 3. Check system time
# 4. Use --trusted-host if needed
```

**Error**: `DNS resolution failed`
```bash
# Solution: Check DNS settings
# 1. Try different DNS servers
# 2. Check /etc/hosts file
# 3. Use IP address instead of domain
```

## 💾 Memory and Performance Issues

### Memory Problems

**Error**: `MemoryError` or `OutOfMemoryError`
```python
# Solution: Optimize memory usage
# 1. Process files in chunks
# 2. Reduce batch sizes
# 3. Close file handles properly
# 4. Use generators for large files
```

**Error**: `Process killed by system`
```bash
# Solution: Reduce resource usage
# 1. Close other applications
# 2. Reduce file size limits
# 3. Use smaller models
# 4. Add swap space (Linux)
```

### Performance Issues

**Problem**: Slow analysis
```python
# Solution: Optimize performance
# 1. Use caching
# 2. Implement async processing
# 3. Use smaller models for initial analysis
# 4. Add progress indicators
```

**Problem**: High CPU usage
```python
# Solution: Optimize processing
# 1. Use multiprocessing for large files
# 2. Implement timeouts
# 3. Add rate limiting
# 4. Use background tasks
```

## 🐛 Application Errors

### Flask Errors

**Error**: `TemplateNotFound`
```bash
# Solution: Check file structure
# 1. Verify templates/ directory exists
# 2. Check file permissions
# 3. Ensure correct file paths
```

**Error**: `Static files not found`
```bash
# Solution: Check static files
# 1. Verify static/ directory exists
# 2. Check file permissions
# 3. Clear browser cache
```

**Error**: `CSRF token missing`
```python
# Solution: Add CSRF protection
# 1. Install Flask-WTF
# 2. Configure CSRF tokens
# 3. Add to forms
```

### Database Errors

**Error**: `Database connection failed`
```bash
# Solution: Check database
# 1. Verify database is running
# 2. Check connection string
# 3. Verify credentials
# 4. Check network connectivity
```

## 🔒 Security Issues

### Authentication Problems

**Error**: `Invalid credentials`
```bash
# Solution: Check authentication
# 1. Verify API keys
# 2. Check environment variables
# 3. Ensure proper permissions
```

**Error**: `Rate limit exceeded`
```python
# Solution: Implement rate limiting
# 1. Add delays between requests
# 2. Use exponential backoff
# 3. Implement request queuing
```

### File Security

**Error**: `Suspicious file detected`
```python
# Solution: Improve file validation
# 1. Add file type checking
# 2. Implement virus scanning
# 3. Use secure file handling
```

## 📱 Mobile/Responsive Issues

### Mobile Problems

**Problem**: Interface not responsive
```css
/* Solution: Check CSS */
/* 1. Verify viewport meta tag */
/* 2. Check media queries */
/* 3. Test on different devices */
```

**Problem**: Touch interactions not working
```javascript
// Solution: Add touch support
// 1. Add touch event listeners
// 2. Implement touch gestures
// 3. Test on mobile devices
```

## 🔍 Debugging Tips

### Enable Debug Mode

```python
# Add to your .env file
FLASK_DEBUG=True
DEBUG=True
```

### Check Logs

```bash
# View application logs
tail -f logs/app.log

# Check system logs
journalctl -u your-service -f  # Linux
```

### Use Debugger

```python
# Add breakpoints in your code
import pdb; pdb.set_trace()

# Or use IPython debugger
import ipdb; ipdb.set_trace()
```

### Monitor Resources

```bash
# Check system resources
htop  # Linux/macOS
top   # All systems
```

## 🚀 Performance Optimization

### Caching

```python
# Add Redis caching
pip install redis
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'redis'})
```

### Async Processing

```python
# Use Celery for background tasks
pip install celery
from celery import Celery

celery = Celery('resumebot')
```

### Database Optimization

```sql
-- Add indexes for better performance
CREATE INDEX idx_filename ON uploads(filename);
CREATE INDEX idx_created_at ON uploads(created_at);
```

## 📞 Getting Help

### Before Asking for Help

1. **Check this guide** for your specific error
2. **Search existing issues** on GitHub
3. **Check the logs** for detailed error messages
4. **Try the quick fixes** above
5. **Test with minimal setup**

### When Creating an Issue

Include the following information:

```markdown
**Environment:**
- OS: [Windows/macOS/Linux]
- Python version: [3.8/3.9/3.10/3.11]
- Flask version: [2.3.3]
- OpenAI version: [1.6.0]

**Error:**
- Full error message
- Stack trace
- Steps to reproduce

**Additional Info:**
- File size and format
- Network conditions
- System resources
```

### Useful Commands

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check system resources
free -h  # Linux
vm_stat  # macOS
wmic computersystem get TotalPhysicalMemory  # Windows

# Check network connectivity
ping api.openai.com
curl -I https://api.openai.com

# Check file permissions
ls -la uploads/ outputs/ logs/
```

## 🔄 Common Workarounds

### Temporary Solutions

1. **API Rate Limits**: Use multiple API keys
2. **File Size Limits**: Split large files
3. **Memory Issues**: Process files in chunks
4. **Network Issues**: Use local caching
5. **Performance Issues**: Use background processing

### Alternative Approaches

1. **Different Models**: Use GPT-3.5-turbo instead of GPT-4
2. **File Formats**: Convert to simpler formats
3. **Processing**: Use external services
4. **Storage**: Use cloud storage
5. **Deployment**: Use containerization

---

**Remember**: Most issues can be resolved by checking the logs, verifying configuration, and ensuring proper setup. When in doubt, start with a minimal configuration and add complexity gradually.
