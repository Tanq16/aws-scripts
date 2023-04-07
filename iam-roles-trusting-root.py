# IAM Roles Trusting Root
# -----------------------
# This script navigates the present working directory to
# ingest "combined-gaad.json" to collect all accounts
# present in the file and list out all roles that trust
# the account root for each of the accounts. Pipe to jq
# for easy filtering.
# 
# If an argument is passed, it is read as a file for
# "account_names", and the expected contents are a list
# of account_number:account_alias values. This is then
# used to replace the account number values with their
# aliases.

import json
import sys
import os

def get_account_numbers(data):
    arns = [i['Arn'] for i in data['UserDetailList']]
    arns += [i['Arn'] for i in data['RoleDetailList']]
    arns += [i['Arn'] for i in data['GroupDetailList']]
    account_numbers = list(set([arn.split(':')[4] for arn in arns]))
    return account_numbers

def get_root_trusts(data, account_numbers):
    roles_trusting_root = {}
    for acct in account_numbers:
        root_arn = f"arn:aws:iam::{acct}:root"
        trusting_roles = []
        for role in data['RoleDetailList']:
            role_assume_policy = role['AssumeRolePolicyDocument']
            for statement in role_assume_policy['Statement']:
                if statement['Principal'] == {'AWS': root_arn}:
                    trusting_roles.append(role['Arn'])
        if len(trusting_roles) == 0:
            continue
        roles_trusting_root[acct] = list(set(trusting_roles))
    return roles_trusting_root

def main(data):
    account_numbers = get_account_numbers(data)
    roles_trusting_root = get_root_trusts(data, account_numbers)
    print(json.dumps(roles_trusting_root))

if __name__ == '__main__':
    files = [file for file in os.listdir(".") if file.endswith("gaad.json")]
    if not "combined-gaad.json" in files:
        print("Usage: python3 iam-roles-trusting-root.py\nEnsure that combined-gaad.json in the current directory.")
        sys.exit(1)
    f = open("combined-gaad.json")
    data = json.loads(f.read())
    f.close()
    main(data)
