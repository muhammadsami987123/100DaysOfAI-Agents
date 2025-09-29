import openai
from typing import List, Dict, Any
from config.openai_config import OpenAIConfig

class JsonChatbot:
    """Handles conversational interactions about JSON using OpenAI GPT"""

    def __init__(self, config: OpenAIConfig):
        self.config = config
        self.client = config.get_client()
        self.conversation_history: List[Dict[str, str]] = []
        self._initialize_history()

    def _initialize_history(self) -> None:
        """Initialize conversation history with a system prompt"""
        self.conversation_history.append({"role": "system", "content": self._get_system_prompt_chatbot()})

    def _get_system_prompt_chatbot(self) -> str:
        """System prompt for the conversational chatbot"""
        return """You are JSONHelperBot's conversational assistant. Your role is to help users with their JSON-related questions, guide them on best practices, and suggest commands they can use with JSONHelperBot. Keep responses concise, helpful, and developer-friendly. You can answer general JSON questions, provide code snippets, explain concepts, and suggest next steps. If a user asks for JSON parsing or explanation, suggest using the `paste`, `upload`, or `fetch` commands.

Guidelines:
1. Respond in a friendly and helpful tone.
2. Use Markdown for formatting, especially for code snippets.
3. Keep conversation history in mind for context.
4. Encourage the use of `paste`, `upload`, or `fetch` commands when appropriate for longer JSON tasks.
5. When providing JSON snippets, use 'json' markdown code blocks.
"""

    def chat(self, user_message: str) -> str:
        """
        Engages in a conversational chat about JSON.

        Args:
            user_message: The user's message or question.

        Returns:
            The chatbot's response as a string.
        """
        if not self.config.is_available():
            return self._fallback_chat_response(user_message)

        self.conversation_history.append({"role": "user", "content": user_message})

        try:
            response = self.client.chat.completions.create(
                model=self.config.get_model(),
                messages=self.conversation_history,
                max_tokens=self.config.get_max_tokens(),
                temperature=self.config.get_temperature()
            )
            assistant_response = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            return assistant_response
        except Exception as e:
            print(f"Error calling OpenAI API for chatbot: {e}")
            return self._fallback_chat_response(user_message)

    def _fallback_chat_response(self, user_message: str) -> str:
        """Fallback chat response when OpenAI is not available"""
        if "hello" in user_message.lower() or "hi" in user_message.lower():
            return "Hello there! I'm JSONHelperBot's chat assistant. How can I help you with JSON today? Please set up your OpenAI API key for full AI capabilities."
        elif "parse" in user_message.lower() or "explain" in user_message.lower() or "json" in user_message.lower():
            return "I can help parse and explain JSON! Please use the 'paste', 'upload', or 'fetch' commands. For full AI features, set up your OpenAI API key."
        return "I'm sorry, I can only provide limited assistance offline. Please set up your OpenAI API key for full conversational capabilities. You can still use the `paste`, `upload`, and `fetch` commands with basic functionality."

    def reset_chat_history(self) -> None:
        """Resets the chatbot's conversation history"""
        self.conversation_history = []
        self._initialize_history()
