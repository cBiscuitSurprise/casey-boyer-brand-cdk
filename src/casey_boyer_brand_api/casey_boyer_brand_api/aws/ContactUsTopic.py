from datetime import datetime
import os
from typing import Any


class ContactUsTopic:
    def __init__(self, snsResource) -> None:
        self.target_arn = os.environ["CONTACT_US_TOPIC_ARN"]
        self.topic = snsResource.Topic(self.target_arn)

    def send_email(self, subject: str, message: str):
        self.topic.publish(
            Subject=subject,
            Message=message,
            MessageAttributes={
                "datetime": {
                    "DataType": "String",
                    "StringValue": datetime.now().isoformat(),
                }
            },
        )
