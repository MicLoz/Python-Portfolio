from transform import TRANSFORM_FUNCTIONS, TRANSFORM_METADATA

PIPELINE_SCHEMA = {
    "extract": {
        "required": True,
        "type": "dict",
        "required_keys": ["mode"],
        "modes": {
            "internal": {
                "required_keys": []
            },
            "json": {
                "required_keys": ["path"]
            }
        }
    },

    "transform": {
        "required": True,
        "type": "dict",
        "required_keys": ["steps"],
        "steps": {
            "type": "list",
            "item_type": "dict",
            "required_keys": ["op"]
        }
    },

    "load": {
        "required": True,
        "type": "dict",
        "modes": {
            "console": {"required_keys": []},
            "csv": {"required_keys": ["path"]}
        }
    }
}