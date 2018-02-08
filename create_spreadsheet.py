from common import get_credentials
from examples import write_row

"""
BEFORE RUNNING:
---------------
1. If not already done, enable the Google Sheets API
   and check the quota for your project at
   https://console.developers.google.com/apis/api/sheets
2. Install the Python client library for Google APIs by running
   `pip install --upgrade google-api-python-client`
"""
from pprint import pprint

from googleapiclient import discovery

# TODO: Change placeholder below to generate authentication credentials. See
# https://developers.google.com/sheets/quickstart/python#step_3_set_up_the_sample
#
# Authorize using one of the following scopes:
# 'https://www.googleapis.com/auth/spreadsheets.readonly'

create_new = False

credentials = get_credentials()

service = discovery.build('sheets', 'v4', credentials=credentials)

spreadsheet_body = {
    # TODO: Add desired entries to the request body.
    "properties": {
        "title": "New_Hai"
    }

}
if create_new:
    request = service.spreadsheets().create(body=spreadsheet_body)
    response = request.execute()

    # TODO: Change code below to process the `response` dict:
    pprint(response)


# The ID of the spreadsheet to update.
spreadsheet_id = response['spreadsheetId'] if create_new else "1JVcnx2oN5XW2MvircP3kNCvI9rZaXtpQOLNF-cGNURc"

# write_row(service, spreadsheet_id)

values = [
    [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
    ]
]
data = [
    {
        'range': "Sheet1!A1:A12",
        'values': values,
        "majorDimension": "COLUMNS"
    },
    {
        'range': "Sheet1!A1:L1",
        'values': values,
        "majorDimension": "ROWS"
    },
    # Additional ranges to update ...
]
body = {
  'valueInputOption': 'RAW',
  'data': data
}
result = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

pprint(result)

