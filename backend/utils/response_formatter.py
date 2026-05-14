from datetime import datetime
from typing import Any
from flask import jsonify


class ResponseFormatter:
    @staticmethod
    def success(data: Any = None, message: str = "OK", status_code: int = 200) -> tuple:
        response = {
            "success": True,
            "message": message,
            "data": data,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

        return jsonify(response), status_code

    @staticmethod
    def error(
        message: str,
        error_code: str | None = None,
        details: Any = None,
        status_code: int = 400,
    ) -> tuple:
        response = {
            "success": False,
            "message": message,
            "data": None,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

        if error_code or details is not None:
            response["error"] = {
                "code": error_code,
                "details": details,
            }

        return jsonify(response), status_code


def success_response(data: Any = None, message: str = "OK", status_code: int = 200) -> tuple:
    return ResponseFormatter.success(
        data=data,
        message=message,
        status_code=status_code
    )


def error_response(
    message: str,
    error_code: str | None = None,
    details: Any = None,
    status_code: int = 400,
) -> tuple:
    return ResponseFormatter.error(
        message=message,
        error_code=error_code,
        details=details,
        status_code=status_code
    )
