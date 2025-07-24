from .base_agent import BaseAgent

class TravelCoordinatorAgent(BaseAgent):

    def __init__(self, api_key: str):
        super().__init__("TravelCoordinator", api_key)

        self.available_agents = {
            "destination": None,
            "budget": None,
        }

    def register_agent(self, agent_type: str, agent_instance):
        self.available_agents[agent_type] = agent_instance
        self.logger.info(f"Registered {agent_type} agent")

    async def plan_trip(self, user_request: str) -> str:
        self.logger.info(f"Starting trip planning for: {user_request}")

        analysis_prompt = f"""
        You are a travel coordinator. Analyse this travel request and extract key information:
        
        User request: "{user_request}"
        
        Extract and format as JSON:
        {{
            "destination": "where they want to go",
            "budget": "their budget if mentioned",
            "duration": "how long the trip is",
            "interests": ["list", "of", "interests"],
            "special_requirements: "any special needs"
        }}
        
        If information is missing mark as "not_specified"
        """

        analysis_result = await self.think(analysis_prompt)
        self.logger.info(f"Trip analysis complete")

        destination_info = "No destination agent available"
        if self.available_agents["destination"]:
            destination_info = await self.available_agents["destination"].get_destination_info(user_request)

        budget_info = "No budget agent available"
        if self.available_agents["budget"]:
            budget_info = await self.available_agents["budget"].analyse_budget(user_request)

        final_plan_prompt = f"""
        You are an expert travel coordinator. Create a comprehensive travel plan using this information:
        
        Original Request: {user_request}
        Trip Analysis: {analysis_result},
        Destination Information: {destination_info},
        Budget Analysis: {budget_info}

        Create a detailed, helpful travel plan that addresses the user's needs.
        Include specific recommendations, tips, and practical advice.
        Format it in a friendly, easy-to-read way.
        """

        final_plan = await self.think(final_plan_prompt)
        self.logger.info(f"Travel plan completed")

        return final_plan
    
    def get_agent_description(self) -> str:
        return "I am the Travel Coordinator. I manage the other agents and create comprehensive travel plan for users."