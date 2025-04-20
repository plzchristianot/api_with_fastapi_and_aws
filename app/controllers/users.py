from fastapi import FastAPI, BackgroundTasks
import boto3
import psycopg2
import pandas as pd
import numpy as np

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

users = table.scan()['Items']

df = pd.DataFrame(users)

print(df.describe())