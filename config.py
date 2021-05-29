import os
from dotenv import load_dotenv

load_dotenv()

user = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')
database = os.environ.get('POSTGRES_DB')

DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
