"""
Error Handler Middleware
=========================
Centralized error handling.

Author: Senior Backend Engineer
Date: 2026-05-11
"""

from flask import current_app
from api.utils.response_formatter import ResponseFormatter


def handle_400(error):
    """Handle 400 Bad Request errors."""
    current_app.logger.warning(f"Bad Request: {error}")
    return ResponseFormatter.error(
        message="Bad Request",
        error_code="BAD_REQUEST",
        details=str(error),
        status_code=400
    )


def handle_404(error):
    """Handle 404 Not Found errors."""
    current_app.logger.warning(f"Not Found: {error}")
    return ResponseFormatter.error(
        message="Resource not found",
        error_code="NOT_FOUND",
        status_code=404
    )


def handle_500(error):
    """Handle 500 Internal Server Error."""
    current_app.logger.error(f"Internal Server Error: {error}", exc_info=True)
    return ResponseFormatter.error(
        message="Internal server error",
        error_code="INTERNAL_ERROR",
        details=str(error) if current_app.debug else None,
        status_code=500
    )


def handle_generic_exception(error):
    """Handle generic exceptions."""
    current_app.logger.error(f"Unhandled exception: {error}", exc_info=True)
    return ResponseFormatter.error(
        message="An unexpected error occurred",
        error_code="UNEXPECTED_ERROR",
        details=str(error) if current_app.debug else None,
        status_code=500
    )
