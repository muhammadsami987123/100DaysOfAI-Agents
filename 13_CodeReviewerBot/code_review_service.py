import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import openai
from openai import OpenAI

from config import (
    OPENAI_API_KEY, OPENAI_MODEL, MAX_TOKENS, TEMPERATURE,
    SUPPORTED_LANGUAGES, REVIEW_CATEGORIES, get_language_from_content,
    ERROR_MESSAGES
)


@dataclass
class CodeIssue:
    """Represents a code issue found during review."""
    category: str
    severity: str  # "low", "medium", "high", "critical"
    line_number: Optional[int]
    message: str
    suggestion: str
    code_snippet: Optional[str] = None


@dataclass
class CodeReviewResult:
    """Represents the complete result of a code review."""
    language: str
    issues: List[CodeIssue]
    suggestions: List[str]
    refactored_code: Optional[str]
    scores: Dict[str, float]
    summary: str
    total_issues: int
    critical_issues: int


class CodeReviewError(Exception):
    """Custom exception for code review errors."""
    pass


class CodeReviewService:
    """Service for AI-powered code review and analysis."""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise CodeReviewError(ERROR_MESSAGES["missing_api_key"])
        
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE
        
        # Check if the model supports JSON responses
        self.supports_json = self._check_json_support()

        # Hard safety cap to avoid accidental gigantic values from env
        try:
            self.max_tokens = max(1, min(int(self.max_tokens), 32000000))
        except Exception:
            self.max_tokens = 4000
    
    def _check_json_support(self) -> bool:
        """Check if the current model supports JSON response format."""
        # Only include models known to support the `response_format` parameter
        # with Chat Completions. Plain 'gpt-4' typically does NOT support it.
        json_supported_models = [
            'gpt-4-1106-preview',
            'gpt-3.5-turbo-1106',
            'gpt-4-turbo',
            'gpt-4-turbo-preview'
        ]

        model_name = (self.model or '').lower()
        supports_json = any(supported in model_name for supported in json_supported_models)
        
        # Debug logging
        print(f"🔍 Model check: '{self.model}' -> JSON support: {supports_json}")
        
        return supports_json
    
    def review_code(self, code: str, language: Optional[str] = None, 
                   ui_language: str = "english") -> CodeReviewResult:
        """
        Perform comprehensive code review using AI.
        
        Args:
            code: The source code to review
            language: Programming language (auto-detected if None)
            ui_language: Language for feedback (english, hindi, urdu)
        
        Returns:
            CodeReviewResult with detailed analysis
        """
        if not code or not code.strip():
            raise CodeReviewError(ERROR_MESSAGES["empty_code"])
        
        # Auto-detect language if not provided
        if not language:
            language = get_language_from_content(code)
        
        if language not in SUPPORTED_LANGUAGES:
            raise CodeReviewError(ERROR_MESSAGES["unsupported_language"])
        
        try:
            # Generate AI review
            review_data = self._generate_ai_review(code, language, ui_language)
            
            # Parse and structure the review
            issues = self._parse_issues(review_data.get("issues", []))
            suggestions = review_data.get("suggestions", [])
            refactored_code = review_data.get("refactored_code")
            scores = review_data.get("scores", {})
            summary = review_data.get("summary", "")
            
            # Calculate statistics
            total_issues = len(issues)
            critical_issues = len([issue for issue in issues if issue.severity == "critical"])
            
            return CodeReviewResult(
                language=language,
                issues=issues,
                suggestions=suggestions,
                refactored_code=refactored_code,
                scores=scores,
                summary=summary,
                total_issues=total_issues,
                critical_issues=critical_issues
            )
            
        except Exception as e:
            raise CodeReviewError(f"Code analysis failed: {str(e)}")
    
    def _generate_ai_review(self, code: str, language: str, ui_language: str) -> Dict[str, Any]:
        """Generate AI-powered code review using OpenAI."""
        
        # Create language-specific prompt
        language_config = SUPPORTED_LANGUAGES[language]
        best_practices = ", ".join(language_config["best_practices"])
        
        # Create UI language-specific instructions
        ui_instructions = self._get_ui_language_instructions(ui_language)
        
        prompt = f"""
You are an expert senior software engineer performing a comprehensive code review. 
Analyze the following {language} code and provide detailed feedback.

Language: {language}
Best Practices to Consider: {best_practices}

{ui_instructions}

Please provide your analysis in the following JSON format:
{{
    "issues": [
        {{
            "category": "syntax|best_practices|performance|security|readability",
            "severity": "low|medium|high|critical",
            "line_number": <line_number_or_null>,
            "message": "<detailed_issue_description>",
            "suggestion": "<specific_improvement_suggestion>",
            "code_snippet": "<relevant_code_snippet_if_applicable>"
        }}
    ],
    "suggestions": [
        "<general_improvement_suggestion_1>",
        "<general_improvement_suggestion_2>"
    ],
    "refactored_code": "<improved_version_of_the_code>",
    "scores": {{
        "readability": <score_0_to_10>,
        "code_quality": <score_0_to_10>,
        "performance": <score_0_to_10>,
        "best_practices": <score_0_to_10>,
        "security": <score_0_to_10>
    }},
    "summary": "<overall_assessment_and_recommendations>"
}}

Code to review:
```{language}
{code}
```

Focus on:
1. Syntax errors and formatting issues
2. Code quality and best practices
3. Performance optimization opportunities
4. Security vulnerabilities
5. Readability and maintainability
6. Language-specific conventions and idioms

Provide actionable, specific feedback that a developer can immediately implement.
"""

        try:
            # Dynamically size max_tokens based on model context window
            context_window = self._get_model_context_window(self.model)
            prompt_token_estimate = self._estimate_tokens(prompt)
            # Keep a safety buffer for the model/system overhead
            safety_buffer = 512
            available_for_completion = max(256, context_window - prompt_token_estimate - safety_buffer)
            max_completion_tokens = max(1, min(self.max_tokens, available_for_completion))

            # If the prompt itself is too large, return a friendly error
            if prompt_token_estimate + 256 + safety_buffer >= context_window:
                raise CodeReviewError(
                    "AI analysis failed: The provided code is too large for the selected model's context window. "
                    "Please reduce the code size (split into smaller parts) or switch to a model with a larger context window."
                )
            # First attempt: Try with response_format if supported
            if self.supports_json:
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": "You are an expert code reviewer with deep knowledge of multiple programming languages and best practices."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=max_completion_tokens,
                        temperature=self.temperature,
                        response_format={"type": "json_object"}
                    )
                    
                    content = response.choices[0].message.content
                    return json.loads(content)
                    
                except Exception as format_error:
                    print(f"⚠️  Response format failed, trying without: {format_error}")
                    # Fall through to try without response_format
            
            # Second attempt: Try without response_format
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer with deep knowledge of multiple programming languages and best practices."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_completion_tokens,
                temperature=self.temperature
            )
            
            content = response.choices[0].message.content
            
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                content = json_match.group()
                return json.loads(content)
            else:
                # If no JSON found, create a fallback response
                return self._create_fallback_response(content, language)
            
        except json.JSONDecodeError:
            raise CodeReviewError("Failed to parse AI response - the AI didn't return valid JSON format")
        except Exception as e:
            error_msg = str(e)
            # Friendlier error for context-length issues
            if 'maximum context length' in error_msg.lower() or 'context_length_exceeded' in error_msg.lower():
                raise CodeReviewError(
                    "AI analysis failed: The prompt exceeds the model's context window. "
                    "Please shorten the code or reduce the requested output."
                )
            if "response_format" in error_msg and "not supported" in error_msg:
                # This should not happen with our fallback mechanism, but just in case
                raise CodeReviewError(f"AI analysis failed: The model '{self.model}' doesn't support structured JSON responses. The application will try to work around this limitation.")
            elif "rate limit" in error_msg.lower():
                raise CodeReviewError("AI analysis failed: Rate limit exceeded. Please wait a moment and try again.")
            elif "quota" in error_msg.lower():
                raise CodeReviewError("AI analysis failed: API quota exceeded. Please check your OpenAI account.")
            else:
                raise CodeReviewError(f"AI analysis failed: {error_msg}")

    def _get_model_context_window(self, model: str) -> int:
        """Return an approximate context window for common models."""
        name = (model or '').lower()
        # Conservative defaults
        if '1106' in name or 'turbo' in name:
            return 128000
        if 'gpt-3.5-turbo-16k' in name:
            return 16000
        if 'gpt-3.5' in name:
            return 4096
        # Plain gpt-4 classic
        return 8192

    def _estimate_tokens(self, text: str) -> int:
        """Very rough token estimation without external deps (≈4 chars per token)."""
        if not text:
            return 0
        # Add small overhead for message structure
        return int(len(text) / 4) + 200
    
    def _create_fallback_response(self, content: str, language: str) -> Dict[str, Any]:
        """Create a fallback response when JSON parsing fails."""
        return {
            "issues": [
                {
                    "category": "best_practices",
                    "severity": "medium",
                    "line_number": None,
                    "message": "AI analysis completed but response format was unexpected. Please review the code manually.",
                    "suggestion": "The AI provided feedback but couldn't be parsed into structured format. Consider reviewing the raw response.",
                    "code_snippet": None
                }
            ],
            "suggestions": [
                "Review the code manually for best practices",
                "Check for syntax errors and formatting issues",
                "Consider code readability and maintainability"
            ],
            "refactored_code": None,
            "scores": {
                "readability": 5.0,
                "code_quality": 5.0,
                "performance": 5.0,
                "best_practices": 5.0,
                "security": 5.0
            },
            "summary": f"Code review completed for {language} code. The AI provided feedback but the response format was unexpected. Please review the code manually and consider the AI's suggestions."
        }
    
    def _get_ui_language_instructions(self, ui_language: str) -> str:
        """Get language-specific instructions for the AI."""
        if ui_language == "hindi":
            return """
Please provide all feedback in Hindi (हिंदी). 
Use simple, clear Hindi that is easy to understand for developers.
Translate technical terms appropriately while maintaining accuracy.
"""
        elif ui_language == "urdu":
            return """
Please provide all feedback in Urdu (اردو).
Use simple, clear Urdu that is easy to understand for developers.
Translate technical terms appropriately while maintaining accuracy.
"""
        else:
            return """
Please provide all feedback in clear, professional English.
Use technical terminology appropriately and provide specific, actionable advice.
"""
    
    def _parse_issues(self, issues_data: List[Dict[str, Any]]) -> List[CodeIssue]:
        """Parse issues from AI response into CodeIssue objects."""
        issues = []
        
        for issue_data in issues_data:
            try:
                issue = CodeIssue(
                    category=issue_data.get("category", "best_practices"),
                    severity=issue_data.get("severity", "medium"),
                    line_number=issue_data.get("line_number"),
                    message=issue_data.get("message", ""),
                    suggestion=issue_data.get("suggestion", ""),
                    code_snippet=issue_data.get("code_snippet")
                )
                issues.append(issue)
            except Exception:
                # Skip malformed issues
                continue
        
        return issues
    
    def get_language_info(self, language: str) -> Dict[str, Any]:
        """Get information about a supported programming language."""
        return SUPPORTED_LANGUAGES.get(language, {})
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported programming languages."""
        return list(SUPPORTED_LANGUAGES.keys())
    
    def validate_code_syntax(self, code: str, language: str) -> List[str]:
        """Basic syntax validation for supported languages."""
        errors = []
        
        if language == "python":
            errors = self._validate_python_syntax(code)
        elif language == "javascript":
            errors = self._validate_javascript_syntax(code)
        elif language == "java":
            errors = self._validate_java_syntax(code)
        # Add more language-specific validators as needed
        
        return errors
    
    def _validate_python_syntax(self, code: str) -> List[str]:
        """Basic Python syntax validation."""
        errors = []
        
        # Check for basic Python syntax issues
        lines = code.split('\n')
        indent_level = 0
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Skip empty lines and comments
            if not stripped or stripped.startswith('#'):
                continue
            
            # Check indentation
            if stripped.startswith(('def ', 'class ', 'if ', 'for ', 'while ', 'try:', 'except:', 'finally:', 'with ')):
                if not line.startswith(' ' * indent_level * 4):
                    errors.append(f"Line {i}: Incorrect indentation")
            
            # Check for common syntax errors
            if stripped.endswith(':'):
                indent_level += 1
            elif stripped.startswith(('return', 'break', 'continue', 'pass')):
                indent_level = max(0, indent_level - 1)
        
        return errors
    
    def _validate_javascript_syntax(self, code: str) -> List[str]:
        """Basic JavaScript syntax validation."""
        errors = []
        
        # Check for basic JavaScript syntax issues
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Skip empty lines and comments
            if not stripped or stripped.startswith('//') or stripped.startswith('/*'):
                continue
            
            # Check for missing semicolons (basic check)
            if (stripped and not stripped.endswith(';') and 
                not stripped.endswith('{') and not stripped.endswith('}') and
                not stripped.startswith('//') and not stripped.startswith('/*')):
                # This is a very basic check and might have false positives
                pass
        
        return errors
    
    def _validate_java_syntax(self, code: str) -> List[str]:
        """Basic Java syntax validation."""
        errors = []
        
        # Check for basic Java syntax issues
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Skip empty lines and comments
            if not stripped or stripped.startswith('//') or stripped.startswith('/*'):
                continue
            
            # Check for missing semicolons (basic check)
            if (stripped and not stripped.endswith(';') and 
                not stripped.endswith('{') and not stripped.endswith('}') and
                not stripped.startswith('//') and not stripped.startswith('/*')):
                # This is a very basic check and might have false positives
                pass
        
        return errors
    
    def generate_code_summary(self, code: str, language: str) -> Dict[str, Any]:
        """Generate a summary of the code structure and complexity."""
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        # Basic metrics
        total_lines = len(lines)
        code_lines = len(non_empty_lines)
        comment_lines = len([line for line in lines if line.strip().startswith(('#', '//', '/*', '*'))])
        
        # Language-specific analysis
        if language == "python":
            functions = len(re.findall(r'^\s*def\s+', code, re.MULTILINE))
            classes = len(re.findall(r'^\s*class\s+', code, re.MULTILINE))
            imports = len(re.findall(r'^\s*(import|from)\s+', code, re.MULTILINE))
        elif language == "javascript":
            functions = len(re.findall(r'function\s+\w+|const\s+\w+\s*=\s*\(|let\s+\w+\s*=\s*\(|var\s+\w+\s*=\s*\('), code)
            classes = len(re.findall(r'class\s+\w+', code))
            imports = len(re.findall(r'import\s+', code))
        else:
            functions = classes = imports = 0
        
        return {
            "total_lines": total_lines,
            "code_lines": code_lines,
            "comment_lines": comment_lines,
            "comment_ratio": comment_lines / max(code_lines, 1),
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "complexity": "low" if code_lines < 50 else "medium" if code_lines < 200 else "high"
        }
