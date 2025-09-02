"""
AI Assistant module for SystemMonitorAgent
Provides optimization suggestions based on system metrics
"""
import os
import openai
from typing import Dict, Any, Optional
from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_MAX_TOKENS
from utils import Colors, print_section

class AIAssistant:
    """AI-powered system optimization assistant"""
    
    def __init__(self):
        self.api_key = OPENAI_API_KEY
        self.model = OPENAI_MODEL
        self.max_tokens = OPENAI_MAX_TOKENS
        self.is_available = bool(self.api_key)
        
        if self.is_available:
            try:
                openai.api_key = self.api_key
                # Test the API connection
                openai.Model.list()
            except Exception as e:
                print(f"{Colors.WARNING}Warning: OpenAI API connection failed: {e}{Colors.RESET}")
                self.is_available = False
    
    def get_optimization_suggestions(self, stats: Dict[str, Any]) -> Optional[str]:
        """Get AI-generated optimization suggestions based on system stats"""
        if not self.is_available:
            return None
        
        try:
            # Extract key metrics
            cpu_usage = stats.get('cpu', {}).get('usage_percent', 0)
            memory_usage = stats.get('memory', {}).get('usage_percent', 0)
            disk_usage = stats.get('disk', {}).get('usage_percent', 0)
            
            # Create prompt for AI
            prompt = self._create_optimization_prompt(cpu_usage, memory_usage, disk_usage)
            
            # Get AI response
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a system optimization expert. Provide concise, actionable advice for improving system performance based on the metrics provided. Focus on practical steps that users can implement immediately."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"{Colors.ERROR}Error getting AI suggestions: {e}{Colors.RESET}")
            return None
    
    def _create_optimization_prompt(self, cpu_usage: float, memory_usage: float, disk_usage: float) -> str:
        """Create a prompt for the AI based on current system metrics"""
        prompt = f"""
My system is currently showing the following resource usage:
- CPU Usage: {cpu_usage:.1f}%
- Memory Usage: {memory_usage:.1f}%
- Disk Usage: {disk_usage:.1f}%

Please provide 3-5 specific, actionable suggestions to optimize my system performance. Focus on:
1. Immediate actions I can take
2. Software recommendations if relevant
3. System configuration tips
4. Process management advice

Keep suggestions concise and practical for a developer/sysadmin user.
"""
        return prompt
    
    def display_suggestions(self, stats: Dict[str, Any]):
        """Display AI-generated optimization suggestions"""
        if not self.is_available:
            print(f"{Colors.WARNING}AI Assistant not available. Set OPENAI_API_KEY environment variable to enable.{Colors.RESET}")
            return
        
        print_section("🤖 AI Optimization Suggestions")
        print(f"{Colors.INFO}Analyzing system metrics...{Colors.RESET}")
        
        suggestions = self.get_optimization_suggestions(stats)
        
        if suggestions:
            print(f"\n{Colors.SUCCESS}💡 AI Recommendations:{Colors.RESET}")
            print(f"{Colors.PROCESS}{suggestions}{Colors.RESET}")
        else:
            print(f"{Colors.WARNING}Unable to generate AI suggestions at this time.{Colors.RESET}")
        
        print(f"\n{Colors.INFO}Note: These are AI-generated suggestions. Always verify before implementing.{Colors.RESET}")
    
    def get_system_health_score(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        """Get AI-generated system health score and analysis"""
        if not self.is_available:
            return {'error': 'AI Assistant not available'}
        
        try:
            # Extract metrics
            cpu_usage = stats.get('cpu', {}).get('usage_percent', 0)
            memory_usage = stats.get('memory', {}).get('usage_percent', 0)
            disk_usage = stats.get('disk', {}).get('usage_percent', 0)
            
            # Calculate basic health score (0-100)
            health_score = 100
            
            if cpu_usage > 90:
                health_score -= 30
            elif cpu_usage > 80:
                health_score -= 20
            elif cpu_usage > 70:
                health_score -= 10
            
            if memory_usage > 90:
                health_score -= 25
            elif memory_usage > 80:
                health_score -= 15
            elif memory_usage > 70:
                health_score -= 10
            
            if disk_usage > 90:
                health_score -= 20
            elif disk_usage > 80:
                health_score -= 10
            
            # Get AI analysis
            prompt = f"""
Based on these system metrics, provide a brief health assessment:
- CPU: {cpu_usage:.1f}%
- Memory: {memory_usage:.1f}%
- Disk: {disk_usage:.1f}%

Health Score: {health_score}/100

Give a 1-2 sentence assessment of system health and any immediate concerns.
"""
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a system health analyst. Provide brief, professional assessments of system health based on resource usage metrics."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=100,
                temperature=0.5
            )
            
            analysis = response.choices[0].message.content.strip()
            
            return {
                'health_score': health_score,
                'analysis': analysis,
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'disk_usage': disk_usage
            }
            
        except Exception as e:
            return {'error': f'Failed to get health score: {e}'}
    
    def display_health_score(self, stats: Dict[str, Any]):
        """Display AI-generated system health score"""
        if not self.is_available:
            print(f"{Colors.WARNING}AI Assistant not available for health scoring.{Colors.RESET}")
            return
        
        print_section("🏥 AI System Health Assessment")
        
        health_data = self.get_system_health_score(stats)
        
        if 'error' in health_data:
            print(f"{Colors.ERROR}Error: {health_data['error']}{Colors.RESET}")
            return
        
        # Display health score with color coding
        score = health_data['health_score']
        if score >= 80:
            score_color = Colors.SUCCESS
            status = "Excellent"
        elif score >= 60:
            score_color = Colors.WARNING
            status = "Good"
        elif score >= 40:
            score_color = Colors.WARNING
            status = "Fair"
        else:
            score_color = Colors.ERROR
            status = "Poor"
        
        print(f"Health Score: {score_color}{score}/100{Colors.RESET} ({status})")
        print(f"CPU Usage: {health_data['cpu_usage']:.1f}%")
        print(f"Memory Usage: {health_data['memory_usage']:.1f}%")
        print(f"Disk Usage: {health_data['disk_usage']:.1f}%")
        
        if health_data['analysis']:
            print(f"\n{Colors.INFO}AI Assessment:{Colors.RESET}")
            print(f"{Colors.PROCESS}{health_data['analysis']}{Colors.RESET}")
