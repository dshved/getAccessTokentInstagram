import sys
import requests
from bs4 import BeautifulSoup
import re

def getAccsess(url):
  reg = re.compile('\d+.\w.+\w+')
  access_token = reg.findall(url)
  return access_token[0]

client_id     = 'CLIENT_ID'
redirect_uri  = 'REDIRECT_URI'

response_type = 'token'
scope         = 'basic+likes+comments+relationships'
next_url      = '/oauth/authorize/?client_id=' + client_id +
                '&redirect_uri=' + redirect_uri +
                '&response_type=' + response_type +
                '&scope='+scope
url           = 'https://www.instagram.com/accounts/login/?force_classic_login=&next=' + next_url
ref_url       = 'https://www.instagram.com' + next_url

username = 'USERNAME'
password = 'PASSWORD'

client = requests.session()

client.get(url)
csrftoken = client.cookies['csrftoken']

login_data = dict(username=username, password=password, csrfmiddlewaretoken=csrftoken, next=next_url)
r = client.post(url, data=login_data, headers=dict(Referer=url))

if r.url == ref_url:
  csrftoken_new = r.cookies['csrftoken']
  allow = 'Authorize'
  allow_data = dict(csrfmiddlewaretoken=csrftoken_new, allow=allow)
  r = client.post(r.url, data=allow_data, headers=dict(Referer=r.url))
  print getAccsess(r.url)
else:
  soup = BeautifulSoup(r.text)
  alert = soup.find('p',{'class':'alert-red'})
  try:
    if len(alert.text) > 0:
    print alert.text
  except:
    print getAccsess(r.url)
