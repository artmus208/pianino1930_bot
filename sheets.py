#! sheets.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import GOOGLE_CREDITINALS_JSON, GOOGLE_SPREADSHEET_NAME
from datetime import datetime, timedelta
print(f"{GOOGLE_CREDITINALS_JSON=}")
print(f"{GOOGLE_SPREADSHEET_NAME=}")
# Подключение к Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDITINALS_JSON, scope)
client = gspread.authorize(credentials)

# Открываем таблицу по названию
spreadsheet = client.open(GOOGLE_SPREADSHEET_NAME)
sheet = spreadsheet.sheet1

def add_participant_to_sheet(name, phone, status, char, consent, time_created):
    sheet.append_row([name, phone, status, char, consent, time_created])


def create_new_sheet(sheet_title):
    sheet_names = [s.title for s in spreadsheet.worksheets()]
    sheet = None
    if sheet_title not in sheet_names:
        sheet = spreadsheet.add_worksheet(
            title=sheet_title, 
            rows=100, 
            cols=100
        )
    else:
        sheet = spreadsheet.worksheet(f"Вызов {sheet_title}")
        print("На этот день лист уже создан")
        
    return sheet

def get_sheet_by_title(title: str):
    return spreadsheet.worksheet(title)


def insert_in_certain_sheet(sheet, name, phone, status, char, consent, time_created):
    sheet.append_row([name, phone, status, char, consent, time_created])
    
if __name__ == "__main__":
    create_new_sheet()

