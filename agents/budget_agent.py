from .base_agent import BaseAgent
import re

class BudgetAgent(BaseAgent):
    def __init__(self, api_key: str):
        super().__init__("BudgetOptimiser", api_key)

    async def analyse_budget(self, travel_request: str) -> str:
        self.logger.info(f"Analysing budget for: {travel_request}")

        budget_prompt = f"""
        You are a budget optimisation expert for travel planning
        
        Travel Request: "{travel_request}"
        
        Analyse and provide:
        1. Estimated cost breakdown (flights, accomodation, food, activities, misc)
        2. Budget optimisation tips
        3. Money saving strategies
        4. Alternative options for different budget levels
        5. Hidden costs to watch out for
        6. Best time to book for savings
        
        If no specific budget is mentioned, provide estimates for budget, mid-range, and luxury options.
        Be specific with numbers and practical advice.
        """

        result = await self.think(budget_prompt)
        self.logger.info(f"Budget analysis complete")
        return result

    async def optimise_costs(self, destination: str, budget: str, duration: str) -> str:
        optimisation_prompt = f"""
        Optimise costs for:
        - Destination: {destination},
        - Budget: {budget}
        - Duration: {duration}

        Provide specific strategies:
        1. Best booking platforms and times
        2. Alternative accomodations
        3. Transportation hacks
        4. Free and low-cost activities
        5. Local money-saving tips
        6. Apps and tools for saving money
        
        Focus on actionable, specific advice."""

        result = await self.think(optimisation_prompt)
        return result
    
    def get_agent_description(self) -> str:
        return "I am the BudgetOptimiser. I help maximise your travel value by analysing costs and finding the best deals."