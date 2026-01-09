"""
JKD Coach - Flask Application with JWT Authentication

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
import tempfile
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from google.cloud import firestore
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

# Import video analysis modules
try:
    from src.video_analyzer import analyze_video_file
    from src.risk_model import video_form_and_danger
    VIDEO_ANALYSIS_AVAILABLE = True
except ImportError:
    VIDEO_ANALYSIS_AVAILABLE = False
    print("⚠️  Video analysis modules not available")

# ============================================================================
# Configuration
# ============================================================================

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Initialize Flask app
app = Flask(__name__)
# Enable CORS for all routes, origins, and methods
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"],
    "expose_headers": ["Content-Type", "Authorization"],
    "supports_credentials": False
}})

# Initialize Firestore client
try:
    _firestore_client = firestore.Client()
    _rounds_collection = _firestore_client.collection('rounds')
    _users_collection = _firestore_client.collection('users')
    print("✅ Connected to Firestore successfully")
except Exception as e:
    print(f"⚠️  Firestore initialization warning: {e}")
    _firestore_client = None
    _rounds_collection = None
    _users_collection = None


# ============================================================================
# Password & JWT Functions
# ============================================================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        return None
    except Exception:
        return None


# ============================================================================
# User Store Functions
# ============================================================================

def create_user(username: str, email: str, password: str, full_name: str = None) -> dict:
    """Create a new user."""
    if _users_collection is None:
        raise Exception("Firestore not available")
    
    # Check if username exists
    existing = list(_users_collection.where('username', '==', username).limit(1).get())
    if existing:
        raise ValueError(f"Username '{username}' already exists")
    
    # Check if email exists
    existing = list(_users_collection.where('email', '==', email).limit(1).get())
    if existing:
        raise ValueError(f"Email '{email}' already exists")
    
    # Create user document
    import uuid
    user_id = str(uuid.uuid4())
    user_doc = {
        'id': user_id,
        'username': username,
        'email': email,
        'full_name': full_name,
        'hashed_password': get_password_hash(password),
        'created_at': firestore.SERVER_TIMESTAMP,
        'is_active': True,
        'is_verified': False
    }
    
    _users_collection.document(user_id).set(user_doc)
    user_doc.pop('hashed_password')
    return user_doc


def get_user_by_username(username: str) -> Optional[dict]:
    """Get user by username."""
    if _users_collection is None:
        return None
    docs = list(_users_collection.where('username', '==', username).limit(1).get())
    if not docs:
        return None
    return docs[0].to_dict()


def get_user_by_id(user_id: str) -> Optional[dict]:
    """Get user by ID."""
    if _users_collection is None:
        return None
    doc = _users_collection.document(user_id).get()
    if not doc.exists:
        return None
    return doc.to_dict()


# ============================================================================
# Authentication Decorators
# ============================================================================

def get_current_user() -> Optional[dict]:
    """Get current user from request Authorization header."""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None
    
    token = parts[1]
    payload = decode_token(token)
    if not payload:
        return None
    
    user_id = payload.get('sub')
    if not user_id:
        return None
    
    user = get_user_by_id(user_id)
    if not user or not user.get('is_active', False):
        return None
    
    return user


def require_auth(f):
    """Decorator to require authentication for Flask routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if user is None:
            return jsonify({
                'status': 'error',
                'message': 'Authentication required'
            }), 401
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# Helper Functions
# ============================================================================

def calculate_danger(round_data: Dict[str, Any]) -> float:
    """Calculate danger score from round metrics."""
    clean = round_data.get('clean_shots_taken', 0) / 5.0
    defense = (10 - round_data.get('defense_score', 5)) / 10.0
    control = (10 - round_data.get('ring_control_score', 5)) / 10.0
    score = (0.5 * clean) + (0.3 * defense) + (0.2 * control)
    return max(0.0, min(score, 1.0))


