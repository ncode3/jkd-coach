"""Integration tests for the Cloud Function handler.

These tests call the `sammo` function directly with a Flask test request context.
"""

import importlib.util
from pathlib import Path

from flask import Flask, request

MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "deployments" / "cloud-functions" / "main.py"
)
SPEC = importlib.util.spec_from_file_location("cloud_function_main", MODULE_PATH)
assert SPEC and SPEC.loader
CLOUD_FUNCTION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLOUD_FUNCTION)
sammo = CLOUD_FUNCTION.sammo


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
