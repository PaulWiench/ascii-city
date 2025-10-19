import json
import time

import boto3


dynamodb = boto3.resource("dynamodb", region_name="eu-central-1")
table = dynamodb.Table("ascii_city_cache")

def get_cache(
        key: str
) -> dict | None:
    response = table.get_item(Key={"cache_key": key})

    if "Item" in response:
        return json.loads(response["Item"]["value"])

def set_cache(
        key: str,
        value: dict,
        ttl_days: int = 7
) -> None:
    table.put_item(
        Item = {
            "cache_key": key,
            "value": json.dumps(value),
            "ttl": int(time.time() + ttl_days * 86400)
        }
    )
