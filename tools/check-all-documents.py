"""

Usage:
    check-all-documents.py <data_set_url> <data_type> [--schema-path=<schema_path>]

Options:
    -h --help                   Show this screen
    --schema-path=<schema_path> Path to where the schemas are

"""
import os
import json
from datetime import datetime

import requests
import jsonschema

from docopt import docopt


def load_json_schema(path_to_schema):
    with open(path_to_schema) as schema_file:
        return json.load(schema_file)


def validate(schema, record):
    jsonschema.validate(
            record,
            schema,
            format_checker=jsonschema.FormatChecker())


def validate_records(schema, records):
    for record in records:
        validate(schema, record)


def calculate_schema_path():
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'schemas'))


def load_schema(data_type, schema_path=None):
    if schema_path is None:
        schema_path = calculate_schema_path()
    root_schema = load_json_schema(os.path.join(schema_path, 'root.json'))
    type_schema = load_json_schema(os.path.join(schema_path, 'data-types',
                                                '{}.json'.format(data_type)))
    return {
        "allOf": [
            root_schema,
            type_schema,
        ]
    }


def load_records(url):
    data = requests.get(url).json().get('data', [])
    records = []
    for i, record in enumerate(data):
        for key in record.keys():
            if key.endswith('_at'):
                del record[key]
        records.append(record)
        if i > 1000:
            break
    return records


def main():
    arguments = docopt(__doc__)

    print('Loading schema')
    schema = load_schema(arguments['<data_type>'], arguments['--schema-path'])
    print('Loading records')
    records = load_records(arguments['<data_set_url>'])

    print('Validating first 1000')
    start = datetime.now()
    validate_records(schema, records)
    elapsed = datetime.now() - start

    print('  took: {}'.format(elapsed))
    print('  per record: {}'.format(elapsed / 1000))


if __name__ == "__main__":
    main()
