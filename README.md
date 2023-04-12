# AWS Scripts Collection

This repo contains a collection of helpful AWS security-related scripts. The best way to use this repo is to clone it in a specific location and call the scripts with `bash` or `python` or `python3` directly. Example &rarr;

```bash
git clone https://github.com/tanq16/aws-scripts.git /opt/aws-scripts/
```

The following scripts currently live in the repo &rarr;

**Utility**

* `aws-multi-session.sh` &rarr; A script to assume a given role across multiple accounts via an IAM user.
* `aws-config-parser.py` &rarr; A script to print out the credentials from the `~/.aws/credentials` file in JSON format for easy `jq` parsing.
* `aws-ip-cidr-check.py` &rarr; A script that takes in an IP or a CIDR range to check if they belong to AWS.

**IAM Analysis**

* `iam-gaad-combine.py` &rarr; A script that combines the result of the multiple JSON files resulting from `aws iam get-account-authorization-details --profile $PRFL > $PRFL-gaad.json`.
* `iam-roles-trusting-root.py` &rarr; A script to print out JSON of all roles that trust account root for all accounts in combined gaad.
* `iam-principal-condenser.py` &rarr; A script that condenses users and roles into a single collection of all their associated policies (including groups and attached policies).
* `iam-permission-condenser.py` &rarr; A script that condenses permissions of users and roles into a single collection of all action, resource combinations.

**Service-Based**

* `iam-old-active-keys.py` &rarr; A script to print out all users and their access keys when the keys have age higher than 90 days for a given account profile.
* `ebs-unencrypted-volsnaps.py` &rarr; A script to print number of unencrypted volumes (all and those attached & in use) and snapshots for a given account profile.
* `s3-num-objects.py` &rarr; A script to print out number of objects per bucket for a given account profile.
* `s3-list-bucket-policies.py` &rarr; A script to print out key value pairs of bucket name and its policy in JSON to stdout.
