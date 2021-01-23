import boto3
import time

table = "likes"

boto3.resource('dynamodb').Table(table).put_item( Item={ 'movie': '1', 'likes': 0 });
boto3.resource('dynamodb').Table(table).put_item( Item={ 'movie': '2', 'likes': 0 });
boto3.resource('dynamodb').Table(table).put_item( Item={ 'movie': '3', 'likes': 0 });