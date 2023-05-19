import gspread
from oauth2client.service_account import ServiceAccountCredentials

def infoSheets(sheet_id: str):

    key_start = 'Inicio'
    key_final = 'Fim'

    records = sheetsAccess(sheet_id)

    text = "Há funcionários de férias nos períodos: \n"
    values = []

    for record in records:
        if key_start in record:
            values.append(record[key_start]+ ' -> ')
        if key_final in record:
            values.append(record[key_final]+ ' \n')

    text += ''.join(values)
    text += "Caso esteja pensando em planejar suas férias, entrar em contato com o Responsável do seu setor em conjunto com a Administração!" 
    return text

def sheetsAccess(sheet_id: str):

    SPREADSHEET_ID = sheet_id

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1

    records = sheet.get_all_records()

    return records