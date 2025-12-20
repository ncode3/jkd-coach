"""
FastAPI server for SAMMO Fight IQ with JWT authentication.

Provides authenticated REST API endpoints for boxing analysis and coaching.
"""
from typing import Dict, List, Any, Optional
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from google.cloud import firestore

from src.auth.routes import router as auth_router
from src.auth.dependencies import get_current_user, optional_authentication
from src.auth.models import UserInDB

# Initialize FastAPI app
app = FastAPI(
    title="SAMMO Fight IQ API",
    description="AI-Powered Boxing Coach API with JWT Authentication",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth_router)

# Initialize Firestore client
_firestore_client = firestore.Client()
_rounds_collection = _firestore_client.collection('rounds')


# Request/Response Models
class RoundData(BaseModel):
    """Round data for boxing analysis."""
    pressure_score: float = Field(..., ge=0, le=10)
    ring_control_score: float = Field(..., ge=0, le=10)
    defense_score: float = Field(..., ge=0, le=10)
    clean_shots_taken: int = Field(..., ge=0)
    notes: Optional[str] = None


class RoundResponse(BaseModel):
    """Response after logging a round."""
    status: str
    id: str
    danger_score: float
    strategy: Dict[str, str]


class DashboardStats(BaseModel):
    """Dashboard statistics response."""
    averages: Dict[str, float]
    most_recent_round_date: Optional[str]
    next_game_plan: Dict[str, Optional[str]]
    total_rounds: int


class RoundHistory(BaseModel):
    """Individual round in history."""
    id: str
    date: Optional[str]
    pressure_score: float
    ring_control_score: float
    defense_score: float
    clean_shots_taken: int
    danger_score: Optional[float]
    notes: Optional[str]


class RoundHistoryResponse(BaseModel):
    """Round history response."""
    rounds: List[Dict[str, Any]]
    total: int


# Helper functions
def calculate_danger(round_data: Dict[str, Any]) -> float:
    """Calculate danger score from round data."""
    clean = round_data.get('clean_shots_taken', 0) / 5.0
    defense = (10 - round_data.get('defense_score', 5)) / 10.0
    control = (10 - round_data.get('ring_control_score', 5)) / 10.0
    score = (0.5 * clean) + (0.3 * defense) + (0.2 * control)
    return max(0.0, min(score, 1.0))


def get_strategy(danger_score: float) -> tuple[str, str]:
    """Get boxing strategy based on danger score."""
    if danger_score >= 0.7:
        return "DEFENSE_FIRST", "High guard, active feet. Max 2-punch combos. Pump the jab, angle off. Do not trade."
    elif danger_score >= 0.4:
        return "RING_CUTTING", "Smart pressure. Cut exits, feint to draw counters. No ego wars. Control space."
    else:
        return "PRESSURE_BODY", "Walk him down. Invest in the body and arms. Bully, clinch, drown him."


# API Routes
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "SAMMO Fight IQ API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.post("/api/log_round", response_model=RoundResponse)
async def log_round(
    round_data: RoundData,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Log a new boxing round with user-specific data.

    Requires authentication. Stores round data associated with the user.

    Args:
        round_data: Round statistics and notes
        current_user: Authenticated user from JWT token

    Returns:
        Round ID, danger score, and recommended strategy
    """
    # Calculate danger score
    danger_score = calculate_danger(round_data.dict())
    strategy_title, strategy_text = get_strategy(danger_score)

    # Prepare document with user association
    round_doc = {
        **round_data.dict(),
        'user_id': current_user.id,
        'username': current_user.username,
        'danger_score': danger_score,
        'strategy_title': strategy_title,
        'strategy_text': strategy_text,
        'date': firestore.SERVER_TIMESTAMP
    }

    # Store in Firestore
    doc_ref, _ = _rounds_collection.add(round_doc)

    return RoundResponse(
        status="success",
        id=doc_ref.id,
        danger_score=danger_score,
        strategy={
            "title": strategy_title,
            "text": strategy_text
        }
    )


@app.get("/api/dashboard_stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Get aggregated statistics for the authenticated user.

    Returns average scores and recommended next strategy based on recent performance.

    Args:
        current_user: Authenticated user from JWT token

    Returns:
        Dashboard statistics including averages and game plan
    """
    # Query only the current user's rounds
    docs = list(
        _rounds_collection
        .where('user_id', '==', current_user.id)
        .stream()
    )

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
        for key in totals:
            try:
                totals[key] += float(data.get(key, 0.0) or 0.0)
            except Exception:
                totals[key] += 0.0

        date_val = data.get('date')
        if date_val is not None:
            if most_recent_date is None or date_val > most_recent_date:
                most_recent_date = date_val
                most_recent = data

    if count == 0:
        averages = {k: 0.0 for k in totals}
    else:
        averages = {k: (totals[k] / count) for k in totals}

    next_game_plan = {"title": None, "text": None}
    if most_recent:
        danger_score = calculate_danger(most_recent)
        strategy_title, strategy_text = get_strategy(danger_score)
        next_game_plan = {"title": strategy_title, "text": strategy_text}

    return DashboardStats(
        averages=averages,
        most_recent_round_date=most_recent_date.isoformat() if most_recent_date else None,
        next_game_plan=next_game_plan,
        total_rounds=count
    )


@app.get("/api/rounds_history", response_model=RoundHistoryResponse)
async def get_rounds_history(
    limit: int = 100,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Get round history for the authenticated user.

    Returns list of all rounds sorted by date (most recent first).

    Args:
        limit: Maximum number of rounds to return
        current_user: Authenticated user from JWT token

    Returns:
        List of user's boxing rounds
    """
    # Query only the current user's rounds
    docs = list(
        _rounds_collection
        .where('user_id', '==', current_user.id)
        .limit(limit)
        .stream()
    )

    rounds = []
    for d in docs:
        data = d.to_dict() or {}
        data['id'] = d.id

        # Convert Firestore timestamp to ISO string
        date_val = data.get('date')
        if date_val:
            try:
                data['date'] = date_val.isoformat()
            except Exception:
                data['date'] = str(date_val)
        else:
            data['date'] = None

        rounds.append(data)

    # Sort by date descending
    rounds.sort(key=lambda x: x.get('date') or '', reverse=True)

    return RoundHistoryResponse(
        rounds=rounds,
        total=len(rounds)
    )


@app.delete("/api/rounds/{round_id}")
async def delete_round(
    round_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """
    Delete a specific round.

    Users can only delete their own rounds.

    Args:
        round_id: Round ID to delete
        current_user: Authenticated user from JWT token

    Returns:
        Success message

    Raises:
        HTTPException: If round not found or unauthorized
    """
    # Get the round document
    doc_ref = _rounds_collection.document(round_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Round not found"
        )

    # Check if the round belongs to the current user
    round_data = doc.to_dict()
    if round_data.get('user_id') != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this round"
        )

    # Delete the round
    doc_ref.delete()

    return {"status": "success", "message": "Round deleted"}


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint (no authentication required).

    Returns:
        Health status
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
