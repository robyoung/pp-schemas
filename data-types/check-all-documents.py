import sys
import json
import functools

import requests
import jsonschema


def parse_args(args):
    if len(args) != 3:
        usage = "usage: python {} [data-set url] [path to schema]".format(
                args[0])
        raise SystemExit(usage)
    return args[1], args[2]


def load_json_schema(path_to_schema):
    with open(path_to_schema) as schema_file:
        return json.load(schema_file)


def load_data_set(url):
    return requests.get(url).json().get('data', [])


def validate(schema, document):
    jsonschema.validate(
            document,
            schema,
            format_checker=jsonschema.FormatChecker())


def main():
    data_set_url, path_to_schema = parse_args(sys.argv)

    print("Loading JSON schema")
    schema = load_json_schema(path_to_schema)
    
    print("Loading documents")
    documents = load_data_set(data_set_url)

    print("Validating documents")
    map(functools.partial(validate, schema), documents)

if __name__ == "__main__":
    main()
