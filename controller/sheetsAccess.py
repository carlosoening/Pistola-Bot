import gspread
from oauth2client.service_account import ServiceAccountCredentials

def infoSheets(sheet_id: str):

    SPREADSHEET_ID = sheet_id

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1

    value = sheet.acell('A1').value