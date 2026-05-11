"""
Request Logger Middleware
==========================
Log all API requests and responses.

Author: Senior Backend Engineer
Date: 2026-05-11
"""

import time
from flask import request, g, current_app


def log_request():
    """Log incoming request."""
    g.start_time = time.time()
    
    current_app.logger.info(
        f"Request: {request.method} {request.path} "
        f"from {request.remote_addr}"
    )
    
    if request.is_json and current_app.debug:
        current_app.logger.debug(f"Request body: {request.get_json()}")


def log_response(response):
    """Log outgoing response."""
    if hasattr(g, 'start_time'):
        elapsed = time.time() - g.start_time
        current_app.logger.info(
            f"Response: {request.method} {request.path} "
            f"Status: {response.status_code} "
            f"Time: {elapsed:.3f}s"
        )
    
    return response
