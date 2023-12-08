import json


def obj_to_dict_items(ls: list) -> str:
    return json.loads(
        json.dumps(
            {"items": [i.model_dump(exclude_defaults=True) for i in ls]}, default=str
        )
    )


def obj_to_dict(obj) -> str:
    return json.loads(json.dumps(obj.model_dump(exclude_defaults=True), default=str))


def dict_to_tuples(test_data: dict, test_name: str) -> list[tuple]:
    td = test_data.get("all_tests").get(test_name)
    return [tuple(t.values()) for t in td]
