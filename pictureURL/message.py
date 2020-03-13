import os
import json
from .models import CSV
import requests

url = "https://www.bulksmsnigeria.com/api/v1/sms/create"

# https://www.bulksmsnigeria.com/api/v1/sms/create?, api_token=BS53DO6EEptDoMNF6y79doLPdSuJlT5FzMkB22HdGq9FvJLR4SCyxZlNnH6D&,
# from=BulkSMS.ng&to=2348063113913&\
#                    body=Welcome&dnd=2



def sendPostRequest(requrl, api_token ,message_from, to, body):
    req_params = {
        "api_token": api_token,
        "from": message_from,
        "to": to,
        "body": body
    }
    response = requests.post(requrl, req_params)
    print(response)
    if response.status_code == 200:
        print(response.status_code)
        return "ok"
    else:
        return response.text


# response = sendPostRequest(url, "P0KpZxWPZwOIT6JIKEBCFOFE6Q12ztUrsbCoxdE2ppfsXRwqAUyx3kEvTYFy", "Efiong", "2348121891955", "api-connection test from my application" )

# print(response.text)

#***** post body size,
## dump the json response


# import csv
# datafile = open('data.csv', 'r')
# myreader = csv.reader(datafile)
#
# for row in myreader:
#     print(row[0], row[1], row[2])