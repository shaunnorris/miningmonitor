#!/usr/bin/env python
# example:

import graphitesend

import simplejson
import urllib2
import cookielib

site = "http://api.f2pool.com/bitcoin/snminer"
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
    e.fp.read()

content = page.read()
 
data = simplejson.loads(content)
averageHashrate = data["hashrate"]
btcPerDay = float(data["value_last_day"])
activeWorkers = data["worker_length"] 

pricesite = "https://api.coindesk.com/v1/bpi/currentprice.json"
req2 = urllib2.Request(pricesite, headers=hdr)
try:
    prices = urllib2.urlopen(req2)
    currprice = prices.read()
    pricedata = simplejson.loads(currprice)
except urllib2.HTTPError, e:
    e.fp.read()



elecperDay = 1.3 * 0.12 * 24 * activeWorkers / 1.26
# rought approximation of 1.3kw per miner at 15cents CDN with 1.26 hard coded exchange rate

USDBTC = pricedata["bpi"]["USD"]["rate"]
USDBTC = float(USDBTC.replace(',', ''))
print USDBTC

usdPerDay = USDBTC * btcPerDay
profitperDay = usdPerDay - elecperDay


print usdPerDay

print averageHashrate 
print btcPerDay

g = graphitesend.init(graphite_server='localhost',system_name='f2pool',group='mining')
print g.send('averageHashrate', averageHashrate)
print g.send('btcPerDay', btcPerDay)
print g.send('usdPerDay', usdPerDay)
print g.send('USDBTC', USDBTC)
print g.send('elecperDay', elecperDay)
print g.send('profitperDay', profitperDay)