import json
import os
from datetime import datetime


def lambda_handler(event, context):
    """
    Demo Lambda handler for a form submission API.
    Handles multiple endpoints via path routing.
    """
    try:
        # Handle OPTIONS preflight (CORS)
        if event.get("httpMethod") == "OPTIONS":
            return _response(200, {"message": "OK"})

        # Parse body
        if "body" in event:
            body = json.loads(event["body"]) if isinstance(event["body"], str) else event["body"]
        else:
            body = event

        path = event.get("path", "") or body.get("path", "")

        # Route to handlers
        if path == "/submit":
            return handle_submit(body)
        elif path == "/health":
            return handle_health()
        elif path == "/version":
            return handle_version()
        else:
            return _response(404, {"error": f"Unknown path: {path}"})

    except Exception as e:
        print(f"Error: {str(e)}")
        return _response(500, {"error": "Internal server error"})


def handle_submit(body):
    """Handle form submission."""
    title = body.get("title", "")
    description = body.get("description", "")
    email = body.get("email", "")

    # Validate required fields
    if not title or not description:
        return _response(400, {
            "error": "Missing required fields",
            "required": ["title", "description"]
        })

    # Validate email format
    if email and "@" not in email:
        return _response(400, {"error": "Invalid email format"})

    # Process submission
    submission_id = f"SUB-{int(datetime.now().timestamp())}"

    return _response(200, {
        "submission_id": submission_id,
        "title": title,
        "status": "received",
        "message": "Form submitted successfully"
    })


def handle_health():
    """Health check endpoint."""
    return _response(200, {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": os.environ.get("APP_VERSION", "1.0.0")
    })


def handle_version():
    """Version endpoint."""
    return _response(200, {
        "version": os.environ.get("APP_VERSION", "1.0.0"),
        "environment": os.environ.get("ENVIRONMENT", "development")
    })


def _response(status_code, body):
    """Create API Gateway response with CORS headers."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps(body),
    }
