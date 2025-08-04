"""
Core EmailAgent class for email generation using GPT
"""

import json
import openai
from typing import Dict, List, Optional, Any
from colorama import init, Fore, Back, Style
from config import EmailConfig

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class EmailAgent:
    def __init__(self, api_key: str):
        """Initialize EmailAgent with OpenAI API key"""
        self.api_key = api_key
        self.config = EmailConfig()
        self.email_history = []
        
    def _extract_recipient_name(self, recipient: str) -> str:
        """Extract recipient name from email or full name"""
        if not recipient:
            return "there"
        
        # If it's an email, try to extract name
        if '@' in recipient:
            name_part = recipient.split('@')[0]
            # Convert common email formats to names
            name_part = name_part.replace('.', ' ').replace('_', ' ').replace('-', ' ')
            name_part = ' '.join(word.capitalize() for word in name_part.split())
            return name_part if name_part and name_part != 'there' else "there"
        
        # If it's already a name, return as is
        return recipient
        
    def generate_email(self, 
                      prompt: str, 
                      template: str = "formal",
                      recipient: str = "",
                      sender: str = "",
                      signature: str = "",
                      tone: Optional[str] = None) -> Dict[str, str]:
        """
        Generate an email using GPT based on the prompt and template
        
        Args:
            prompt: Natural language description of what the email should contain
            template: Email template to use (formal, casual, follow_up, etc.)
            recipient: Recipient name/email
            sender: Sender name/email
            signature: Custom signature
            tone: Override template tone if specified
            
        Returns:
            Dictionary containing email components (subject, to, from, body)
        """
        try:
            # Get template configuration
            template_config = self.config.TEMPLATES.get(template, self.config.TEMPLATES["formal"])
            
            # Use custom tone if provided, otherwise use template tone
            email_tone = tone or template_config["tone"]
            
            # Set defaults and extract recipient name
            sender = sender or self.config.DEFAULT_FROM
            signature = signature or self.config.DEFAULT_SIGNATURE
            recipient_name = self._extract_recipient_name(recipient)
            
            # Create system prompt with improved instructions
            system_prompt = f"""You are an expert email writer. Generate a professional email based on the user's request.

Template: {template_config['name']} - {template_config['description']}
Tone: {email_tone}
Greeting: {template_config['greeting']}
Closing: {template_config['closing']}

IMPORTANT REQUIREMENTS:
- Write a compelling, specific subject line that captures the email's purpose
- Replace placeholder text like {{recipient}} with actual names when provided
- Include specific details, dates, times, and context from the user's request
- Make the email feel personalized and relevant to the specific situation
- Use natural, conversational language while maintaining professionalism
- Include specific action items, deadlines, or next steps when appropriate
- Craft a polished, professional sign-off that matches the email's purpose
- Format the email with proper line breaks and structure

PERSONALIZATION GUIDELINES:
- If recipient name is provided, use it naturally in the greeting
- Include specific details mentioned in the prompt (dates, times, locations, etc.)
- Reference specific events, projects, or contexts when relevant
- Make the email feel like it was written specifically for this situation

Return a JSON object with this structure:
{{
    "subject": "Specific, compelling subject line",
    "to": "recipient@example.com",
    "from": "{sender}",
    "body": "Complete email body with personalized greeting and closing"
}}"""

            # Create user prompt with enhanced context
            user_prompt = f"""Write a professional email about: {prompt}

CONTEXT:
- Recipient: {recipient if recipient else "Not specified"} (Name: {recipient_name})
- Sender: {sender}
- Signature: {signature}
- Template: {template_config['name']} ({template_config['description']})
- Tone: {email_tone}

INSTRUCTIONS:
- Extract specific details from the prompt (dates, times, locations, names, etc.)
- Create a compelling subject line that summarizes the email's purpose
- Write a personalized email that feels specific to this situation
- Use the recipient name "{recipient_name}" naturally in the greeting
- Include relevant details and context from the prompt
- Use natural language that flows well
- End with an appropriate, professional closing

Please generate a complete email with subject line and body."""

            # Call OpenAI API using the new client format
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=self.config.MAX_TOKENS,
                temperature=self.config.TEMPERATURE
            )
            
            # Parse response
            content = response.choices[0].message.content.strip()
            
            # Try to parse JSON response
            try:
                email_data = json.loads(content)
                # Ensure all required fields are present
                if "subject" not in email_data:
                    email_data["subject"] = "Email"
                if "to" not in email_data:
                    email_data["to"] = recipient or "recipient@example.com"
                if "from" not in email_data:
                    email_data["from"] = sender
                if "body" not in email_data:
                    email_data["body"] = content
            except json.JSONDecodeError:
                # If JSON parsing fails, create a structured response
                lines = content.split('\n')
                subject = lines[0].replace('Subject:', '').strip() if lines else "Email"
                body = '\n'.join(lines[1:]) if len(lines) > 1 else content
                
                email_data = {
                    "subject": subject,
                    "to": recipient or "recipient@example.com",
                    "from": sender,
                    "body": body
                }
            
            # Add to history
            self.email_history.append({
                "prompt": prompt,
                "template": template,
                "email": email_data,
                "timestamp": "now"  # You could add actual timestamp here
            })
            
            return email_data
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error generating email: {e}")
            return {
                "subject": "Error",
                "to": recipient or "recipient@example.com",
                "from": sender,
                "body": f"Error generating email: {e}"
            }
    
    def generate_quick_email(self, prompt: str) -> Dict[str, str]:
        """Generate a quick email with minimal parameters"""
        return self.generate_email(
            prompt=prompt,
            template="formal",
            recipient="",
            sender=self.config.DEFAULT_FROM,
            signature=self.config.DEFAULT_SIGNATURE
        )
    
    def get_templates(self) -> Dict[str, Dict[str, str]]:
        """Get available email templates"""
        return self.config.TEMPLATES
    
    def get_email_history(self) -> List[Dict[str, Any]]:
        """Get email generation history"""
        return self.email_history
    
    def run_terminal(self):
        """Run the terminal interface"""
        print(f"{Fore.CYAN}🤖 EmailWriterAgent - Terminal Mode")
        print(f"{Fore.YELLOW}Available commands:")
        print("  write <prompt> - Generate an email")
        print("  templates - Show available templates")
        print("  history - Show email history")
        print("  help - Show this help")
        print("  quit - Exit")
        print()
        
        while True:
            try:
                command = input(f"{Fore.GREEN}📧 EmailWriterAgent> ").strip()
                
                if not command:
                    continue
                    
                if command.lower() == "quit" or command.lower() == "exit":
                    print(f"{Fore.YELLOW}👋 Goodbye!")
                    break
                    
                elif command.lower() == "help":
                    self.show_terminal_help()
                    
                elif command.lower() == "templates":
                    self.show_templates()
                    
                elif command.lower() == "history":
                    self.show_history()
                    
                elif command.startswith("write "):
                    prompt = command[6:].strip()
                    if prompt:
                        self.generate_terminal_email(prompt)
                    else:
                        print(f"{Fore.RED}❌ Please provide a prompt for the email")
                        
                else:
                    print(f"{Fore.RED}❌ Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}👋 Goodbye!")
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Error: {e}")
    
    def generate_terminal_email(self, prompt: str):
        """Generate and display email in terminal"""
        print(f"{Fore.CYAN}📧 Generating email for: {prompt}")
        
        # Get template choice
        print(f"{Fore.YELLOW}Available templates:")
        templates = self.get_templates()
        for i, (key, template) in enumerate(templates.items(), 1):
            print(f"  {i}. {template['name']} - {template['description']}")
        
        try:
            choice = input(f"{Fore.GREEN}Select template (1-{len(templates)}) or press Enter for formal: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(templates):
                template_key = list(templates.keys())[int(choice) - 1]
            else:
                template_key = "formal"
        except:
            template_key = "formal"
        
        # Get recipient
        recipient = input(f"{Fore.GREEN}Recipient (optional): ").strip()
        
        # Generate email
        email = self.generate_email(
            prompt=prompt,
            template=template_key,
            recipient=recipient
        )
        
        # Display email
        print(f"\n{Fore.CYAN}" + "="*50)
        print(f"📧 GENERATED EMAIL")
        print("="*50)
        print(f"{Fore.YELLOW}Subject: {Fore.WHITE}{email['subject']}")
        print(f"{Fore.YELLOW}To: {Fore.WHITE}{email['to']}")
        print(f"{Fore.YELLOW}From: {Fore.WHITE}{email['from']}")
        print(f"{Fore.CYAN}" + "-" * 50)
        print(f"{Fore.WHITE}{email['body']}")
        print(f"{Fore.CYAN}" + "="*50)
        
        # Ask if user wants to save
        save = input(f"{Fore.GREEN}Save to file? (y/n): ").strip().lower()
        if save == 'y':
            self.save_email_to_file(email)
    
    def show_terminal_help(self):
        """Show terminal help"""
        print(f"{Fore.CYAN}🤖 EmailWriterAgent - Help")
        print(f"{Fore.YELLOW}Commands:")
        print("  write <prompt> - Generate an email with the given prompt")
        print("  templates - Show available email templates")
        print("  history - Show email generation history")
        print("  help - Show this help message")
        print("  quit/exit - Exit the application")
        print()
        print(f"{Fore.YELLOW}Examples:")
        print("  write meeting tomorrow at 2pm")
        print("  write thank you for the interview")
        print("  write follow up on project proposal")
    
    def show_templates(self):
        """Show available templates"""
        print(f"{Fore.CYAN}📧 Available Email Templates:")
        templates = self.get_templates()
        for key, template in templates.items():
            print(f"  {Fore.YELLOW}{key}: {Fore.WHITE}{template['name']}")
            print(f"    {Fore.GRAY}{template['description']}")
            print()
    
    def show_history(self):
        """Show email history"""
        if not self.email_history:
            print(f"{Fore.YELLOW}📧 No email history yet.")
            return
        
        print(f"{Fore.CYAN}📧 Email History:")
        for i, entry in enumerate(self.email_history[-5:], 1):  # Show last 5
            print(f"  {Fore.YELLOW}{i}. {Fore.WHITE}{entry['prompt'][:50]}...")
            print(f"    Template: {entry['template']}")
            print()
    
    def save_email_to_file(self, email: Dict[str, str]):
        """Save email to a text file"""
        try:
            filename = f"email_{len(self.email_history)}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Subject: {email['subject']}\n")
                f.write(f"To: {email['to']}\n")
                f.write(f"From: {email['from']}\n")
                f.write("-" * 50 + "\n")
                f.write(email['body'])
            
            print(f"{Fore.GREEN}✅ Email saved to {filename}")
        except Exception as e:
            print(f"{Fore.RED}❌ Error saving email: {e}") 