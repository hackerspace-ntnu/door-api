import json


def decode_json_bytes(json_bytes):
    return json.loads(json_bytes.decode('utf-8'))
