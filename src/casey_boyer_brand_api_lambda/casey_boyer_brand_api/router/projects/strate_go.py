from dataclasses import asdict
import json
import logging

from http_router import Router

from casey_boyer_brand_api.projects import strate_go
from casey_boyer_brand_api.utils.http import handle_options_request


logger = logging.getLogger(__name__)

router_strate_go = Router(trim_last_slash=True)


@router_strate_go.route("/connect", methods=["GET", "OPTIONS"])
def connect(*args, **kwargs):
    logger.debug("/project/strate-go/connect: " + str((*args, *kwargs)))
    event = args[0]

    if event["requestContext"]["http"]["method"] == "OPTIONS":
        return handle_options_request(event["headers"], ["GET", "POST"])

    response = strate_go.get_server()

    return {
        "statusCode": 200,
        "body": json.dumps(asdict(response), ensure_ascii=False),
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "application/json",
        },
    }
