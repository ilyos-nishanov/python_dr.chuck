#geocoding - taking text version of an address and turning it into geolocation
#openstreetmap.org
#py4e.com/code3/
# geoapify.com/geocoding-api --is not free

import urllib.request, urllib.parse
import json, ssl
#havily rate limited proxy of geoapify.com
serviceurl = 'https://py4e-data.dr-chuck.net/opengeo?q' #after q if you put =Ann+Arbor%2C+MI

#ignore ssl certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    address = input('Enter location: ')
    if len(address)<1: break
    
    address = address.strip()
    parms = dict()
    parms['q']=address # take the text that comes after q=...and put it here
    
    url = serviceurl + urllib.parse.urlencode(parms)
    
    print('Retrieving', url)
    uh = urllib.request.urlopen(url,context=ctx)
    data = uh.read().decode() #returns in python string and stored in data variable
    print('Retrieved', len(data), 'characters', data[:20].replace('\n',' '))
    
    # check data loads 
    try:
        js = json.loads(data)
    except:
        js = None
    
    #another sanity check    
    if not js or 'features' not in js:
        print('=== Download error ===')
        print(data)
        break
    if len(js['features']) == 0:
        print('=== Object not found ===')
        print(data)
        break
    #print(json.dumps(js, indent=4))
    
    lat = js['features'][0]['properties']['lat']
    lon = js['features'][0]['properties']['lon']
    print('lat', lat, 'lon', lon)
    location = js['features'][0]['properties']['formatted']
    