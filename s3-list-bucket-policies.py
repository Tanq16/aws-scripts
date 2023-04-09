# S3 List Bucket Policies
# -----------------------
# This script takes in the value of a profile that has an
# active session locally and prints out a JSON object with
# keys as bucket names and values as the bucket policies
# for each of those buckets. The result is stored in the
# analysis directory in cwd.

from botocore.exceptions import ClientError
import boto3
import json
import sys

def main(profile_name):
    s3 = boto3.session.Session(profile_name=profile_name)
    s3 = session.resource('s3')
    bucket_list = [bucket.name for bucket in s3.buckets.all()]

    policies = {}

    for bucket_name in bucket_list:
        bucket = s3.Bucket(bucket_name)
        try:
            policy = bucket.Policy().policy
            policies[bucket_name] = json.loads(policy)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
                pass
            else:
                raise e

    if not os.path.exists('./analysis'):
        os.makedirs('analysis')
    f = open('analysis/s3-bucket-policies-' + profile_name + '.json', 'w')
    f.write(json.dumps(policies))
    f.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 s3-list-bucket-policies.py <PROFILE>')
        sys.exit(1)
    profile = sys.argv[1]
    main(profile)
