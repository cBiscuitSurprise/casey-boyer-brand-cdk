import logging
from typing import cast

from http_router import NotFoundError

from casey_boyer_brand_api.router import router
from casey_boyer_brand_api.router.Match import Match

# configure logging
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("boto3").setLevel(logging.INFO)
logging.getLogger("botocore").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.INFO)

logger = logging.getLogger(__name__)


def handler(event, context):
    logger.debug(f"received event: {event}")

    # event.headers.x-forwarded-for -- Actual IP Address
    # event.requestContext.http.method
    # event.requestContext.http.path
    # event.requestContext.http.userAgent == 'Amazon CloudFront'

    match = router(event["rawPath"], method=event["requestContext"]["http"]["method"])

    try:
        response = cast(Match, match).target(event, pathParameters=match.params)
        logger.debug(f"response: {response}")
        return response
    except NotFoundError as e:
        logger.error(f"bad route: {e}")

        return {
            "statusCode": 404,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": '{"message": "API not found"}',
            "isBase64Encoded": False,
        }
