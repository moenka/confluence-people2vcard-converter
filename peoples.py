#!/usr/bin/env python3

import argparse
import os
import requests
import sys
from bs4 import BeautifulSoup

url = ''
user_name = ''
user_pass = ''
parser = 'html.parser'
path = './contacts'

try:
  os.mkdir(path)
except FileExistsError:
  print("INFO: '%s' directory already exists." % path)


credentials = requests.auth.HTTPBasicAuth(user_name, user_pass)
req = requests.get(url, auth=credentials)
soup = BeautifulSoup(req.text, parser)

for vcard in soup.find_all('div', 'vcard'):
  try:
    full_name = vcard.h4.a.contents[0]
    rev_name = ';'.join(full_name.split(' ')[::-1])
    nick_name = vcard.h4.a['data-username']
    mail = vcard.find('a', 'email').contents[0]
  except IndexError:
    continue

  content = (
    "BEGIN:VCARD\n"
    "VERSION:3.0\n"
    "FN:%s\n"
    "N:%s;;;\n"
    "NICKNAME:%s\n"
    "EMAIL;TYPE=INTERNET;TYPE=WORK:%s\n"
    "END:VCARD") % (full_name, rev_name, nick_name, mail)

  with open("%s/%s.vcf" % (path, nick_name), 'w') as fp:
    fp.write(content)

