This project is based on Google API Client Libraries
---------------------------------------------------------------------------------

In order to run it:
 1. Create a project in Google cloud platform (Google console)
 2. Set up an OAuth 2.0
 3. Enable Google Sheets API
 4. Download client_secret.json file from Google console and place it in res-csv-google-drive-uploader directory

Notes:
1. client_secret.json file is private and therefore missing from this repository
2. if your browser is on a different machine run this application with the command-line parameter
--noauth_local_webserver



Config Files
---------------------------------------------------------------------------------
1. Use config_initial.ini example in order to create a new spreadsheet
2. For spreadsheet which is already exists use config.ini (spreadsheet_title, spreadsheet_url fields are optional)


Sign-in gmail viaserver terminal 
---------------------------------------------------------------------------------
Use w3m

https://www.howtogeek.com/103574/how-to-browse-from-the-linux-terminal-with-w3m/



URL structure
---------------------------------------------------------------------------------

https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={sheet_id}



Important Links
---------------------------------------------------------------------------------

Getting Started
https://developers.google.com/api-client-library/python/start/get_started

Google cloud platform
https://console.cloud.google.com/home/dashboard

Manage projects in the console
https://support.google.com/cloud/answer/6158853

Setting up OAuth 2.0
https://support.google.com/cloud/answer/6158849