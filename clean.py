import boto3
import random
import string


print("Cleaning");

s3 = boto3.client('s3');
s3r = boto3.resource('s3');
buckets = s3.list_buckets()["Buckets"]

for bucket in buckets:
    bucketName = bucket["Name"]
    print(" - BUCKET: " + bucketName);
    br = s3r.Bucket(bucketName)
    br.objects.all().delete()
    s3.delete_bucket( Bucket=bucketName )
                
            