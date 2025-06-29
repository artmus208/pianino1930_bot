#! sheets.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Подключение к Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(credentials)

# Открываем таблицу по названию
spreadsheet = client.open("Участники массовки")
sheet = spreadsheet.sheet1

def add_participant_to_sheet(name, age, phone, consent):
    sheet.append_row([name, str(age), phone, consent])
