import google.generativeai as genai
import logging
from datetime import datetime
import json

class BaseAgent:
    """Base agent for all AI agents in the system"""
    
    def __init__(self, agent_name: str, api_key: str):
        self.agent_name = agent_name
        self.api_key = api_key

        genai.configure(api_key=api_key)
        self.model=genai.GenerativeModel('gemini-1.5-flash')

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"Agent-{agent_name}")

        self.message_queue = []

        self.logger.info(f"Agent {agent_name} ready")

    async def think(self, prompt: str) -> str:
        try: 
            self.logger.info(f"{self.agent_name} is thinking")
            response = self.model.generate_content(prompt)
            self.logger.info(f"{self.agent_name} finished thinking")
            return response.text
        except Exception as e:
            self.logger.error(f"{self.agent_name} has error {str(e)}")
            return f"Sorry, I encountered an error ({str(e)})"
    
    async def send_message_to_agent(self, recipient_agent: str, message: str) -> str:
        self.logger.info(f"{self.agent_name} is sending message to {recipient_agent}")

        agent_message = {
            "from": self.agent_name,
            "to": recipient_agent,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }

        return json.dumps(agent_message)
    
    def get_agent_description(self) -> str:
        return f"I am {self.agent_name}, a base AI agent"