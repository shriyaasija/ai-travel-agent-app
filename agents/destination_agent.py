from .base_agent import BaseAgent

class DestinationAgent(BaseAgent):
    def __init__(self, api_key: str):
        super().__init__("DestinationExpert", api_key)

    async def get_destination_info(self, travel_request: str) -> str:
        self.logger.info(f"Researching destinations for: {travel_request}")

        destination_prompt = f"""
        You are a destination expert with deep knowledge of travel destinations worldwide.
        
        Travel request: "{travel_request}"
        
        Provide detailed information about:
        1. Top attractions and must-see places
        2. Local culture and customs
        3. Best time to visit
        4. Transportation options
        5. Food and dining recommendations
        6. Hidden gems and local favourites
        7. Safety tips and considerations
        
        Be specific and practical. Include insider tips that make the difference between a good trip and an amazing trip
        """

        result = await self.think(destination_prompt)
        self.logger.info(f"Destination research completed")
        return result
    
    async def find_activities(self, destination: str, interests: list) -> str:
        interests_str = ", ".join(interests) if interests else "general sightseeing"

        activities_prompt = f"""
        Find specific activites in {destination} for someone interested in: {interests_str}

        Provide:
        1. Specific activity names and locations
        2. Approximate costs
        3. Time required
        4. Booking requirements
        5. Best time to visit
        
        Focus on unique, memorable experiences that match their interests.
        """

        result = await self.think(activities_prompt)
        return result

    def get_agent_description(self) -> str:
        return "I am the Destination Expert. I know everything about travel destinations, attractions, culture, and activities worldwide."