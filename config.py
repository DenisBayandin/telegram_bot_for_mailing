from decouple import  config


TG_TOKEN = config("TG_TOKEN", cast=str)
ADMIN_ID = config("ADMIN_ID", cast=int)
