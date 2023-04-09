# IAM Old & Active Keys
# ---------------------
# This script takes in the value of a profile that has an
# active session locally and prints out a json object with
# a key "data" that has a list of users, each of which is
# a dictionary with keys "user" (the username) and "keys"
# (a list of all >90 day old active keys for that user).
# `jq` can be used to modify the output and print data as
# necessary.

import sys
import boto3
import json
from datetime import datetime, timedelta

def get_active_keys(iam_client, user_name):
    active_keys = []
    response = iam_client.list_access_keys(UserName=user_name)
    for access_key in response['AccessKeyMetadata']:
        if access_key['Status'] == 'Active':
            last_rotated = access_key['CreateDate'].replace(tzinfo=None)
            if datetime.utcnow() - last_rotated > timedelta(days=90):
                active_keys.append(access_key['AccessKeyId'] + ' :: ' + access_key['CreateDate'].strftime('%Y-%m-%d'))
    return active_keys

def main(profile_name):
    session = boto3.Session(profile_name=profile_name)
    iam_client = session.client('iam')

    users = []
    response = iam_client.list_users(MaxItems=999)
    for user in response['Users']:
        user_name = user['UserName']
        active_keys = get_active_keys(iam_client, user_name)
        if active_keys:
            users.append({'user': user_name, 'keys': active_keys})

    print(json.dumps({'data':users}))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 iam-old-active-keys.py <PROFILE>')
        sys.exit(1)
    profile = sys.argv[1]
    main(profile)
