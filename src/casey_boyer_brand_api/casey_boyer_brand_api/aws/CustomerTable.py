from boto3.dynamodb.conditions import Key
from typing import Any, Dict, List, Optional
from casey_boyer_brand_api.aws.CustomerTableRecord import CustomerTableRecord


class CustomerTable:
    _TABLE_NAME = "CaseyBoyerBrandCustomers"

    def __init__(self, ddbResource) -> None:
        self.table = ddbResource.Table(self._TABLE_NAME)

    def update(self, record: CustomerTableRecord):
        self.table.update_item(**record.toDynamoDbRecord())

    def get_with_id(self, id: str) -> Optional[CustomerTableRecord]:
        response = self.table.get_item(
            Key={
                "Id": id,
            }
        )

        if response.get("Item") is None:
            return None
        else:
            return self._create_customer_table_record(response.get("Item"))

    def get_with_email(self, email: str) -> Optional[CustomerTableRecord]:
        response = self.table.query(
            IndexName="CustomerEmailIndex",
            Select="ALL_ATTRIBUTES",
            KeyConditionExpression=Key("Email").eq(email),
        )
        return self._resolve_query(response.get("Items", []))

    def get_with_phone(self, phone: str) -> Optional[CustomerTableRecord]:
        response = self.table.query(
            IndexName="CustomerPhoneIndex",
            Select="ALL_ATTRIBUTES",
            KeyConditionExpression=Key("Phone").eq(phone),
        )
        return self._resolve_query(response.get("Items", []))

    def _resolve_query(
        self, items: List[Dict[str, Any]]
    ) -> Optional[CustomerTableRecord]:
        if items:
            return self._create_customer_table_record(items[0])

        return None

    def _create_customer_table_record(self, item: Dict[str, Any]):
        return CustomerTableRecord.from_dict(item)
