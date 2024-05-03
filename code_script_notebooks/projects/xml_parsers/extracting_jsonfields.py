import json


def extract_field_names(obj):
    """Extracts all field names from a nested JSON object.

    Args:
    obj: A JSON object.

    Returns:
    A list of all field names in the JSON object.
    """

    field_names = []

    def _extract_field_names(obj, field_names):
        if isinstance(obj, dict):
            for key, value in obj.items():
                field_names.append(key)
                _extract_field_names(value, field_names)
        elif isinstance(obj, list):
            for item in obj:
                _extract_field_names(item, field_names)

    _extract_field_names(obj, field_names)
    return field_names


# Example usage:

nested_json_data = """
{
  "name": "John Doe",
  "age": 30,
  "address": {
    "street": "123 Main Street",
    "city": "San Francisco",
    "state": "CA",
    "zip": "94105"
  }
}
"""



field_names = extract_field_names(json.loads(nested_json_data))

print(field_names)