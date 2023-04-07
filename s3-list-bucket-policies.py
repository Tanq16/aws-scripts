# S3 List Bucket Policies
# -----------------------
# This script takes in the value of a profile that has an
# active session locally and prints out a JSON object with
# keys as bucket names and values as the bucket policies
# for each of those buckets. Pipe to jq for filtering.

from botocore.exceptions import ClientError
import boto3
import json
import sys

def main(profile_name):
    s3 = boto3.session.Session(profile_name=profile_name).client('s3')
    bucket_list = [bucket['Name'] for bucket in s3.list_buckets()['Buckets']]

    policies = {}

    for bucket in bucket_list:
        try:
            policy = s3.get_bucket_policy(Bucket=bucket)['Policy']
            policies[bucket] = json.loads(policy)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
                pass
            else:
                raise e

    print(json.dumps(policies))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 s3-list-bucket-policies.py <PROFILE>")
        sys.exit(1)
    profile = sys.argv[1]
    main(profile)
