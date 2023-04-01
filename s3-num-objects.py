# S3 Number of Objects per Bucket
# -------------------------------
# This script takes in the value of a profile that has an
# active session locally and prints out the name of all
# buckets within that account and a count of the number
# of objects within each of the buckets.

import sys
import boto3
from concurrent.futures import ThreadPoolExecutor

def check_bucket(bucket_name,sess):
    s3 = sess.resource('s3')
    bucket = s3.Bucket(bucket_name)
    summa = sum(1 for _ in bucket.objects.filter())
    print(bucket_name, ":", summa)

def main(profile):
    session = boto3.Session(profile_name=profile)
    s3 = session.resource('s3')
    bucket_names = [bucket.name for bucket in s3.buckets.all()]

    with ThreadPoolExecutor(max_workers=8) as executor:
        for bucket_name in bucket_names:
            executor.submit(check_bucket, bucket_name, session)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 s3-num-objects.py <PROFILE>")
        sys.exit(1)
    profile = sys.argv[1]
    main(profile)