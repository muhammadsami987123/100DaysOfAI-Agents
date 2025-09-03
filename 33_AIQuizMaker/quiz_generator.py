#!/usr/bin/env python3
"""
Core Quiz Generator Module for AI Quiz Maker

This module handles the OpenAI API integration and quiz generation logic.
It provides methods to generate quizzes from topics, text files, or pasted content.
"""

import json
import os
import re
from typing import Dict, List, Optional, Any, Tuple
import openai
from config import get_api_key, get_quiz_prompt_template, get_quiz_validation_prompt, OPENAI_MODEL

class QuizGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the QuizGenerator with OpenAI API key."""
        self.api_key = api_key or get_api_key()
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = OPENAI_MODEL
        
    def generate_quiz(self, 
                     content: str,
                     num_questions: int = 5,
                     difficulty: str = "medium",
                     include_answers: bool = True,
                     validate: bool = True) -> Dict[str, Any]:
        """
        Generate a quiz from the given content.
        
        Args:
            content: Topic, text, or content to generate quiz from
            num_questions: Number of questions to generate
            difficulty: Difficulty level (easy, medium, hard)
            include_answers: Whether to include answer key
            validate: Whether to validate the generated quiz
            
        Returns:
            Dictionary containing the quiz data
        """
        try:
            # Prepare the prompt
            prompt = get_quiz_prompt_template().format(
                num_questions=num_questions,
                content=content,
                difficulty=difficulty
            )
            
            # Generate quiz using OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert quiz creator."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            quiz_content = response.choices[0].message.content.strip()
            
            # Debug: Print the raw response
            print(f"🔍 Raw AI Response:")
            print(quiz_content)
            print("-" * 50)
            
            # Parse the quiz content
            parsed_quiz = self._parse_quiz_content(quiz_content, num_questions)
            
            # Debug: Print parsed quiz
            print(f"🔍 Parsed Quiz:")
            print(f"Expected questions: {num_questions}")
            print(f"Parsed questions: {len(parsed_quiz)}")
            for i, q in enumerate(parsed_quiz):
                print(f"Q{i+1}: {q.get('question', 'NO QUESTION')}")
                print(f"Options: {q.get('options', {})}")
                print(f"Answer: {q.get('answer', 'NO ANSWER')}")
            print("-" * 50)
            
            # Validate if requested
            if validate:
                validation_result = self._validate_quiz(parsed_quiz, num_questions, difficulty)
                if not validation_result["valid"]:
                    # Try to regenerate with corrected prompt
                    corrected_quiz = self._regenerate_quiz(content, num_questions, difficulty, validation_result["issues"])
                    parsed_quiz = self._parse_quiz_content(corrected_quiz, num_questions)
            
            # Prepare the result
            result = {
                "topic": self._extract_topic(content),
                "difficulty": difficulty,
                "questions": num_questions,
                "quiz": parsed_quiz,
                "generated_at": self._get_timestamp(),
                "model": self.model,
                "include_answers": include_answers
            }
            
            return result
            
        except Exception as e:
            raise Exception(f"Failed to generate quiz: {str(e)}")
    
    def _parse_quiz_content(self, content: str, expected_questions: int) -> List[Dict[str, Any]]:
        """Parse the raw quiz content into structured format."""
        questions = []
        
        # Split content into lines and process
        lines = content.strip().split('\n')
        current_question = None
        current_options = {}
        current_answer = None
        
        print(f"🔍 Parsing {len(lines)} lines...")
        for i, line in enumerate(lines):
            print(f"🔍 Line {i+1}: '{line}'")
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this is a new question (starts with number)
            if re.match(r'^\d+\.', line):
                # Save previous question if exists
                if current_question and current_options:
                    questions.append({
                        "question": current_question,
                        "options": current_options,
                        "answer": current_answer
                    })
                
                # Start new question
                current_question = line.split('.', 1)[1].strip()
                current_options = {}
                current_answer = None
                
            # Check if this is an option (starts with A, B, C, D, possibly with leading spaces)
            elif re.match(r'^\s*[A-D]\)', line):
                option_letter = line.strip()[0]
                option_text = line.split(')', 1)[1].strip()
                current_options[option_letter] = option_text
                
            # Check if this is an answer line
            elif line.lower().startswith('answer:'):
                if current_question and current_options:
                    answer = line.split(':', 1)[1].strip().upper()
                    current_answer = answer
        
        # Add the last question if exists
        if current_question and current_options:
            questions.append({
                "question": current_question,
                "options": current_options,
                "answer": current_answer
            })
        
        # If we couldn't parse properly, try alternative parsing
        if len(questions) != expected_questions:
            questions = self._alternative_parse(content, expected_questions)
        
        return questions
    
    def _alternative_parse(self, content: str, expected_questions: int) -> List[Dict[str, Any]]:
        """Alternative parsing method for different quiz formats."""
        questions = []
        
        # Try to find questions using regex patterns
        question_pattern = r'(\d+\.\s*[^A-D]+?)(?=\d+\.|$)'
        option_pattern = r'\s*([A-D])\)\s*([^A-D]+?)(?=\s*[A-D]\)|$)'
        answer_pattern = r'Answer:\s*([A-D])'
        
        # Extract questions
        question_matches = re.findall(question_pattern, content, re.DOTALL)
        option_matches = re.findall(option_pattern, content, re.DOTALL)
        answer_matches = re.findall(answer_pattern, content, re.IGNORECASE)
        
        for i, question_text in enumerate(question_matches[:expected_questions]):
            question = {
                "question": question_text.strip(),
                "options": {},
                "answer": answer_matches[i] if i < len(answer_matches) else None
            }
            
            # Extract options for this question
            start_idx = content.find(question_text)
            end_idx = content.find(f"{i+2}.", start_idx) if i+2 <= len(question_matches) else len(content)
            question_section = content[start_idx:end_idx]
            
            for option_letter, option_text in option_matches:
                if option_text.strip() in question_section:
                    question["options"][option_letter] = option_text.strip()
            
            questions.append(question)
        
        return questions
    
    def _validate_quiz(self, quiz: List[Dict[str, Any]], expected_questions: int, difficulty: str) -> Dict[str, Any]:
        """Validate the generated quiz."""
        issues = []
        
        # Check number of questions
        if len(quiz) != expected_questions:
            issues.append(f"Expected {expected_questions} questions, got {len(quiz)}")
        
        # Validate each question
        for i, question in enumerate(quiz):
            if not question.get("question"):
                issues.append(f"Question {i+1} has no text")
            
            options = question.get("options", {})
            if len(options) != 4:
                issues.append(f"Question {i+1} has {len(options)} options instead of 4")
            
            if not question.get("answer"):
                issues.append(f"Question {i+1} has no answer")
            elif question["answer"] not in options:
                issues.append(f"Question {i+1} answer '{question['answer']}' not found in options")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
    
    def _regenerate_quiz(self, content: str, num_questions: int, difficulty: str, issues: List[str]) -> str:
        """Regenerate quiz with corrections based on validation issues."""
        correction_prompt = f"""
        The previous quiz generation had these issues:
        {chr(10).join(f"- {issue}" for issue in issues)}
        
        Please regenerate the quiz for:
        Topic: {content}
        Questions: {num_questions}
        Difficulty: {difficulty}
        
        Ensure all requirements are met this time.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert quiz creator. Fix the previous issues."},
                {"role": "user", "content": correction_prompt}
            ],
            temperature=0.5,
            max_tokens=2000
        )
        
        return response.choices[0].message.content.strip()
    
    def _extract_topic(self, content: str) -> str:
        """Extract a topic from the content."""
        if len(content) <= 100:
            return content
        
        # Try to extract first sentence or first few words
        lines = content.split('\n')
        first_line = lines[0].strip()
        
        if len(first_line) <= 100:
            return first_line
        
        # Take first 50 characters and add ellipsis
        return first_line[:50] + "..."
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def export_quiz(self, quiz_data: Dict[str, Any], format_type: str = "md") -> str:
        """Export quiz in the specified format."""
        if format_type == "md":
            return self._export_markdown(quiz_data)
        elif format_type == "json":
            return self._export_json(quiz_data)
        elif format_type == "csv":
            return self._export_csv(quiz_data)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _export_markdown(self, quiz_data: Dict[str, Any]) -> str:
        """Export quiz as Markdown."""
        md = f"# Quiz: {quiz_data['topic']}\n\n"
        md += f"**Difficulty**: {quiz_data['difficulty'].title()}\n"
        md += f"**Questions**: {quiz_data['questions']}\n"
        md += f"**Generated**: {quiz_data['generated_at']}\n\n"
        md += "---\n\n"
        
        for i, question in enumerate(quiz_data['quiz'], 1):
            md += f"{i}. **{question['question']}**\n"
            
            for option, text in question['options'].items():
                md += f"   {option}) {text}\n"
            
            if quiz_data.get('include_answers', True):
                md += f"   \n   **Answer**: {question['answer']}\n"
            
            md += "\n"
        
        return md
    
    def _export_json(self, quiz_data: Dict[str, Any]) -> str:
        """Export quiz as JSON."""
        return json.dumps(quiz_data, indent=2, ensure_ascii=False)
    
    def _export_csv(self, quiz_data: Dict[str, Any]) -> str:
        """Export quiz as CSV."""
        csv_lines = ["Question,Option A,Option B,Option C,Option D,Answer"]
        
        for question in quiz_data['quiz']:
            options = question['options']
            row = [
                f'"{question["question"]}"',
                f'"{options.get("A", "")}"',
                f'"{options.get("B", "")}"',
                f'"{options.get("C", "")}"',
                f'"{options.get("D", "")}"',
                question['answer']
            ]
            csv_lines.append(','.join(row))
        
        return '\n'.join(csv_lines)
    
    def save_quiz(self, quiz_data: Dict[str, Any], filename: str, format_type: str = "md") -> str:
        """Save quiz to file and return the file path."""
        from config import OUTPUTS_DIR
        
        # Ensure file has proper extension
        if not filename.endswith(f'.{format_type}'):
            filename += f'.{format_type}'
        
        filepath = os.path.join(OUTPUTS_DIR, filename)
        
        content = self.export_quiz(quiz_data, format_type)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath
    
    def generate_quiz_from_file(self, filepath: str, **kwargs) -> Dict[str, Any]:
        """Generate quiz from a text file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self.generate_quiz(content, **kwargs)
            
        except Exception as e:
            raise Exception(f"Failed to read file {filepath}: {str(e)}")
    
    def get_quiz_statistics(self, quiz_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get statistics about the generated quiz."""
        questions = quiz_data['quiz']
        
        # Count questions by difficulty indicators
        easy_indicators = ['basic', 'simple', 'fundamental', 'introductory']
        hard_indicators = ['advanced', 'complex', 'expert', 'sophisticated']
        
        easy_count = sum(1 for q in questions if any(indicator in q['question'].lower() for indicator in easy_indicators))
        hard_count = sum(1 for q in questions if any(indicator in q['question'].lower() for indicator in hard_indicators))
        medium_count = len(questions) - easy_count - hard_count
        
        return {
            "total_questions": len(questions),
            "estimated_difficulty_distribution": {
                "easy": easy_count,
                "medium": medium_count,
                "hard": hard_count
            },
            "average_question_length": sum(len(q['question']) for q in questions) / len(questions),
            "generation_time": quiz_data.get('generated_at'),
            "model_used": quiz_data.get('model')
        }
