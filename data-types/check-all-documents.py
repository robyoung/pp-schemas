import sys
import json
import functools

import requests
import jsonschema


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
    if len(sys.argv) != 3:
        print("usage: python {} [data-set url] [path to schema]".format(
            sys.argv[0]))
        sys.exit(1)

    _, data_set_url, path_to_schema = sys.argv

    print("Loading JSON schema")
    schema = load_json_schema(path_to_schema)
    
    print("Loading documents")
    documents = load_data_set(data_set_url)

    print("Validating documents")
    map(functools.partial(validate, schema), documents)

if __name__ == "__main__":
    main()
