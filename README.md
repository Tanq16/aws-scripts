# AWS Scripts Collection

This repo contains a collection of helpful AWS security-related scripts. The best way to use this repo is to clone it in a specific location and call the scripts with `bash` or `python` or `python3` directly. Example &rarr;

```bash
git clone https://github.com/tanq16/aws-scripts.git /opt/aws-scripts/
```

The following scripts currently live in the repo &rarr;

**General**

* `aws-multi-session.sh` &rarr; A script to assume a given role across multiple accounts via an IAM user.
* `iam-gaad-combine.py` &rarr; A script that combines the result of the multiple JSON files resulting from `aws iam get-account-authorization-details --profile $PRFL > $PRFL-gaad.json`.
* `aws-config-parser.py` &rarr; A script to print out the credentials from the `~/.aws/credentials` file in JSON format for easy `jq` parsing.

**Account Specific**

* `ebs-unencrypted-volsnaps.py` &rarr; A script to print number of unencrypted volumes (all and those attached & in use) and snapshots for a given account profile.
* `iam-old-active-keys.py` &rarr; A script to print out all users and their access keys when the keys have age higher than 90 days for a given account profile.
* `s3-num-objects.py` &rarr; A script to print out number of objects per bucket for a given account profile.
