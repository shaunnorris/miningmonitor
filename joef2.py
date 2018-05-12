#!/usr/bin/env python
# example:

import graphitesend

import simplejson
import urllib2
import cookielib

site = "http://api.f2pool.com/litecoin/niehaus"
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

pricesite = "https://api.coinmarketcap.com/v2/ticker/2/?convert=USD"
req2 = urllib2.Request(pricesite, headers=hdr)
try:
    prices = urllib2.urlopen(req2)
    currprice = prices.read()
    pricedata = simplejson.loads(currprice)
except urllib2.HTTPError, e:
    e.fp.read()



elecperDay = 0.8 * 0.12 * 24 * activeWorkers 
# rought approximation of 800w per miner at 12cents US for elec hard coded exchange rate

USDLTC = pricedata["data"]["quotes"]["USD"]["price"]
print USDLTC

usdPerDay = USDLTC * btcPerDay
profitperDay = usdPerDay - elecperDay


print usdPerDay

print averageHashrate 
print btcPerDay

g = graphitesend.init(graphite_server='localhost',system_name='joef2')
print g.send('averageHashrate', averageHashrate)
print g.send('ltcPerDay', btcPerDay)
print g.send('usdPerDay', usdPerDay)
print g.send('USDLTC', USDLTC)
print g.send('elecperDay', elecperDay)
print g.send('profitperDay', profitperDay)
