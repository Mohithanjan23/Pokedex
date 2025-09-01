from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)  # This will allow the frontend to make requests to this backend

# In a real application, you would use a database.
# For this example, we'll use a simple JSON file as a "database" for the leaderboard.
LEADERBOARD_FILE = 'leaderboard.json'

def get_leaderboard():
    """Reads the leaderboard data from the JSON file."""
    try:
        with open(LEADERBOARD_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_leaderboard(leaderboard_data):
    """Saves the leaderboard data to the JSON file."""
    # Sort by score descending before saving
    leaderboard_data.sort(key=lambda x: x['score'], reverse=True)
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard_data, f, indent=4)

@app.route('/')
def index():
    return "Welcome to the Pokédex Backend API! Gotta Code 'Em All!"

@app.route('/api/leaderboard', methods=['GET'])
def api_get_leaderboard():
    """API endpoint to get the current leaderboard."""
    leaderboard = get_leaderboard()
    return jsonify(leaderboard[:10]) # Return top 10 scores

@app.route('/api/leaderboard', methods=['POST'])
def api_update_leaderboard():
    """API endpoint to add a new score to the leaderboard."""
    data = request.get_json()
    if not data or 'name' not in data or 'score' not in data:
        return jsonify({'error': 'Invalid data. "name" and "score" are required.'}), 400

    name = data['name']
    score = data['score']
    
    leaderboard = get_leaderboard()
    leaderboard.append({'name': name, 'score': score})
    save_leaderboard(leaderboard)
    
    return jsonify({'success': True, 'message': 'Leaderboard updated.'}), 201

# Note: The /pokemon/{id}, /search, and /random logic is handled
# client-side with the public PokeAPI to reduce server load and complexity.
# If you wanted to add them here, you would use a library like `requests`
# to call the PokeAPI from the backend.

if __name__ == '__main__':
    # For development, you can run this script directly.
    # For production, use a proper WSGI server like Gunicorn or Waitress.
    app.run(debug=True, port=5001)


