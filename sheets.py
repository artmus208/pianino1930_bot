#! sheets.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_CREDITINALS_JSON, GOOGLE_SPREADSHEET_NAME
print(GOOGLE_CREDITINALS_JSON)
print(GOOGLE_SPREADSHEET_NAME)
# Подключение к Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDITINALS_JSON, scope)
client = gspread.authorize(credentials)

# Открываем таблицу по названию
spreadsheet = client.open(GOOGLE_SPREADSHEET_NAME)
sheet = spreadsheet.sheet1

def add_participant_to_sheet(name, phone, status, char, consent, time_created):
    sheet.append_row([name, phone, status, char, consent, time_created])



if __name__ == "__main__":
    add_participant_to_sheet("Луиза", "+7 917 221 1428", "АМС","Зритель", "TRUE", "02.07.2025")