# EBS Unencrypted Volumes & Snapshots
# -----------------------------------
# This script takes in the value of a profile that has an
# active session locally and prints out the number of
# unecnrypted volumes and snapshots across all regions for
# that account. It also prints the number of unencrypted
# volumes that are attached and in use.

import boto3
import sys

def list_ebs_volumes(profile):
    session = boto3.Session(profile_name=profile)
    ec2_client = session.client('ec2', region_name='us-west-2')

    # list all regions
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    unencrypted_volumes = 0
    unencrypted_snapshots = 0
    unencrypted_attached_volumes = 0

    for region in regions:
        ec2_client = session.client('ec2', region_name=region)

        volumes = ec2_client.describe_volumes(MaxResults=9999)['Volumes']
        snapshots = ec2_client.describe_snapshots(OwnerIds=['self'], MaxResults=9999)['Snapshots']

        # Check each volume and snapshot for encryption and attachment
        for volume in volumes:
            if 'Encrypted' in volume and not volume['Encrypted']:
                unencrypted_volumes += 1
                if len(volume['Attachments']) > 0 and volume['State'] == 'in-use':
                    unencrypted_attached_volumes += 1
        for snapshot in snapshots:
            if 'Encrypted' in snapshot and not snapshot['Encrypted']:
                unencrypted_snapshots += 1

    print("Unencrypted Volumes: ", unencrypted_volumes)
    print("Unencrypted Snapshots: ", unencrypted_snapshots)
    print("Unencrypted Volumes (attached & in-use): ", unencrypted_attached_volumes)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 ebs-unencrypted-volumes-snapshots.py <PROFILE>")
        sys.exit(1)
    profile = sys.argv[1]
    list_ebs_volumes(profile)
