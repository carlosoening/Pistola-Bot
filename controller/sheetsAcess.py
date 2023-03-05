import gspread
from oauth2client.service_account import ServiceAccountCredentials
import tkinter as tk

def infoSheets():

    SPREADSHEET_ID = '[SHEET ID HERE]'

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1

    value = sheet.acell('A1').value