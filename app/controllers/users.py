from fastapi import FastAPI, BackgroundTasks
import boto3
import psycopg2
import pandas as pd
import numpy as np
import json

from app.responses.users import ErrorResponse

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

async def clean_up():
    conn = psycopg2.connect(
            host='example.c3mqa60k2ubs.us-west-1.rds.amazonaws.com',
            database='postgres',
            user='postgres',
            password='ultimatez',
            port=5432
        )

    db = conn.cursor()

    users = table.scan()['Items']
    users_nosql = [i['username'] for i in users]


    df = pd.DataFrame(users)

    new_df = df[["username", "first_name", "last_name", "age", "premium"]]

    json_str = new_df.to_json(orient="index")
    json_final = json.loads(json_str)

    db.execute("SELECT username FROM users;")

    data = db.fetchall()
    users_rds = ["".join(user) for user in data]
    

    #condition to check if the user is already in the rds db
    for item in users_nosql:
        if item not in users_rds:
            for key, value in json_final.items():
                if value["username"] == item:
                    db.execute("""INSERT INTO users (username, first_name, last_name, age, premium) 
                            VALUES (%s, %s, %s, %s, %s);""",
                            (value['username'], value['first_name'], value['last_name'], value['age'], value['premium']))
                    conn.commit()
        
    db.close()
    conn.close()

