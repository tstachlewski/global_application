import boto3
import time

table = "likes"

boto3.client('dynamodb', region_name='eu-west-1').create_table( TableName=table, StreamSpecification={ 'StreamEnabled': True, 'StreamViewType': 'NEW_AND_OLD_IMAGES'  }, KeySchema=[ { 'AttributeName': 'movie', 'KeyType': 'HASH' } ], AttributeDefinitions=[ { 'AttributeName': 'movie', 'AttributeType': 'S' }, ], ProvisionedThroughput={ 'ReadCapacityUnits': 50, 'WriteCapacityUnits': 50 }, );
boto3.client('dynamodb', region_name='us-west-1').create_table( TableName=table, StreamSpecification={ 'StreamEnabled': True, 'StreamViewType': 'NEW_AND_OLD_IMAGES'  }, KeySchema=[ { 'AttributeName': 'movie', 'KeyType': 'HASH' } ], AttributeDefinitions=[ { 'AttributeName': 'movie', 'AttributeType': 'S' }, ], ProvisionedThroughput={ 'ReadCapacityUnits': 50, 'WriteCapacityUnits': 50 }, );

ddb = boto3.client('dynamodb', region_name='eu-west-1');

ddb.create_global_table( GlobalTableName=table, ReplicationGroup=[ { 'RegionName': 'us-west-1' }, { 'RegionName': 'eu-west-1' } ] )

