"""
This script is used to update secrets in zappa_settings.json and used
by zappa-deploy.sh script.
"""
import json
import argparse

# Argument parser
PARSER = argparse.ArgumentParser(
    description='Set secrets in zappa_settings.json'
)

PARSER.add_argument(
    'env',
    nargs='?',
    help='Environment name'
)

PARSER.add_argument(
    '--single-source-api-key',
    nargs='?',
    default='',
    help='SingleSource api key'
)

PARSER.add_argument(
    '--zappa-settings',
    nargs='?',
    default='zappa_settings.json',
    help='Zappa config file'
)

ARGS = PARSER.parse_args()

if __name__ == '__main__':
    with open(ARGS.zappa_settings, 'r+') as f:
        data = json.load(f)
        data[ARGS.env]['aws_environment_variables']['SINGLE_SOURCE_API_KEY'] = ARGS.single_source_api_key
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
