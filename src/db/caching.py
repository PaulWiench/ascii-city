import boto3
import json


dynamodb = boto3.resource("dynamodb", region_name="eu-central-1")
table = dynamodb.Table("ascii_city_cache")

def get_cache(
        key: str
) -> dict | None:
    response = table.get_item(Key={"cache_key": key})

    if "Item" in response:
        return json.loads(response["Item"]["value"])
