import time
from flask import request, g, current_app


def log_request():
    g.start_time = time.time()
    current_app.logger.info("Request %s %s", request.method, request.path)


def log_response(response):
    if hasattr(g, 'start_time'):
        elapsed = time.time() - g.start_time
        current_app.logger.info(
            "Response %s %s %s %.3fs",
            request.method,
            request.path,
            response.status_code,
            elapsed,
        )
    
    return response
