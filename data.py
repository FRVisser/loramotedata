#!/usr/bin/env python3
import json
import base64
import binascii
import csv
from datetime import datetime


with open ( 'data.json' ) as data_file:
    data = json.load ( data_file )

lenData = len ( data["points"] )

hexData = []

for i in range ( 0, lenData ):
    hexData.append(i)
    hexData[i] = ( binascii.b2a_hex ( binascii.a2b_base64 ( data["points"][i]["data"] )))

led = []
pressure = []
temperature = []
altitude = []
battery = []
latitude = []
longitude = []
elevation = []
time = []
delta = []

for i in range ( 0, lenData ):
    led.append(i)
    pressure.append(i)
    temperature.append(i)
    altitude.append(i)
    battery.append(i)
    latitude.append(i)
    longitude.append(i)
    elevation.append(i)
    time.append(i)


    led[i] = int(hexData[i][:2], 16)
    pressure[i] = int(hexData[i][2:-26], 16) * 10.0
    temperature[i] = int(hexData[i][6:-22], 16) / 100.0
    altitude[i] = int(hexData[i][10:-18], 16) / 10.0
    battery[i] = (int(hexData[i][14:-16], 16) / 255.0)

    latitude[i] = hexData[i][16:-10]
    if int(latitude[i],16) & 0x800000:
        latitude[i] = ( ( int(latitude[i],16) & 0x00FFFFFF ) + 1 ) * -90.0 / 0x800000;
    else:
        latitude[i] = int(latitude[i],16) * 90.0 / 0x7FFFFF;



    longitude[i] = hexData[i][22:-4]
    if int(longitude[i],16) & 0x800000:
        longitude[i] = ( ( int(longitude[i],16) & 0x00FFFFFF ) + 1 ) * -180.0 / 0x800000;
    else:
        longitude[i] = int(longitude[i],16) * 180.0 / 0x7FFFFF;


    elevation[i] = hexData[i][28:]
    time[i] = datetime.strptime(data["points"][i]["time"][11:][:8], '%H:%M:%S')

startTime = min(time)
for i in range ( 0, lenData ):
    delta.append(i)
    delta[i] = time[i] - startTime

print ( led[0] )
print ( pressure[0] )
print ( temperature[0] )
print ( altitude[0] )
print ( battery[0] )
print ( latitude[0] )
print ( longitude[0] )
print ( elevation[0] )
print ( time[0])
print ( hexData[0] )
print ( hexData[lenData - 1])

with open('data.csv', 'wb') as csvfile:
    csv = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # csv.writerow(['latitude', 'longitude'])
    #
    # for i in range ( 0, lenData ):
    #     csv.writerow([latitude[i], longitude[i]])
    csv.writerow(['delta', 'time', 'node_eui', 'gateway_eui', 'led', 'pressure', 'temperature', 'altitude', 'battery', 'latitude', 'longitude', 'elevation'])

    for i in range ( 0, lenData ):
        csv.writerow([delta[i], time[i], data["points"][i]["node_eui"], data["points"][i]["gateway_eui"], led[i], pressure[i], temperature[i], altitude[i], battery[i], latitude[i], longitude[i], elevation[i]])

# print ("second time")
#
#
# with open('map.csv', 'wb') as csvfile:
#     csv = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     # csv.writerow(['latitude', 'longitude'])
#     #
#     # for i in range ( 0, lenData ):
#     #     csv.writerow([latitude[i], longitude[i]])
#     csv.writerow(['latitude', 'longitude'])
#
#     for i in range ( 0, lenData ):
#          csv.writerow([latitude[i], longitude[i]])

# time = [h , m, s]
# for i in range ( 0, lenData ):
#     time.append(i)
#     time0h = int(data["points"][0]["time"][11:-14])
#     time0m = int(data["points"][0]["time"][14:-11])
#     time0s = int(data["points"][0]["time"][17:-8])
#time1 = data["points"][10]["time"][11:-8]
