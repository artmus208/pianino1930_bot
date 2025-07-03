from os import environ
from dotenv import load_dotenv
load_dotenv("./envs/artmus_bot.env")

DB_NAME=environ.get("DB_NAME")
DB_USER=environ.get("DB_USER")
DB_HOST=environ.get("DB_HOST")
DB_PORT=environ.get("DB_PORT")
DB_PASS=environ.get("DB_PASS")
TG_TOKEN=environ.get("TG_TOKEN")
TG_ADMINS=list(map(int, environ.get("TG_ADMINS").split(',')))
GOOGLE_CREDITINALS_JSON=environ.get("GOOGLE_CREDITINALS_JSON")
GOOGLE_SPREADSHEET_NAME=environ.get("GOOGLE_SPREADSHEET_NAME")

print(f"{DB_HOST=}")
print(f"{TG_ADMINS=}")
print(f"{GOOGLE_CREDITINALS_JSON=}")