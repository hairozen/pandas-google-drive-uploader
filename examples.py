from pprint import pprint


def write_row(service, spreadsheet_id):

    # The A1 notation of the values to update.
    range_ = "Sheet1!A1:L1"

    # How the input data should be interpreted.
    # https://developers.google.com/sheets/api/reference/rest/v4/ValueInputOption
    value_input_option = 'RAW'  # TODO: Update placeholder value.

    value_range_body = {
        # TODO: Add desired entries to the request body. All existing entries
        # will be replaced.
        "values": [
            [
                1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
            ]
        ]
    }

    request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, body=value_range_body)
    response = request.execute()

    # TODO: Change code below to process the `response` dict:
    pprint(response)
