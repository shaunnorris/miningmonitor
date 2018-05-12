#!/usr/bin/env python
# example:

import graphitesend

import simplejson
import urllib2
import cookielib

site = "https://api.nicehash.com/api?method=stats.provider.ex&addr=3GyXcFpZBsDT78Tz7hZD4k1mFjrXdzYP3j"
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


totalProf = 0

for i in data["result"]["current"]:
	algoProf = float(i["profitability"])
        algoName = i["name"]
        print algoName
       	#if "a" in i["data"][0]:
        hashRate = 0 
        try:
	#there is activity for this algo
	#to get the profitibility per day in BTC, multiply "a" rate by algo profitibility and add to total prof 
                print i["data"]
                hashRate = i["data"][0]["a"]
      		totalProf = totalProf + algoProf * float(i["data"][0]["a"])
                print str(algoProf) + ":" + str(hashRate)
        except Exception:
            print "no a found"
    
print "total profitibility in BTC/day is " + str(totalProf)
btcPerDay = totalProf




elecperDay = 0
# rough approximation of robbie elec costs / month
pricesite = "https://api.coindesk.com/v1/bpi/currentprice.json"
req2 = urllib2.Request(pricesite, headers=hdr)
try:
    prices = urllib2.urlopen(req2)
    currprice = prices.read()
    pricedata = simplejson.loads(currprice)
except urllib2.HTTPError, e:
    e.fp.read()

USDBTC = pricedata["bpi"]["USD"]["rate"]
USDBTC = float(USDBTC.replace(',', ''))
print "BTC price:" + str(USDBTC)

usdPerDay = USDBTC * btcPerDay
print "USD per day:" + str(usdPerDay)
profitperDay = usdPerDay - elecperDay


print  usdPerDay
print  btcPerDay

g = graphitesend.init(graphite_server='localhost',system_name='joe')
print g.send('btcPerDay', btcPerDay)
print g.send('usdPerDay', usdPerDay)
print g.send('USDBTC', USDBTC)
print g.send('elecperDay', elecperDay)
print g.send('profitperDay', profitperDay)
