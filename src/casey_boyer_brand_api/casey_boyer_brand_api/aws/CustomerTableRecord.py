from typing import Any, Dict, Optional
from uuid import uuid4


def new_id():
    return str(uuid4())


class CustomerTableRecord:
    def __init__(
        self,
        *,
        id: Optional[str] = None,
        Name: Optional[str] = None,
        Email: Optional[str] = None,
        Phone: Optional[str] = None,
        **kwargs: Dict[str, Any],
    ):
        self.id = new_id() if id is None else id
        self.Name = Name
        self.Email = Email
        self.Phone = Phone
        self.extra = kwargs

    def update_with(self, update: "CustomerTableRecord"):
        if update.Name is not None:
            self.Name = update.Name

        if update.Email is not None:
            self.Email = update.Email

        if update.Phone is not None:
            self.Phone = update.Phone

        if update.extra is not None:
            self.extra = update.extra

    def toDynamoDbRecord(self):
        return {
            "Key": {"Id": self.id},
            "AttributeUpdates": {
                "Name": {"Action": "PUT", "Value": self.Name},
                "Email": {"Action": "PUT", "Value": self.Email},
                "Phone": {"Action": "PUT", "Value": self.Phone},
                **{k: {"Action": "PUT", "Value": v} for k, v in self.extra.items()},
            },
        }
