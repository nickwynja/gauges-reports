import sys
import credentials

gauge = {
    'id' : '',
    'url' : 'http://site.com',
    'title' : 'My Site',
    'site' : 'my-site',
    'name' : 'site.com'
  }

api = {
    'url' : 'https://secure.gaug.es/gauges/',
    'header' : 'X-Gauges-Token',
    'token' : 'YOURTOKEN'
  }

report = {
    'path' : '/path/to/dir/',
    'name' : gauge['site'] + '-daily-report-',
    'ext' : '.md'
  }

def getJSON(url, header, token):
    import json
    import urllib2
    req = urllib2.Request(url)
    req.add_header(header, token)
    opener = urllib2.build_opener()
    f = opener.open(req)
    return json.load(f)

# Get traffic

trafficURL = api['url'] + gauge['id'] + '/traffic'
j = getJSON(trafficURL, api['header'], api['token'])
date = j['date']

# Create report

f = open(report['path'] + report['name'] + date + report['ext'], 'w+')
f.write('# Gauges Report for [' + gauge['name'] + '](' + gauge['url'] + ') on '  + date + "\n\n")

# Traffic Report

f.write("## Traffic \n\n")

latest = len(j['traffic'])-1
today = j['traffic'][latest]
views = today['views']
people = today['people']

f.write(str(views) + ' views by ' + str(people) + "  people.  \n\n")

# Content View Report

contentURL = api['url'] + gauge['id'] + '/content'

j = getJSON(contentURL, api['header'], api['token'])
date = j['date']

f.write("## Views \n\n")

for content in j['content']:
  title = content['title']
  if title.endswith(' ' + gauge['title']):
    title = title[:-len(gauge['title']) - 3]
  uri = content['url']
  views = content['views']
  report = '[' + title + '](' + uri + ') : ' + str(views) + "  \n"
  
  f.write(report.encode('utf-8', 'ignore'))

# Referrers Report

referrersURL = api['url'] + gauge['id'] + '/referrers'
j = getJSON(referrersURL, api['header'], api['token'])

f.write("## Referrers \n\n")

for referrer in j['referrers']:
  host = referrer['host']
  uri = referrer['url']
  views = referrer['views']
  report = '[' + host + '](' + uri + ') : ' + str(views) + "  \n"
      
  f.write(report.encode('utf-8', 'ignore'))

f.closed
