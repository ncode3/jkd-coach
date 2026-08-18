"""Integration tests for the Cloud Function handler.

These tests call the `sammo` function directly with a Flask test request context.
"""

from flask import Flask, request
from main import sammo


def test_dashboard_stats_endpoint_empty():
    app = Flask(__name__)
    with app.test_request_context("/dashboard_stats", method="GET"):
        resp = sammo(request)
        # sammo returns (body, status, headers)
        if isinstance(resp, tuple):
            body, status, headers = resp
        else:
            body = resp
            status = getattr(resp, "status_code", 200)

        data = body.get_json()
        assert status == 200
        assert "averages" in data
