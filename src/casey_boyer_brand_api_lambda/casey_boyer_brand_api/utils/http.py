import logging
from typing import Any, Dict, List, Optional


logger = logging.getLogger(__name__)


def get_header(headers: Dict[str, str], name: str):
    return headers.get(name, headers.get(name.lower()))


def handle_options_request(headers: Dict[str, Any], allowed_methods: List[str]):
    logger.debug("handling OPTIONS request: " + str((headers, allowed_methods)))
    requested_methods = get_header(headers, "access-control-request-method")
    requested_origin: Optional[str] = get_header(headers, "origin")
    if (
        requested_methods in allowed_methods
        and requested_origin is not None
        and requested_origin.startswith("http://localhost")
    ):
        return {
            "statusCode": 200,
            "isBase64Encoded": False,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": requested_origin,
                "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            },
        }
    else:
        raise ValueError("invalid OPTIONS request")
