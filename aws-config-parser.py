# AWS Config Parser
# -----------------
# Run as python3 aws-config-parse.py | jq '<your-commands>'
# using jq, print values for access keys; example:
# for devacc's secret access key: `jq '.devacc.sak'`.
# If passed with the parameter gaad-generate, it will
# instead download and store get-account-authorization-
# details for all the profiles as JSON files.

import os
import sys
import json
import boto3
from configparser import ConfigParser

def get_aws_profiles():
    config = ConfigParser()
    config.read(os.path.expanduser('~/.aws/credentials'))

    profiles = {}
    # parse for access key IDs and secret access keys
    for section in config.sections():
        profile = {
            'aki': config[section]['aws_access_key_id'],
            'sak': config[section]['aws_secret_access_key'],
        }
        # parse for session token if present (STS sessions)
        if 'aws_session_token' in config[section]:
            profile['st'] = config[section]['aws_session_token']
        profiles[section] = profile

    return profiles

def main():
    profiles = get_aws_profiles()
    print(json.dumps(profiles))
    if len(sys.argv) > 1 and sys.argv[1] == 'gaad-generate':
        if not os.path.exists('./gaads'):
            os.makedirs('gaads')
        for i in profiles.keys():
            if i == 'default':
                continue
            session = boto3.Session(profile_name=i)
            iam = session.client('iam')
            account_authorization_details = iam.get_account_authorization_details()
            with open(i + '-gaad.json', 'w') as f:
                f.write(json.dumps(account_authorization_details))

if __name__ == '__main__':
    main()
