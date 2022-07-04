import requests
from requests.auth import HTTPBasicAuth
import json
import psycopg2

url = "https://auvikapi.us4.my.auvik.com/v1/stat/deviceAvailability/uptime?filter[fromTime]=2022-06-22T01:00:00.000Z&filter[thruTime]=2022-06-23T01:00:00.000Z&filter[interval]=hour"

payload={}

response = requests.request("GET", url, auth = HTTPBasicAuth("cwheaton@autonometech.com", "BnkY5EiqbCHiamrxcmtb8Ge8PYoQaHlo/sfJGeql951ZwCLw"), data=payload)

response = response.json()

try:
    connection = psycopg2.connect(user="postgres",
                                  password="1234",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="template1")
    cursor = connection.cursor()
    print(connection.server_version)
    for i in range(len(response["data"])):
        id = response["data"][i]["id"]
        for j in range(len(response["data"][i]["attributes"]["stats"][0]["data"])):
            postgres_insert_query = 'INSERT INTO public."auvik_data" (id, recordedAt, percent) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING'
            record_to_insert = (id, response["data"][i]["attributes"]["stats"][0]["data"][j][0], response["data"][i]["attributes"]["stats"][0]["data"][j][1])
            cursor.execute(postgres_insert_query, record_to_insert)

            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into table")

except (Exception, psycopg2.Error) as error:
    print("Failed to insert record into template1 database and data table", error)

finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")