# 🤝 Contributing to ResumeFeedbackBot

Thank you for your interest in contributing to ResumeFeedbackBot! This guide will help you get started with development and contributing to the project.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Feature Development](#feature-development)
- [Bug Reports](#bug-reports)
- [Documentation](#documentation)

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- OpenAI API key (for testing)
- Basic knowledge of Flask, Python, and web development

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/29_ResumeFeedbackBot.git
   cd 29_ResumeFeedbackBot
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/muhammadsami987123/29_ResumeFeedbackBot.git
   ```

## 🔧 Development Setup

### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### 3. Environment Configuration

```bash
# Copy environment template
cp env.example .env

# Edit .env file with your settings
# At minimum, add your OpenAI API key
OPENAI_API_KEY=your_api_key_here
```

### 4. Create Required Directories

```bash
# Create necessary directories
mkdir -p uploads outputs logs static/css static/js
```

### 5. Run Development Server

```bash
# Start development server
python server.py

# Or with debug mode
FLASK_DEBUG=True python server.py
```

## 📝 Code Style

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- **Line length**: 88 characters (Black default)
- **Indentation**: 4 spaces
- **String quotes**: Double quotes for docstrings, single quotes for strings
- **Import order**: Standard library, third-party, local imports

### Code Formatting

We use [Black](https://black.readthedocs.io/) for code formatting:

```bash
# Format all Python files
black .

# Check formatting without changes
black --check .
```

### Linting

We use [Flake8](https://flake8.pycqa.org/) for linting:

```bash
# Run linter
flake8 .

# Run with specific configuration
flake8 --config .flake8 .
```

### Type Hints

We encourage the use of type hints:

```python
from typing import Dict, List, Optional, Union

def analyze_resume(file_path: str, target_role: Optional[str] = None) -> Dict[str, Union[str, float, List[str]]]:
    """Analyze a resume file and return results."""
    pass
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=.

# Run specific test file
python -m pytest tests/test_resume_analyzer.py

# Run with verbose output
python -m pytest -v
```

### Writing Tests

Create tests in the `tests/` directory:

```python
# tests/test_resume_analyzer.py
import pytest
from resume_analyzer import ResumeAnalyzer

class TestResumeAnalyzer:
    def test_extract_text_from_pdf(self):
        analyzer = ResumeAnalyzer()
        # Test implementation
        
    def test_analyze_resume(self):
        analyzer = ResumeAnalyzer()
        # Test implementation
```

### Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest configuration
├── test_resume_analyzer.py  # Resume analyzer tests
├── test_portfolio_analyzer.py  # Portfolio analyzer tests
├── test_chat_service.py     # Chat service tests
└── test_server.py           # Server endpoint tests
```

### Mocking External Services

```python
import pytest
from unittest.mock import patch, MagicMock

def test_openai_api_call():
    with patch('openai.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        # Test implementation
```

## 📤 Submitting Changes

### 1. Create a Feature Branch

```bash
# Create and switch to feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/your-bug-description
```

### 2. Make Your Changes

- Write your code following the style guide
- Add tests for new functionality
- Update documentation if needed
- Commit your changes with clear messages

### 3. Commit Messages

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Examples:
```
feat(analyzer): add support for RTF files
fix(server): resolve memory leak in file upload
docs(readme): update installation instructions
test(analyzer): add unit tests for PDF parsing
```

### 4. Push and Create Pull Request

```bash
# Push your branch
git push origin feature/your-feature-name

# Create pull request on GitHub
```

### 5. Pull Request Guidelines

- **Title**: Clear and descriptive
- **Description**: Explain what and why, not how
- **Tests**: Ensure all tests pass
- **Documentation**: Update docs if needed
- **Screenshots**: For UI changes

## 🚀 Feature Development

### Adding New Features

1. **Create an issue** describing the feature
2. **Discuss the approach** with maintainers
3. **Implement the feature** following the guidelines
4. **Add tests** for the new functionality
5. **Update documentation** if needed

### Feature Checklist

- [ ] Feature is well-documented
- [ ] Tests are written and passing
- [ ] Code follows style guidelines
- [ ] Error handling is implemented
- [ ] Performance is considered
- [ ] Security implications are addressed

### Example: Adding New File Format Support

```python
# 1. Update resume_analyzer.py
def extract_text_from_rtf(self, file_path: str) -> str:
    """Extract text from RTF file."""
    # Implementation here
    pass

# 2. Update extract_text_from_file method
def extract_text_from_file(self, file_path: str) -> str:
    file_extension = file_path.lower().split('.')[-1]
    
    if file_extension == 'pdf':
        return self.extract_text_from_pdf(file_path)
    elif file_extension in ['docx', 'doc']:
        return self.extract_text_from_docx(file_path)
    elif file_extension == 'rtf':
        return self.extract_text_from_rtf(file_path)  # New format
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")

# 3. Add tests
def test_extract_text_from_rtf(self):
    analyzer = ResumeAnalyzer()
    # Test implementation

# 4. Update documentation
# Add RTF to supported formats list
```

## 🐛 Bug Reports

### Before Reporting

1. **Check existing issues** for similar problems
2. **Try the troubleshooting guide** in TROUBLESHOOTING.md
3. **Test with minimal setup** to isolate the issue
4. **Check the logs** for error details

### Bug Report Template

```markdown
**Bug Description**
Clear and concise description of the bug.

**Steps to Reproduce**
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

**Expected Behavior**
What you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g., Windows 10, macOS 12.0, Ubuntu 20.04]
- Python: [e.g., 3.9.7]
- Flask: [e.g., 2.3.3]
- OpenAI: [e.g., 1.6.0]

**Additional Context**
- Screenshots if applicable
- Error logs
- File formats/sizes involved
```

## 📚 Documentation

### Code Documentation

- **Docstrings**: Use Google style docstrings
- **Comments**: Explain why, not what
- **Type hints**: Use them consistently

```python
def analyze_resume_with_context(
    resume_text: str, 
    target_role: Optional[str] = None,
    industry: Optional[str] = None
) -> Dict[str, Any]:
    """Analyze resume with optional context.
    
    Args:
        resume_text: The text content of the resume
        target_role: Optional target job role for analysis
        industry: Optional industry context
        
    Returns:
        Dictionary containing analysis results with keys:
        - overall_score: float
        - scores: Dict[str, float]
        - strengths: List[str]
        - weaknesses: List[str]
        - suggestions: List[str]
        
    Raises:
        ValueError: If resume_text is empty
        OpenAIError: If API call fails
    """
    pass
```

### README Updates

When adding features, update:
- Feature list in README.md
- Installation instructions if needed
- Configuration options
- Usage examples

### API Documentation

For new API endpoints:
- Add to README.md API section
- Include request/response examples
- Document error codes
- Add to OpenAPI/Swagger if implemented

## 🔧 Development Tools

### Pre-commit Hooks

Install pre-commit hooks for automatic formatting:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### VS Code Configuration

Create `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "editor.formatOnSave": true,
    "python.testing.pytestEnabled": true
}
```

### Docker Development

```dockerfile
# Dockerfile.dev
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt requirements-dev.txt ./
RUN pip install -r requirements.txt -r requirements-dev.txt

COPY . .
EXPOSE 5000

CMD ["python", "server.py"]
```

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow project conventions

### Communication

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Pull Requests**: Keep them focused and well-documented

### Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## 📞 Getting Help

### Resources

- **Documentation**: README.md and TROUBLESHOOTING.md
- **Issues**: Check existing GitHub issues
- **Discussions**: GitHub Discussions for questions
- **Code**: Review existing code for examples

### Contact

- **Maintainer**: [Your Name]
- **Email**: [Your Email]
- **GitHub**: [Your GitHub Profile]

---

**Thank you for contributing to ResumeFeedbackBot!** 🎉

Your contributions help make this project better for everyone in the career development community.
