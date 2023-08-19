from typing import Optional

import boto3

from casey_boyer_brand_api.aws.ContactUsTopic import ContactUsTopic
from casey_boyer_brand_api.aws.CustomerTable import CustomerTable

_session: Optional[boto3.Session] = None
_customer_table: Optional[CustomerTable] = None
_contact_us_topic: Optional[ContactUsTopic] = None


def get_session():
    global _session
    if _session is None:
        _session = boto3.Session()

    return _session


def get_ddb_resource():
    return get_session().resource("dynamodb")


def get_sns_resource():
    return get_session().resource("sns")


def get_customer_table():
    global _customer_table
    if _customer_table is None:
        _customer_table = CustomerTable(get_ddb_resource())

    return _customer_table


def get_contact_us_topic():
    global _contact_us_topic
    if _contact_us_topic is None:
        _contact_us_topic = ContactUsTopic(get_sns_resource())

    return _contact_us_topic
