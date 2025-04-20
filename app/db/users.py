import boto3
from fastapi import FastAPI
import psycopg2

conn = psycopg2.connect(
        host='example.c3mqa60k2ubs.us-west-1.rds.amazonaws.com',
        database='postgres',
        user='postgres',
        password='ultimatez',
        port=5432
    )

db = conn.cursor()

db.execute("CREATE TABLE users (id serial PRIMARY KEY, username varchar, first_name varchar, last_name varchar, age integer, premium bool);")
db.execute("""INSERT INTO users (username, first_name, last_name, age, premium) 
           VALUES (%s, %s, %s, %s, %s);""",
           ("el_plz", "christian", "oviedo", 24, True))

conn.commit()