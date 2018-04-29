#!/usr/bin/env python
# example:

import graphitesend

import simplejson
import urllib2
import cookielib

site = "https://api.ethermine.org/miner/:0xac723b12e73056f577a3a90d8767c031bfd9b83e/currentStats"
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
elecperDay = 0.6 * 0.21 * 24 * activeWorkers / 1.32
profitperDay = usdPerDay - elecperDay
 
# 600 W = 0.6kW * 21 cents / kwH * 24 h * 1.32 SGD / USD (rough approximation)

print averageHashrate 
print usdPerDay
print elecperDay

g = graphitesend.init(graphite_server='localhost',system_name='ethermine',group='mining')
print g.send('averageHashrate', averageHashrate)
print g.send('usdPerDay', usdPerDay)
print g.send('elecperDay', elecperDay)
print g.send('profitperDay', profitperDay)
