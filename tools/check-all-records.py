"""

Usage:
    check-all-records.py <data_group> <data_type> [--schema-path=<schema_path>]

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


def data_type_schema_path(data_type, schema_path):
    return os.path.join(schema_path, 'data-types', '{}.json'.format(data_type))


def data_set_schema_path(data_group, data_type, schema_path):
    return os.path.join(schema_path, 'data-sets', data_group, '{}.json'.format(data_type))


def load_schema(data_group, data_type, schema_path=None):
    if schema_path is None:
        schema_path = calculate_schema_path()
    schema = {
        "description": "Combined schema for a data-set",
        "definitions": {
            "root": load_json_schema(os.path.join(schema_path, 'root.json')),
        },
        "allOf": [ {"$ref": "#/definitions/root"} ]
    }
    try:
        schema['definitions']['data-type'] = load_json_schema(
            data_type_schema_path(data_type, schema_path))
        schema['allOf'].append({"$ref": "#/definitions/data-type"})

        schema['definitions']['data-set'] = load_json_schema(
            data_set_schema_path(data_group, data_type, schema_path))
        schema['allOf'].append({"$ref": "#/definitions/data-set"})
    except IOError:
        pass
    return schema


def load_records(data_group, data_type):
    url = 'https://www.performance.service.gov.uk/data/{}/{}'.format(data_group, data_type)
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
    print('data group: {}'.format(arguments['<data_group>']))
    print('data type: {}'.format(arguments['<data_type>']))

    print('Loading schema')
    schema = load_schema(arguments['<data_group>'], arguments['<data_type>'], arguments['--schema-path'])
    print('Loading records')
    records = load_records(arguments['<data_group>'], arguments['<data_type>'])

    print('Validating first 1000')
    start = datetime.now()
    validate_records(schema, records)
    elapsed = datetime.now() - start

    print('  took: {}'.format(elapsed))
    print('  per record: {}'.format(elapsed / 1000))


if __name__ == "__main__":
    main()
