# S3 Size & Number of Objects per Bucket
# --------------------------------------
# This script takes in the value of a profile that has an
# active session locally and prints out the name of all
# buckets within that account and a count of the number
# of objects along with the total size of each bucket.

import sys
import boto3
import threading

threadLimiter = threading.BoundedSemaphore(24)

class BucketCounterThread(threading.Thread):
    def __init__(self, bucket_name, sess):
        threading.Thread.__init__(self)
        self.bucket_name = bucket_name
        self.sess = sess

    def run(self):
        threadLimiter.acquire()
        try:
            self.run_limited()
        finally:
            threadLimiter.release()

    def run_limited(self):
        s3 = self.sess.resource('s3')
        bucket = s3.Bucket(self.bucket_name)
        count, size = 0, 0
        for obj in bucket.objects.all():
            count += 1
            size += obj.size
        size = convert_size(size)
        print(f"{size} ({count})  :  {self.bucket_name}")

def convert_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0 or unit == 'TB':
            break
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} {unit}"

def main(profile):
    session = boto3.Session(profile_name=profile)
    s3 = session.resource('s3')
    bucket_names = [bucket.name for bucket in s3.buckets.all()]

    threads = []
    for bucket_name in bucket_names:
        t = BucketCounterThread(bucket_name, session)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 s3-num-objects.py <PROFILE>")
        sys.exit(1)
    profile = sys.argv[1]
    main(profile)
