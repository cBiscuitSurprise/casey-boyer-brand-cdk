import logging

from casey_boyer_brand_api.aws import get_contact_us_topic, get_customer_table
from casey_boyer_brand_api.aws.CustomerTableRecord import CustomerTableRecord
from casey_boyer_brand_api.contact_us.contact_us_template import build_message

logger = logging.getLogger(__name__)


def handle_contact_us(input: CustomerTableRecord):
    logger.debug("resolving existing record")
    table = get_customer_table()

    record = None
    if input.Email:
        record = table.get_with_email(input.Email)

    if record is None and input.Phone:
        record = table.get_with_phone(input.Phone)
    else:
        logger.debug("found existing record via email")

    if record is None:
        record = input
    else:
        logger.debug("found existing record via phone")
        record.update_with(input)

    logger.debug("updating record")
    table.update(record)

    # send notification
    logger.debug("sending notification")
    topic = get_contact_us_topic()
    topic.send_email("Home Base Contact Us Submitted", build_message(record))
