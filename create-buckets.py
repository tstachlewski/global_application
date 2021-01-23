import boto3
import json

bucket_suffix = 'summit-underthecloud-16'

s3 = boto3.client('s3', region_name='eu-west-1')
s3.create_bucket(  Bucket= bucket_suffix + '-europe', CreateBucketConfiguration={ 'LocationConstraint': 'eu-west-1'});
s3.put_bucket_versioning( Bucket=bucket_suffix + '-europe', VersioningConfiguration={ 'MFADelete': 'Disabled', 'Status': 'Enabled' } )

s3 = boto3.client('s3', region_name='us-west-1')
s3.create_bucket( Bucket= bucket_suffix + '-usa', CreateBucketConfiguration={ 'LocationConstraint': 'us-west-1'});
s3.put_bucket_versioning( Bucket=bucket_suffix + '-usa', VersioningConfiguration={ 'MFADelete': 'Disabled', 'Status': 'Enabled' } )


iam = boto3.client('iam')
trust_relationship_policy = { "Version": "2012-10-17", "Statement": [ { "Effect": "Allow", "Principal": { "Service": "s3.amazonaws.com" }, "Action": "sts:AssumeRole" } ] }
iam.create_role( RoleName= bucket_suffix + "ReplicationRole", AssumeRolePolicyDocument=json.dumps(trust_relationship_policy) );
iam.attach_role_policy( RoleName = bucket_suffix + "ReplicationRole", PolicyArn='arn:aws:iam::aws:policy/AmazonS3FullAccess' )
roleArn = iam.get_role(RoleName=bucket_suffix + "ReplicationRole")["Role"]["Arn"]

s3 = boto3.client('s3', region_name='eu-west-1')
s3.put_bucket_replication( Bucket=bucket_suffix + '-europe', ReplicationConfiguration={ 'Role': roleArn, 'Rules': [ { 'Destination': { 'Bucket': 'arn:aws:s3:::' + bucket_suffix + '-usa', 'StorageClass': 'STANDARD', }, 'Prefix': '', 'Status': 'Enabled', }, ], }, )
s3 = boto3.client('s3', region_name='us-west-1')
s3.put_bucket_replication( Bucket=bucket_suffix + '-usa', ReplicationConfiguration={ 'Role': roleArn, 'Rules': [ { 'Destination': { 'Bucket': 'arn:aws:s3:::' + bucket_suffix + '-europe', 'StorageClass': 'STANDARD', }, 'Prefix': '', 'Status': 'Enabled', }, ], }, )
