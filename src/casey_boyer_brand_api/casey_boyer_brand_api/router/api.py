from datetime import datetime
import logging
from typing import Any, Dict, List, Optional
from http_router import Router
import json

from casey_boyer_brand_api.aws.CustomerTableRecord import CustomerTableRecord
from casey_boyer_brand_api.contact_us import handle_contact_us

api = Router(trim_last_slash=True)
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


@api.route("/health-check", methods=["GET", "POST", "OPTIONS"])
def health_check(*args, **kwargs):
    logger.debug("/health-check: " + str((*args, *kwargs)))
    event = args[0]

    if event["requestContext"]["http"]["method"] == "OPTIONS":
        return handle_options_request(event["headers"], ["GET", "POST"])

    response = {
        "message": "🍎 healthy",
        "timestamp": datetime.now().isoformat() + "Z",
    }
    return {
        "statusCode": 200,
        "body": json.dumps(response, ensure_ascii=False),
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "application/json",
        },
    }


@api.route("/contact", methods=["POST", "OPTIONS"])
def contact(*args, **kwargs):
    logger.debug("/contact: " + str((*args, *kwargs)))
    event = args[0]

    if event["requestContext"]["http"]["method"] == "OPTIONS":
        return handle_options_request(event["headers"], ["GET", "POST"])

    body = json.loads(event.get("body", "{}"))
    logger.debug(f"parsing body: {body}")
    handle_contact_us(CustomerTableRecord.from_dict(body))

    response = {
        "message": "contact info received",
        "timestamp": datetime.now().isoformat() + "Z",
    }

    return {
        "statusCode": 200,
        "body": json.dumps(response, ensure_ascii=False),
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "application/json",
        },
    }
