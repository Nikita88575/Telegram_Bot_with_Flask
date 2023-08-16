import os
from dotenv import load_dotenv

load_dotenv()

BOT_API = str(os.getenv('API'))
SECRET_KEY = str(os.getenv('SECRET_KEY'))

admin_id = [
    683880937
]

DEBUG = str(os.getenv('DEBUG'))

IP = os.getenv('IP')
PGUSER = str(os.getenv('PGUSER'))
PGPASSWORD = str(os.getenv('PGPASSWORD'))
DATABASE = str(os.getenv('DATABASE'))
POSTGERS_URI = f'postgresql://{PGUSER}:{PGPASSWORD}@{IP}/{DATABASE}'