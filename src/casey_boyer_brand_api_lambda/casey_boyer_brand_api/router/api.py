from datetime import datetime
import logging
import json

from http_router import Router

from casey_boyer_brand_api.aws.CustomerTableRecord import CustomerTableRecord
from casey_boyer_brand_api.contact_us import handle_contact_us
from casey_boyer_brand_api.utils.string import capitalize
from casey_boyer_brand_api.router.projects import router_projects
from casey_boyer_brand_api.utils.http import handle_options_request

logger = logging.getLogger(__name__)

api = Router(trim_last_slash=True)
api.route("/projects")(router_projects)


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
    handle_contact_us(
        CustomerTableRecord.from_dict({capitalize(k): v for k, v in body.items()})
    )

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
