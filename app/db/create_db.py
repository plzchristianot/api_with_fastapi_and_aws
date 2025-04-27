# import boto3
# import psycopg2

# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('users')


# info = table.scan()['Items']
# users = []

# for i in info:
#     users.append(i['username'])


# conn = psycopg2.connect(
#             host='example.c3mqa60k2ubs.us-west-1.rds.amazonaws.com',
#             database='postgres',
#             user='postgres',
#             password='ultimatez',
#             port=5432
#         )

# db = conn.cursor()

# db.execute("SELECT username FROM users;")
# data = db.fetchall()
# users_rds = []

# for user in data:
#     res = "".join(user)
#     users_rds.append(res)

# for item in users:
#     if item in users_rds:
#         #agregar aqui la query para hacer la insercion de datos
#         ...