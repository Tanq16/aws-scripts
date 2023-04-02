# S3 Number of Objects per Bucket
# -------------------------------
# This script takes in the value of a profile that has an
# active session locally and prints out the name of all
# buckets within that account and a count of the number
# of objects along with the total size of each bucket.

import sys
import boto3
import concurrent.futures

def convert_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0 or unit == 'TB':
            break
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} {unit}"

def run_enumerator(bucket_name,sess):
    s3 = sess.resource('s3')
    bucket = s3.Bucket(bucket_name)
    count, size = 0, 0
    for obj in bucket.objects.all():
        count += 1
        size += obj.size
    size = convert_size(size)
    print(f"{size} ({count})  :  {bucket_name}")

def main(profile):
    session = boto3.Session(profile_name=profile)
    s3 = session.resource('s3')
    bucket_names = [bucket.name for bucket in s3.buckets.all()]
    for bucket_name in bucket_names:
        run_enumerator(bucket_name, session)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 s3-num-objects.py <PROFILE>")
        sys.exit(1)
    profile = sys.argv[1]
    main(profile)