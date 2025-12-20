"""
Cloud Functions HTTP entry point for SAMMO Fight IQ.

Routes:
- POST /log_round -> store round in Firestore
- GET  /dashboard_stats -> aggregated stats and next game plan
- GET  /rounds_history -> list of rounds sorted by date (desc)

All responses include CORS headers.
"""
from typing import Any, Dict, List, Optional, Tuple
import os
from datetime import datetime

import functions_framework
from flask import jsonify, make_response
from google.cloud import firestore

# Initialize Firestore client globally
_firestore_client = firestore.Client()
_rounds_collection = _firestore_client.collection('rounds')


def _cors_headers() -> Dict[str, str]:
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }


def calculate_danger(round_data):
    # 0.0 to 1.0 scale
    clean = round_data.get('clean_shots_taken', 0) / 5.0
    defense = (10 - round_data.get('defense_score', 5)) / 10.0
    control = (10 - round_data.get('ring_control_score', 5)) / 10.0
    score = (0.5 * clean) + (0.3 * defense) + (0.2 * control)
    return max(0.0, min(score, 1.0))


def get_strategy(danger_score):
    if danger_score >= 0.7:
        return "DEFENSE_FIRST", "High guard, active feet. Max 2-punch combos. Pump the jab, angle off. Do not trade."
    elif danger_score >= 0.4:
        return "RING_CUTTING", "Smart pressure. Cut exits, feint to draw counters. No ego wars. Control space."
    else:
        return "PRESSURE_BODY", "Walk him down. Invest in the body and arms. Bully, clinch, drown him."


def _to_iso(ts) -> Optional[str]:
    if ts is None:
        return None
    # Firestore timestamps are datetime-like
    try:
        return ts.isoformat()
    except Exception:
        try:
            return datetime.fromtimestamp(float(ts)).isoformat()
        except Exception:
            return str(ts)


def _handle_log_round(request) -> Tuple[Any, int, Dict[str, str]]:
    payload = request.get_json(silent=True)
    if not payload:
        body = {'status': 'error', 'message': 'Invalid or missing JSON payload'}
        headers = _cors_headers()
        return jsonify(body), 400, headers

    # Add server timestamp
    payload['date'] = firestore.SERVER_TIMESTAMP

    doc_ref, _ = _rounds_collection.add(payload)
    body = {'status': 'success', 'id': doc_ref.id}
    headers = _cors_headers()
    return jsonify(body), 200, headers


def _handle_dashboard_stats(request) -> Tuple[Any, int, Dict[str, str]]:
    docs = list(_rounds_collection.stream())
    count = 0
    totals = {'pressure_score': 0.0, 'ring_control_score': 0.0, 'defense_score': 0.0, 'clean_shots_taken': 0.0}
    most_recent = None
    most_recent_date = None

    for d in docs:
        data = d.to_dict() or {}
        count += 1
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

    next_game_plan = (None, None)
    if most_recent:
        danger_score = calculate_danger(most_recent)
        next_game_plan = get_strategy(danger_score)

    body = {
        'averages': averages,
        'most_recent_round_date': _to_iso(most_recent_date) if most_recent_date is not None else None,
        'next_game_plan': {
            'title': next_game_plan[0],
            'text': next_game_plan[1]
        }
    }
    headers = _cors_headers()
    return jsonify(body), 200, headers


def _handle_rounds_history(request) -> Tuple[Any, int, Dict[str, str]]:
    docs = list(_rounds_collection.stream())
    rounds: List[Dict[str, Any]] = []
    for d in docs:
        data = d.to_dict() or {}
        data['id'] = d.id
        date_val = data.get('date')
        data['date'] = _to_iso(date_val)
        rounds.append(data)

    # Sort by date desc; items with None date go to the end
    def _date_key(item):
        return item.get('date') or ''

    rounds.sort(key=_date_key, reverse=True)

    headers = _cors_headers()
    return jsonify({'rounds': rounds}), 200, headers


@functions_framework.http
def sammo(request):
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return ('', 204, _cors_headers())

    path = request.path or request.environ.get('PATH_INFO', '/')
    # Normalize path
    path = path.rstrip('/')

    if path.endswith('/log_round') and request.method == 'POST':
        return _handle_log_round(request)
    elif path.endswith('/dashboard_stats') and request.method == 'GET':
        return _handle_dashboard_stats(request)
    elif path.endswith('/rounds_history') and request.method == 'GET':
        return _handle_rounds_history(request)
    else:
        headers = _cors_headers()
        return jsonify({'status': 'error', 'message': 'Not Found'}), 404, headers
