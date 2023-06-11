import enum
from typing import Dict


def json_dump(obj: Dict) -> Dict:
    valid_json: Dict[str, str] = {}

    for k, v in obj.items():
        if isinstance(v, enum.Enum):
            v = v.value
        else:
            v = str(v)
        valid_json[k] = v

    return valid_json
