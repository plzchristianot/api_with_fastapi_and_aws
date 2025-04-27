import boto3
from fastapi import FastAPI
import psycopg2

#connection to RDS hosted on AWS
conn = psycopg2.connect(
        host='example.c3mqa60k2ubs.us-west-1.rds.amazonaws.com',
        database='postgres',
        user='postgres',
        password='ultimatez',
        port=5432
    )

#create a cursor instance to make queries and operations
# db = conn.cursor()