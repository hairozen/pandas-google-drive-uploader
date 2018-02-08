import sys
from common import get_credentials, create_new_spreadsheet, clear_spreadsheet, convert_to_letter_index, \
    change_sheet_size, write_all_data
from googleapiclient import discovery
from configparser import ConfigParser
import pandas as pd

"""
BEFORE RUNNING:
---------------
1. If not already done, enable the Google Sheets API
   and check the quota for your project at
   https://console.developers.google.com/apis/api/sheets
2. Install the Python client library for Google APIs by running
   `pip install --upgrade google-api-python-client`
"""

# pandas data
df = pd.read_csv("dpc_cf_recom_post.csv", sep='\t')
rows_length = len(df.index)
columns_length = len(df.columns)


parser = ConfigParser()
parser.read('config.ini')
# The ID of the spreadsheet to update.
spreadsheet_id = parser.get('spreadsheet', 'id')
spreadsheet_title = parser.get('spreadsheet', 'title')

# Get the credentials required for google drive API
credentials = get_credentials()
# Create the service for google drive API
service = discovery.build('sheets', 'v4', credentials=credentials)

# Create new spreadsheet if not exist
if "None" == spreadsheet_id:
    create_new_spreadsheet(service, parser, spreadsheet_title)
    spreadsheet_id = parser.get('spreadsheet', 'id')

# Get sheet_id
sheet_id = parser.get('sheet', 'id')
# Get sheet_name
sheet_name = parser.get('sheet', 'name')

# clear exists spreadsheet
sheet_column_letter = convert_to_letter_index(parser.getint('sheet', 'column_count'))
clear_spreadsheet(service, spreadsheet_id, sheet_name, sheet_column_letter)

# Adjust spreadsheet size
change_sheet_size(service, parser, spreadsheet_id, sheet_id, columns_length, rows_length)

# Write all data to sheet_name in spreadsheet_id
write_all_data(service, spreadsheet_id, sheet_name, df, rows_length)



