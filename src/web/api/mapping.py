smart_api_mapping = {
    "_doc": {
        "dynamic_templates": [
            {
                "ignore_example_field": {
                    "match": "example",
                    "mapping": {
                        "index": False
                    }
                }
            },
            {
                "ignore_ref_field": {
                    "match": "$ref",
                    "mapping": {
                        "index": False
                    }
                }
            },
            {
                "ignore_schema_field": {
                    "match": "schema",
                    "mapping": {
                        "enabled": False
                    }
                }
            },
            {
                "ignore_content_field": {
                    "match": "content",
                    "mapping": {
                        "enabled": False
                    }
                }
            },
            # this must be the last template
            {
                "template_1": {
                    "match": "*",
                    "match_mapping_type": "string",
                    "mapping": {
                        "type": "text",
                        "index": True,
                        "ignore_malformed": True,
                        "fields": {
                                "raw": {
                                    "type": "keyword"
                                }
                        }
                    }
                }
            }
        ],
        "properties": {
            "components": {
                "enabled": False
            },
            "definitions": {
                "enabled": False
            },
            "~raw": {
                "type": "binary"
            }
        }
    }
}
