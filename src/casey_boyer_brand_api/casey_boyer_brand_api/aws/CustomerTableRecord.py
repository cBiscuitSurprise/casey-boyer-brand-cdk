from dataclasses import dataclass, field
import inspect
from typing import Any, Dict, Optional
from uuid import uuid4


def new_id():
    return str(uuid4())


@dataclass
class CustomerTableRecord:
    id: Optional[str] = field(default_factory=new_id)
    Name: Optional[str] = None
    Email: Optional[str] = None
    Phone: Optional[str] = None
    Message: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, input: Dict[str, Any]):
        params = {
            k: v for k, v in input.items() if k in inspect.signature(cls).parameters
        }
        extra = {
            k: v for k, v in input.items() if k not in inspect.signature(cls).parameters
        }
        if "extra" in input:
            extra["extra"] = input["extra"]
        params["extra"] = extra
        return cls(**params)

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
                "Message": {"Action": "PUT", "Value": self.Phone},
                **{k: {"Action": "PUT", "Value": v} for k, v in self.extra.items()},
            },
        }
