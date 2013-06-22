#!/usr/bin/python

import os
import sys
import time
import simplejson as json
import Geoclue
import requests

POS_PROVIDER = 'Ubuntu GeoIP'
WEATHER_ID = os.getenv('WEATHER_ID', 'CHANGEME')
TMPFILE = '/tmp/weather.json'
MIN_AGE = 600

if WEATHER_ID == 'CHANGEME':
    print "set WEATHER_ID in env"
    sys.exit()

now = time.time()
try:
    st = os.stat(TMPFILE)
    cache_time = st.st_mtime
except OSError:
    cache_time = 0

cache_age = int(now - cache_time)

if cache_age > MIN_AGE:
    l = Geoclue.DiscoverLocation()
    l.init()
    l.set_position_provider(POS_PROVIDER)
    pos = l.get_location_info()
    print pos
    latitude = pos['latitude']
    longitude = pos['longitude']
    url = 'http://www.myweather2.com/developer/forecast.ashx?uac=%s&query=%s,%s&temp_unit=c&output=json' % (WEATHER_ID, latitude, longitude)
    req = requests.request('GET', url)
    f = open(TMPFILE, 'wb')
    f.write(req.content)
    f.close()
# else:
    # print "using weather cache, age: %s" % cache_age

f = open(TMPFILE, 'rb')
s = f.read()
f.close()
j = json.loads(s)

weather_humidity = j['weather']['curren_weather'][0]['humidity']
weather_pressure = j['weather']['curren_weather'][0]['pressure']
weather_temp = j['weather']['curren_weather'][0]['temp']
weather_temp_unit = j['weather']['curren_weather'][0]['temp_unit']
weather_code = j['weather']['curren_weather'][0]['weather_code']
weather_text = j['weather']['curren_weather'][0]['weather_text'].split(',')[0]
wind_dir = j['weather']['curren_weather'][0]['wind'][0]['dir']
wind_speed = j['weather']['curren_weather'][0]['wind'][0]['speed']
wind_speed_unit = j['weather']['curren_weather'][0]['wind'][0]['wind_unit']

print "%s: %s%s" % (weather_text, weather_temp, weather_temp_unit)