def get_strategy(danger_score: float) -> Tuple[str, str]:
    """Get recommended boxing strategy based on danger score."""
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
    """Convert Firestore timestamp to ISO format string."""
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
        'service': 'JKD Coach',
        'version': '1.0.0',
        'description': 'AI-Powered Boxing Coach API with JWT Authentication',
        'tagline': 'Be Water. Train Smarter.',
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
                'analyze_video': '/api/analyze_video (POST - multipart/form-data)',
                'dashboard_stats': '/api/dashboard_stats (GET)',
                'rounds_history': '/api/rounds_history (GET)',
                'delete_round': '/api/rounds/{id} (DELETE)'
            }
        }
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    firestore_status = "connected" if _firestore_client is not None else "disconnected"
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'firestore': firestore_status
    }), 200


# ============================================================================
# Authentication Endpoints
# ============================================================================

@app.route('/auth/register', methods=['POST'])
def register():
    """Register a new user."""
    if _users_collection is None:
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
        user = create_user(
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
    """Login and get JWT access token."""
    if _users_collection is None:
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
        user = get_user_by_username(username)
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
            'expires_in': ACCESS_TOKEN_EXPIRE_MINUTES * 60
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
    """Get current authenticated user information."""
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
    """Log a new boxing round with danger score and strategy calculation."""
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


@app.route('/api/analyze_video', methods=['POST'])
@require_auth
def analyze_video():
    """Analyze a boxing video and extract metrics using MediaPipe pose detection."""
    if not VIDEO_ANALYSIS_AVAILABLE:
        return jsonify({
            'status': 'error',
            'message': 'Video analysis not available - missing dependencies'
        }), 503

    if _rounds_collection is None:
        return jsonify({
            'status': 'error',
            'message': 'Firestore not available'
        }), 503

    try:
        user = get_current_user()

        # Check if video file was uploaded
        if 'video' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No video file provided'
            }), 400

        video_file = request.files['video']

        if video_file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'Empty filename'
            }), 400

        # Get optional metadata from form data
        round_name = request.form.get('round_name', 'video_round')
        notes = request.form.get('notes', '')

        # Save uploaded video to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            temp_path = temp_file.name
            video_file.save(temp_path)

        try:
            # Analyze video using MediaPipe
            app.logger.info(f"Analyzing video: {video_file.filename}")
            metrics = analyze_video_file(temp_path)

            # Calculate danger and form scores
            enriched_metrics = video_form_and_danger(metrics)

            # Get danger score and focus recommendation
            danger_score = enriched_metrics['video_danger_score']
            form_score = enriched_metrics['video_form_score']
            focus_next_round = enriched_metrics['video_focus_next_round']

            # Generate coaching strategy based on danger score
            strategy_title, strategy_text = get_strategy(danger_score)

            # Prepare document for Firestore
            round_doc = {
                'user_id': user['id'],
                'username': user['username'],
                'round_name': round_name,
                'video_filename': video_file.filename,
                'notes': notes,

                # Video metrics
                'total_frames': enriched_metrics['total_frames'],
                'pose_frames': enriched_metrics['pose_frames'],
                'pose_coverage': enriched_metrics['pose_coverage'],
                'guard_down_ratio': enriched_metrics['guard_down_ratio'],
                'avg_left_guard_height': enriched_metrics['avg_left_guard_height'],
                'avg_right_guard_height': enriched_metrics['avg_right_guard_height'],
                'avg_hip_rotation': enriched_metrics['avg_hip_rotation'],
                'avg_stance_width': enriched_metrics['avg_stance_width'],
                'head_movement_score': enriched_metrics['head_movement_score'],

                # Scores and recommendations
                'danger_score': danger_score,
                'form_score': form_score,
                'focus_next_round': focus_next_round,
                'strategy_title': strategy_title,
                'strategy_text': strategy_text,

                'date': firestore.SERVER_TIMESTAMP,
                'analysis_type': 'video'
            }

            # Store in Firestore
            doc_ref, _ = _rounds_collection.add(round_doc)

            # Generate coaching feedback
            coaching_feedback = generate_video_coaching(enriched_metrics, strategy_text)

            return jsonify({
                'status': 'success',
                'id': doc_ref.id,
                'metrics': {
                    'total_frames': enriched_metrics['total_frames'],
                    'pose_coverage': round(enriched_metrics['pose_coverage'] * 100, 1),
                    'guard_down_ratio': round(enriched_metrics['guard_down_ratio'] * 100, 1),
                    'avg_left_guard_height': round(enriched_metrics['avg_left_guard_height'], 3),
                    'avg_right_guard_height': round(enriched_metrics['avg_right_guard_height'], 3),
                    'avg_hip_rotation': round(enriched_metrics['avg_hip_rotation'], 1),
                    'avg_stance_width': round(enriched_metrics['avg_stance_width'], 3),
                    'head_movement_score': round(enriched_metrics['head_movement_score'], 3),
                },
                'scores': {
                    'danger_score': round(danger_score, 2),
                    'form_score': round(form_score, 1),
                    'focus_next_round': focus_next_round
                },
                'strategy': {
                    'title': strategy_title,
                    'text': strategy_text
                },
                'coaching': coaching_feedback
            }), 200

        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': f'Video analysis error: {str(e)}'
        }), 400
    except Exception as e:
        app.logger.error(f"Error analyzing video: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }), 500


def generate_video_coaching(metrics: Dict[str, Any], strategy_text: str) -> str:
    """Generate coaching feedback based on video metrics."""
    danger_score = metrics['video_danger_score']
    guard_down_ratio = metrics['guard_down_ratio']
    pose_coverage = metrics['pose_coverage']

    feedback_parts = []

    # Danger level assessment
    if danger_score >= 0.7:
        feedback_parts.append("⚠️ HIGH RISK - Your danger score is critically high.")
    elif danger_score >= 0.4:
        feedback_parts.append("⚡ MODERATE RISK - Some defensive concerns to address.")
    else:
        feedback_parts.append("✅ LOW RISK - Good defensive fundamentals.")

    # Guard discipline
    if guard_down_ratio > 0.3:
        feedback_parts.append(f"Guard down {guard_down_ratio*100:.0f}% of the time - MAJOR concern.")
    elif guard_down_ratio > 0.15:
        feedback_parts.append(f"Guard dropping {guard_down_ratio*100:.0f}% of frames - needs work.")
    else:
        feedback_parts.append(f"Solid guard discipline ({guard_down_ratio*100:.0f}% down).")

    # Pose tracking quality
    if pose_coverage < 0.5:
        feedback_parts.append(f"Low tracking coverage ({pose_coverage*100:.0f}%) - video quality issue or angles.")

    # Hip rotation
    hip_rotation = metrics['avg_hip_rotation']
    if hip_rotation < 25:
        feedback_parts.append(f"Hip rotation weak ({hip_rotation:.0f}°) - work on stance and pivots.")
    elif hip_rotation > 40:
        feedback_parts.append(f"Good hip rotation ({hip_rotation:.0f}°) - generating power.")

    # Add strategy
    feedback_parts.append(f"\nStrategy: {strategy_text}")

    return "\n".join(feedback_parts)


@app.route('/api/dashboard_stats', methods=['GET'])
@require_auth
def get_dashboard_stats():
    """Get aggregated statistics for the authenticated user."""
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
    """Get history of user's rounds, sorted by date (most recent first)."""
    if _rounds_collection is None:
        return jsonify({
            'status': 'error',
            'message': 'Firestore not available'
        }), 503
    
    try:
        user = get_current_user()
        
        # Get limit from query parameter
        limit = request.args.get('limit', default=100, type=int)
        limit = min(limit, 1000)
        
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
    """Delete a specific round."""
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
    port = int(os.getenv('PORT', 8080))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv('FLASK_ENV') == 'development'
    )
