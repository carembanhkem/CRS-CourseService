from decouple import config as decouple_config

DATABASE_URL = decouple_config("DATABASE_URL", default="")
print(DATABASE_URL)
AWS_REGION = decouple_config("AWS_REGION", default="")
