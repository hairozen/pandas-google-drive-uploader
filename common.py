import os
import string
from datetime import datetime
from pprint import pprint


from oauth2client import tools
from oauth2client.file import Storage
from oauth2client import client

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
read_data = False
create_spreadsheet = True
if read_data:
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
elif create_spreadsheet:
    SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def create_new_spreadsheet(service, parser, spreadsheet_title):
    spreadsheet_body = {
        # TODO: Add desired entries to the request body.
        "properties": {
            "title": spreadsheet_title
        }

    }
    request = service.spreadsheets().create(body=spreadsheet_body)
    response = request.execute()

    # TODO: Change code below to process the `response` dict:
    # pprint(response)

    spreadsheet_id = response['spreadsheetId']
    spreadsheet_url = response['spreadsheetUrl']
    print("New spreadsheet was created in {spreadsheet_url}".format(spreadsheet_url=spreadsheet_url))
    parser.set('spreadsheet', 'id', spreadsheet_id)
    parser.set('spreadsheet', 'url', spreadsheet_url)

    parser.add_section('sheet')
    parser.set('sheet', 'id', str(response['sheets'][0]['properties']['sheetId']))
    parser.set('sheet', 'name', str(response['sheets'][0]['properties']['title']))
    parser.set('sheet', 'column_count', str(response['sheets'][0]['properties']['gridProperties']['columnCount']))
    parser.set('sheet', 'row_count', str(response['sheets'][0]['properties']['gridProperties']['rowCount']))

    with open('config.ini', 'w') as configfile:
        parser.write(configfile)


def clear_spreadsheet(service, spreadsheet_id, sheet_name, sheet_column_letter):
    range_all = '{sheet_name}!A1:{sheet_column_letter}'.format(sheet_name=sheet_name, sheet_column_letter=sheet_column_letter)
    response = service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=range_all, body={}).execute()
    # pprint(response)


def convert_to_letter_index(numeric_index):
    letters = []
    while numeric_index >= 0:
        letters.append(string.ascii_uppercase[numeric_index % 26])
        numeric_index = numeric_index // 26 - 1
    return ''.join(reversed(letters))


def change_sheet_size(service, parser, spreadsheet_id, sheet_id, columns_length, rows_length):
    sheet_column_count = parser.getint('sheet', 'column_count')
    sheet_row_count = parser.getint('sheet', 'row_count')

    requests = []
    send = False
    new_sheet_column_count = sheet_column_count
    new_sheet_row_count = sheet_row_count

    if columns_length > sheet_column_count:
        send = True
        to_add = columns_length - sheet_column_count + 5
        requests.append({
            "appendDimension": {
                "sheetId": sheet_id,
                "dimension": "COLUMNS",
                "length": to_add
            }
        })
        new_sheet_column_count += to_add
    if rows_length > sheet_row_count:
        send = True
        to_add = rows_length - sheet_row_count + 10
        requests.append({
            "appendDimension": {
                "sheetId": sheet_id,
                "dimension": "ROWS",
                "length": to_add
            }
        })
        new_sheet_row_count += to_add

    if send:
        body = {
            'requests': requests
        }
        response = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        # pprint(response)

        parser.set('sheet', 'column_count', str(new_sheet_column_count))
        parser.set('sheet', 'row_count', str(new_sheet_row_count))

        with open('config.ini', 'w') as configfile:
            parser.write(configfile)


def write_all_data(service, spreadsheet_id, sheet_name, df, rows_length):
    data = []
    # Add the headers
    headers_req = {
        'range': "{sheet_name}!A2:{letter_index}2".format(sheet_name=sheet_name,
                                                          letter_index=convert_to_letter_index(len(df.columns))),
        'values': [list(df.columns)],
        "majorDimension": "ROWS"
    }
    data.append(headers_req)

    date_val = [["Last Update: {0}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))]]
    date_req = {
        'range': "A1",
        'values': date_val,
        "majorDimension": "ROWS"
    }
    data.append(date_req)

    for col, index in zip(df.columns, range(0, len(df.columns))):
        values = [list(df[col].fillna('').map(lambda x: str(x)))]
        letter_index = convert_to_letter_index(index)
        range_ = "{sheet_name}!{letter_index}3:{letter_index}{rows_length}".format(sheet_name=sheet_name,
                                                                                   letter_index=letter_index,
                                                                                   rows_length=rows_length + 2)
        req = {
            'range': range_,
            'values': values,
            "majorDimension": "COLUMNS"
        }
        data.append(req)

    body = {
        'valueInputOption': 'RAW',
        'data': data
    }

    result = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
    # pprint(result)
