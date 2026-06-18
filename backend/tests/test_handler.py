"""Unit tests for the Lambda handler."""
import json
import pytest
from backend.lambda_function import lambda_handler, handle_submit, handle_health


class TestLambdaHandler:
    """Tests for the main lambda_handler function."""

    def test_options_returns_200(self):
        """CORS preflight should return 200."""
        event = {"httpMethod": "OPTIONS"}
        result = lambda_handler(event, None)
        assert result["statusCode"] == 200

    def test_unknown_path_returns_404(self):
        """Unknown paths should return 404."""
        event = {"path": "/unknown", "body": "{}"}
        result = lambda_handler(event, None)
        assert result["statusCode"] == 404

    def test_health_endpoint(self):
        """Health endpoint should return healthy status."""
        event = {"path": "/health", "body": "{}"}
        result = lambda_handler(event, None)
        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert body["status"] == "healthy"

    def test_version_endpoint(self):
        """Version endpoint should return version info."""
        event = {"path": "/version", "body": "{}"}
        result = lambda_handler(event, None)
        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert "version" in body


class TestSubmitHandler:
    """Tests for form submission."""

    def test_submit_success(self):
        """Valid submission should return 200 with submission ID."""
        event = {
            "path": "/submit",
            "body": json.dumps({
                "title": "Test Project",
                "description": "A test submission",
                "email": "test@example.com"
            })
        }
        result = lambda_handler(event, None)
        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert body["status"] == "received"
        assert "submission_id" in body
        assert body["submission_id"].startswith("SUB-")

    def test_submit_missing_title(self):
        """Missing title should return 400."""
        event = {
            "path": "/submit",
            "body": json.dumps({
                "description": "A test submission"
            })
        }
        result = lambda_handler(event, None)
        assert result["statusCode"] == 400

    def test_submit_missing_description(self):
        """Missing description should return 400."""
        event = {
            "path": "/submit",
            "body": json.dumps({
                "title": "Test Project"
            })
        }
        result = lambda_handler(event, None)
        assert result["statusCode"] == 400

    def test_submit_invalid_email(self):
        """Invalid email should return 400."""
        event = {
            "path": "/submit",
            "body": json.dumps({
                "title": "Test",
                "description": "Test",
                "email": "not-an-email"
            })
        }
        result = lambda_handler(event, None)
        assert result["statusCode"] == 400

    def test_submit_no_email_is_ok(self):
        """Email is optional - submission without it should work."""
        event = {
            "path": "/submit",
            "body": json.dumps({
                "title": "Test Project",
                "description": "A test submission"
            })
        }
        result = lambda_handler(event, None)
        assert result["statusCode"] == 200


class TestCORSHeaders:
    """Tests for CORS headers in responses."""

    def test_cors_headers_present(self):
        """All responses should include CORS headers."""
        event = {"path": "/health", "body": "{}"}
        result = lambda_handler(event, None)
        assert result["headers"]["Access-Control-Allow-Origin"] == "*"
        assert "POST" in result["headers"]["Access-Control-Allow-Methods"]


class TestPingEndpoint:
    """Tests for the ping endpoint."""

    def test_ping_returns_pong(self):
        """Ping should return pong."""
        event = {"path": "/ping", "body": "{}"}
        result = lambda_handler(event, None)
        assert result["statusCode"] == 200
        body = json.loads(result["body"])
        assert body["message"] == "pong"
