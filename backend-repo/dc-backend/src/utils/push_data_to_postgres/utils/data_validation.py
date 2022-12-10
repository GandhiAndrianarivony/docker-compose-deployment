from typing import List


def validate(list_obj: List[dict], model):
    data = []
    for lo in list_obj:
        data.append(dict(model.parse_obj(lo)))
    return data

