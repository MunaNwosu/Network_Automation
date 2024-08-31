from  mistapi import mist_call,mist_info
import influxdb_client, time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS


org = "Capstone"
url = "http://localhost:8086"
token = '9e37c51b-6ffe-4e78-8382-007caf2d1077' #  docker-compose token
#token = 'GwoyekGDRfKJTsWsL4ZNAdQQA0eeEI3-mB3CsQ3uIcmfP_27Z4prEjJJ4Ttwjn0-JUZX9mC0PnJIMTcvmXlnKQ=='

#write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
with influxdb_client.InfluxDBClient(url=url, token=token, org=org) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS)


bucket = "Mist_info"

mist_token = 'Token G08vHaapdBafXEeHQa2yyBcjYy1fhYhbO1BSBUcW9H0sWAZjRD8OxWzTUwfpbPwHuHoeUjebiP18J0wyojkIn2DhUC35Mf7Z'
baseurl = "https://api.gc2.mist.com/api/v1"

while True:
    #mist call
    response1, response2, response3 = mist_call(mist_token, baseurl)
    influx_data = mist_info(response1, response2, response3)

    
    #writing to influxdb
    points = [
        Point("AP_data")
        .tag("site","Humber college")
        .field("2.4 band uplink",influx_data[0]),
        Point("AP_data")
        .tag("site","Humber college")
        .field("5 band uplink",influx_data[1]),
        Point("AP_data")
        .tag("site","Humber college")
        .field("2.4 band downlink",influx_data[2]),
        Point("AP_data")
        .tag("site","Humber college")
        .field("5 band downlink",influx_data[3]),
        Point("AP_data")
        .tag("site","Humber college")
        .field("2.4 band Channel Utilization",influx_data[4]),
        Point("AP_data")
        .tag("site","Humber college")
        .field("5 band Channel Utilization",influx_data[5]),
        Point("AP_data")
        .tag("site","Humber college")
        .field("Total Users",influx_data[6]),
    ]

    try:
        write_api.write(bucket=bucket, org="Capstone", record=points)
        print("Data written Succesfully to InfluxDB")
    except Exception as e:
        print(f"Error sending to InfluxDB: {e}")

    time.sleep(15)
          





