# command_router.py

from utils.llm_service import LLMService
from agents.agent_registry import AGENT_REGISTRY

class CommandRouter:
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        self.agent_registry = AGENT_REGISTRY

    def route_command(self, command: str):
        prompt = self._build_routing_prompt(command)
        
        # Get the LLM's response
        llm_response = self.llm_service.generate_response(prompt)
        
        # Parse the response to get the agent name and arguments
        agent_name, args = self._parse_llm_response(llm_response)
        
        if agent_name in self.agent_registry:
            return self.agent_registry[agent_name], args
        else:
            return None, None

    def _build_routing_prompt(self, command: str) -> str:
        agent_descriptions = self._get_agent_descriptions()
        
        prompt = f"""
        You are an intelligent command router for a personal assistant named Jarvis.
        Your task is to determine the most appropriate agent to handle the user's command.

        Here are the available agents and their descriptions:
        {agent_descriptions}

        User command: "{command}"

        Based on the user's command, which agent should be used?
        Please respond with the name of the agent and any arguments that should be passed to it, in the following format:
        AGENT: [AgentName]
        ARGS: [arguments]
        
        If no specific agent is applicable, respond with:
        AGENT: None
        ARGS: None
        """
        return prompt

    def _get_agent_descriptions(self) -> str:
        descriptions = ""
        for agent_name, agent_class in self.agent_registry.items():
            # In a real application, you would have more descriptive docstrings for each agent.
            descriptions += f"- {agent_name}: {agent_class.__doc__ or 'No description available.'}\n"
        return descriptions

    def _parse_llm_response(self, response: str) -> (str, str):
        agent_name = None
        args = None
        
        lines = response.strip().split('\n')
        for line in lines:
            if line.startswith("AGENT:"):
                agent_name = line.replace("AGENT:", "").strip()
            elif line.startswith("ARGS:"):
                args = line.replace("ARGS:", "").strip()
                
        return agent_name, args