#!/usr/bin/env python
# example:

import graphitesend

import simplejson
import urllib2
import cookielib

site = "https://api-zcash.flypool.org/miner/:t1QT5K1i41gscAfJNWSSefjUkiyGBAk9XVi/currentStats"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


req = urllib2.Request(site, headers=hdr)

try:
    page = urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.fp.read()

content = page.read()
 
data = simplejson.loads(content)

averageHashrate = data["data"]["averageHashrate"]
usdPerDay = data["data"]["usdPerMin"]*60*24
activeWorkers = data["data"]["activeWorkers"] 
elecperDay = 0.85 * 0.21 * 24 * activeWorkers / 1.32
profitperDay = usdPerDay - elecperDay

print averageHashrate 
print usdPerDay

g = graphitesend.init(graphite_server='localhost',system_name='zcash-flypool',group='mining')
print g.send('averageHashrate', averageHashrate)
print g.send('usdPerDay', usdPerDay)
print g.send('elecperDay', elecperDay)
print g.send('profitperDay', profitperDay)
