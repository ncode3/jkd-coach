"""
SAMMO Fight IQ - Flask Application with JWT Authentication

A containerized boxing analysis API that provides:
- User registration and login with JWT tokens
- Health check endpoint
- Round logging with danger score calculation (protected)
- Dashboard statistics (protected, user-specific)
- Round history retrieval (protected, user-specific)
- Round deletion (protected, user-specific)

Connects to Google Cloud Firestore for data persistence.
"""
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from google.cloud import firestore
from dotenv import load_dotenv

# Import authentication module
from auth_flask import (
    require_auth,
    optional_auth,
    get_current_user,
    create_access_token,
    verify_password,
    user_store,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Firestore client
try:
    _firestore_client = firestore.Client()
    _rounds_collection = _firestore_client.collection('rounds')
    print("✅ Connected to Firestore successfully")
except Exception as e:
    print(f"⚠️  Firestore initialization warning: {e}")
    _firestore_client = None
    _rounds_collection = None


# ============================================================================
# Helper Functions
# ============================================================================

def calculate_danger(round_data: Dict[str, Any]) -> float:
    """
    Calculate danger score from round metrics.

    Formula:
    - 50% weight: clean shots taken (normalized to 0-1, assuming max 5 shots)
    - 30% weight: defense score (inverted, 10 is best)
    - 20% weight: ring control score (inverted, 10 is best)

    Args:
        round_data: Dictionary containing round metrics

    Returns:
        Danger score between 0.0 (safe) and 1.0 (high danger)
    """
    clean = round_data.get('clean_shots_taken', 0) / 5.0
    defense = (10 - round_data.get('defense_score', 5)) / 10.0
    control = (10 - round_data.get('ring_control_score', 5)) / 10.0
    score = (0.5 * clean) + (0.3 * defense) + (0.2 * control)
    return max(0.0, min(score, 1.0))


def get_strategy(danger_score: float) -> Tuple[str, str]:
    """
    Get recommended boxing strategy based on danger score.

    Strategy zones:
    - High danger (≥0.7): DEFENSE_FIRST - Focus on protection
    - Medium danger (0.4-0.7): RING_CUTTING - Smart pressure
    - Low danger (<0.4): PRESSURE_BODY - Aggressive offense

    Args:
        danger_score: Danger score between 0.0 and 1.0

    Returns:
        Tuple of (strategy_title, strategy_text)
    """
    if danger_score >= 0.7:
        return (
            "DEFENSE_FIRST",
            "High guard, active feet. Max 2-punch combos. Pump the jab, angle off. Do not trade."
        )
    elif danger_score >= 0.4:
        return (
            "RING_CUTTING",
            "Smart pressure. Cut exits, feint to draw counters. No ego wars. Control space."
        )
    else:
        return (
            "PRESSURE_BODY",
            "Walk him down. Invest in the body and arms. Bully, clinch, drown him."
        )


def _to_iso(ts) -> Optional[str]:
    """
    Convert Firestore timestamp to ISO format string.

    Args:
        ts: Firestore timestamp or datetime object

    Returns:
        ISO format string or None
    """
    if ts is None:
        return None
    try:
        return ts.isoformat()
    except Exception:
        try:
            return datetime.fromtimestamp(float(ts)).isoformat()
        except Exception:
            return str(ts)


# ============================================================================
# Public Endpoints
# ============================================================================

@app.route('/')
def root():
    """Root endpoint with API information."""
    return jsonify({
        'service': 'SAMMO Fight IQ',
        'version': '1.0.0',
        'description': 'AI-Powered Boxing Coach API with JWT Authentication',
        'authentication': 'JWT Bearer Token',
        'endpoints': {
            'public': {
                'health': '/health',
                'register': '/auth/register (POST)',
                'login': '/auth/login (POST)'
            },
            'protected': {
                'me': '/auth/me (GET)',
                'log_round': '/api/log_round (POST)',
                'dashboard_stats': '/api/dashboard_stats (GET)',
                'rounds_history': '/api/rounds_history (GET)',
                'delete_round': '/api/rounds/{id} (DELETE)'
            }
        }
    })


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for OpenShift probes.

    Returns:
        JSON with status and timestamp
    """
    firestore_status = "connected" if _firestore_client is not None else "disconnected"
    auth_status = "enabled" if user_store is not None else "disabled"

    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'firestore': firestore_status,
        'authentication': auth_status
    }), 200


# ============================================================================
# Authentication Endpoints
# ============================================================================

@app.route('/auth/register', methods=['POST'])
def register():
    """
    Register a new user.

    Expected JSON:
    {
        "username": "fighter1",
        "email": "fighter@example.com",
        "password": "SecurePass123!",
        "full_name": "Fighter One" (optional)
    }

    Returns:
        User information (no password)
    """
    if user_store is None:
        return jsonify({
            'status': 'error',
            'message': 'Authentication not available'
        }), 503

    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'Invalid JSON payload'
            }), 400

        # Validate required fields
        required_fields = ['username', 'email', 'password']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400

        # Validate password length
        if len(data['password']) < 8:
            return jsonify({
                'status': 'error',
                'message': 'Password must be at least 8 characters'
            }), 400

        # Create user
        user = user_store.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            full_name=data.get('full_name')
        )

        return jsonify({
            'status': 'success',
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user.get('full_name'),
                'is_active': user.get('is_active', True),
                'is_verified': user.get('is_verified', False)
            }
        }), 201

    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
    except Exception as e:
        app.logger.error(f"Registration error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }), 500


@app.route('/auth/login', methods=['POST'])
def login():
    """
    Login and get JWT access token.

    Expected JSON:
    {
        "username": "fighter1",
        "password": "SecurePass123!"
    }

    Returns:
        JWT access token
    """
    if user_store is None:
        return jsonify({
            'status': 'error',
            'message': 'Authentication not available'
        }), 503

    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'message': 'Invalid JSON payload'
            }), 400

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({
                'status': 'error',
                'message': 'Username and password required'
            }), 400

        # Get user
        user = user_store.get_user_by_username(username)
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'Incorrect username or password'
            }), 401

        # Verify password
        if not verify_password(password, user['hashed_password']):
            return jsonify({
                'status': 'error',
                'message': 'Incorrect username or password'
            }), 401

        # Check if user is active
        if not user.get('is_active', False):
            return jsonify({
                'status': 'error',
                'message': 'User account is inactive'
            }), 403

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={'sub': user['id'], 'username': user['username']},
            expires_delta=access_token_expires
        )

        return jsonify({
            'access_token': access_token,
            'token_type': 'bearer',
            'expires_in': ACCESS_TOKEN_EXPIRE_MINUTES * 60  # seconds
        }), 200

    except Exception as e:
        app.logger.error(f"Login error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }), 500


@app.route('/auth/me', methods=['GET'])
@require_auth
def get_current_user_info():
    """
    Get current authenticated user information.

    Requires: Authorization header with Bearer token

    Returns:
        User profile information
    """
    user = get_current_user()

    return jsonify({
        'id': user['id'],
        'username': user['username'],
        'email': user['email'],
        'full_name': user.get('full_name'),
        'is_active': user.get('is_active', True),
        'is_verified': user.get('is_verified', False)
    }), 200


# ============================================================================
# Protected Boxing Endpoints
# ============================================================================

@app.route('/api/log_round', methods=['POST'])
@require_auth
def log_round():
    """
    Log a new boxing round with danger score and strategy calculation.

    Requires: Authorization header with Bearer token

    Expected JSON payload:
    {
        "pressure_score": float (0-10),
        "ring_control_score": float (0-10),
        "defense_score": float (0-10),
        "clean_shots_taken": int,
        "notes": str (optional)
    }

    Returns:
        JSON with round ID, danger score, and recommended strategy
    """
    if _rounds_collection is None:
        return jsonify({
            'status': 'error',
            'message': 'Firestore not available'
        }), 503

    try:
        user = get_current_user()
        payload = request.get_json()

        if not payload:
            return jsonify({
                'status': 'error',
                'message': 'Invalid or missing JSON payload'
            }), 400

        # Validate required fields
        required_fields = ['pressure_score', 'ring_control_score', 'defense_score', 'clean_shots_taken']
        missing_fields = [field for field in required_fields if field not in payload]

        if missing_fields:
            return jsonify({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400

        # Calculate danger score and strategy
        danger_score = calculate_danger(payload)
        strategy_title, strategy_text = get_strategy(danger_score)

        # Prepare document with user association
        round_doc = {
            'user_id': user['id'],
            'username': user['username'],
            'pressure_score': float(payload['pressure_score']),
            'ring_control_score': float(payload['ring_control_score']),
            'defense_score': float(payload['defense_score']),
            'clean_shots_taken': int(payload['clean_shots_taken']),
            'notes': payload.get('notes', ''),
            'danger_score': danger_score,
            'strategy_title': strategy_title,
            'strategy_text': strategy_text,
            'date': firestore.SERVER_TIMESTAMP
        }

        # Store in Firestore
        doc_ref, _ = _rounds_collection.add(round_doc)

        return jsonify({
            'status': 'success',
            'id': doc_ref.id,
            'danger_score': danger_score,
            'strategy': {
                'title': strategy_title,
                'text': strategy_text
            }
        }), 200

    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': f'Invalid data type: {str(e)}'
        }), 400
    except Exception as e:
        app.logger.error(f"Error logging round: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }), 500


@app.route('/api/dashboard_stats', methods=['GET'])
@require_auth
def get_dashboard_stats():
    """
    Get aggregated statistics for the authenticated user.

    Requires: Authorization header with Bearer token

    Returns:
        JSON with:
        - averages: Average scores across all user's rounds
        - most_recent_round_date: Date of most recent round
        - next_game_plan: Recommended strategy based on most recent round
        - total_rounds: Total number of rounds logged by user
    """
    if _rounds_collection is None:
        return jsonify({
            'status': 'error',
            'message': 'Firestore not available'
        }), 503

    try:
        user = get_current_user()

        # Query only the current user's rounds
        docs = list(_rounds_collection.where('user_id', '==', user['id']).stream())
        count = len(docs)

        totals = {
            'pressure_score': 0.0,
            'ring_control_score': 0.0,
            'defense_score': 0.0,
            'clean_shots_taken': 0.0
        }

        most_recent = None
        most_recent_date = None

        for d in docs:
            data = d.to_dict() or {}

            # Accumulate totals
            for key in totals:
                try:
                    totals[key] += float(data.get(key, 0.0) or 0.0)
                except Exception:
                    totals[key] += 0.0

            # Track most recent round
            date_val = data.get('date')
            if date_val is not None:
                if most_recent_date is None or date_val > most_recent_date:
                    most_recent_date = date_val
                    most_recent = data

        # Calculate averages
        if count == 0:
            averages = {k: 0.0 for k in totals}
        else:
            averages = {k: round(totals[k] / count, 2) for k in totals}

        # Generate next game plan based on most recent round
        next_game_plan = {'title': None, 'text': None}
        if most_recent:
            danger_score = calculate_danger(most_recent)
            strategy_title, strategy_text = get_strategy(danger_score)
            next_game_plan = {
                'title': strategy_title,
                'text': strategy_text
            }

        return jsonify({
            'averages': averages,
            'most_recent_round_date': _to_iso(most_recent_date),
            'next_game_plan': next_game_plan,
            'total_rounds': count
        }), 200

    except Exception as e:
        app.logger.error(f"Error getting dashboard stats: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }), 500


@app.route('/api/rounds_history', methods=['GET'])
@require_auth
def get_rounds_history():
    """
    Get history of user's rounds, sorted by date (most recent first).

    Requires: Authorization header with Bearer token

    Query Parameters:
        limit (optional): Maximum number of rounds to return (default: 100)

    Returns:
        JSON with:
        - rounds: List of round objects
        - total: Total number of rounds
    """
    if _rounds_collection is None:
        return jsonify({
            'status': 'error',
            'message': 'Firestore not available'
        }), 503

    try:
        user = get_current_user()

        # Get limit from query parameter
        limit = request.args.get('limit', default=100, type=int)
        limit = min(limit, 1000)  # Cap at 1000 for safety

        # Query only the current user's rounds
        docs = list(
            _rounds_collection
            .where('user_id', '==', user['id'])
            .limit(limit)
            .stream()
        )

        rounds = []
        for d in docs:
            data = d.to_dict() or {}
            data['id'] = d.id

            # Convert Firestore timestamp to ISO string
            date_val = data.get('date')
            data['date'] = _to_iso(date_val)

            rounds.append(data)

        # Sort by date descending (most recent first)
        rounds.sort(key=lambda x: x.get('date') or '', reverse=True)

        return jsonify({
            'rounds': rounds,
            'total': len(rounds)
        }), 200

    except Exception as e:
        app.logger.error(f"Error getting rounds history: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }), 500


@app.route('/api/rounds/<round_id>', methods=['DELETE'])
@require_auth
def delete_round(round_id):
    """
    Delete a specific round.

    Requires: Authorization header with Bearer token
    Users can only delete their own rounds.

    Args:
        round_id: Round ID to delete

    Returns:
        Success message
    """
    if _rounds_collection is None:
        return jsonify({
            'status': 'error',
            'message': 'Firestore not available'
        }), 503

    try:
        user = get_current_user()

        # Get the round document
        doc_ref = _rounds_collection.document(round_id)
        doc = doc_ref.get()

        if not doc.exists:
            return jsonify({
                'status': 'error',
                'message': 'Round not found'
            }), 404

        # Check if the round belongs to the current user
        round_data = doc.to_dict()
        if round_data.get('user_id') != user['id']:
            return jsonify({
                'status': 'error',
                'message': 'Not authorized to delete this round'
            }), 403

        # Delete the round
        doc_ref.delete()

        return jsonify({
            'status': 'success',
            'message': 'Round deleted'
        }), 200

    except Exception as e:
        app.logger.error(f"Error deleting round: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }), 500


# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500


# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    # Get port from environment variable (OpenShift uses PORT)
    port = int(os.getenv('PORT', 8080))

    # Run the application
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv('FLASK_ENV') == 'development'
    )
