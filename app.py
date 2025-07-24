import os
from flask import Flask, render_template, request, jsonify, session
from agents.coordinator_agent import TravelCoordinatorAgent
from agents.destination_agent import DestinationAgent
from agents.budget_agent import BudgetAgent
import logging
import asyncio
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET-KEY', 'dev-secret-key-change-in-prod')

API_KEY = os.environ.get('GEMINI_API_KEY')
if not API_KEY:
    logger.error("GEMINI_API_KEY environment variable not set")
    raise ValueError("GEMINI_API_KEY environment variable is required")

logger.info("Initialising AI Agent System")

coordinator = TravelCoordinatorAgent(API_KEY)
destination_agent = DestinationAgent(API_KEY)
budget_agent = BudgetAgent(API_KEY)

coordinator.register_agent("destination", destination_agent)
coordinator.register_agent("budget", budget_agent)

logger.info("All agents initialised and registered")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/plan-trip', methods=['POST'])
def plan_trip():        
    try:
        data = request.get_json()
        user_request = data.get('request', '')

        if not user_request:
            return jsonify({'error': 'No travel request provided'}), 400
        
        logger.info(f"New travel request: {user_request}")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            travel_plan = loop.run_until_complete(coordinator.plan_trip(user_request))
        finally:
            loop.close()

        return jsonify({
            'success': True,
            'travel_plan': travel_plan,
            'agents_used': ['TravelCoordinator', 'DestinationExpert', 'BudgetOptimiser']
        })
        
    except Exception as e:
        logger.error(f"Error planning trip: {str(e)}")
        return jsonify({
            "error": f"Sorry, I encountered an error: {str(e)}"
        }), 500

@app.route('/api/agent-status')
def agent_status():
    return jsonify({
        'agents': {
            'coordinator': coordinator.get_agent_description(),
            'destination': destination_agent.get_agent_description(),
            'budget': budget_agent.get_agent_description()
        },
        'status': 'All agents operational'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)