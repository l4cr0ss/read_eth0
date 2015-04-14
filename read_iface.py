#!/usr/bin/python
'''
Gets the inet4 addr assigned to an iface and texts it to a cellphone
'''

# Library for sys.exit
import sys

# Libraries for sending an SMS via SMTP
import smtplib
from email.mime.text import MIMEText

# Libraries for getting and formatting the current time
import time
import datetime

# Library for running ip via the shell
import subprocess

'''
Function to load the config
'''
def get_config():
  vars = {}
  f = open('.config', 'r')
  for line in f:
    t = line.split('=')
    vars[t[0]] = t[1].rstrip()
  print "loaded config"
  print vars
  return vars
    
'''
Function to get the inet4 addr assigned to iface
'''
def get_iface_addr(name='eth0'):
  # grab the output of ip addr and parse it into lines
  op = subprocess.check_output(["ip", "addr"]).split('\n')

  # look for iface in the output. once you find it grab the addr
  found = 0
  iface = ''
  for line in op:
    if name in line:
      if 'inet' in line:
        found = 1
        continue

    if found:
      l = line.strip()
      p = l.rfind('inet') + 5
      s = l.find('/')
      iface = l[p:s]
      break

  return iface

'''
Setup the output strings
'''
str_success = "{0} My device has booted with an IP address of {1}"
str_failure = "{0} My device has booted, but without an IP address"

'''
Get the current time and format it as a human readable string.
'''
cur_ts = time.time()
cur_dt = datetime.datetime.fromtimestamp(cur_ts)
cur_time = cur_dt.strftime('%Y-%m-%d %H:%M:%S')

iface = get_iface_addr()
result = '\n'
if iface:
  result = result + str_success.format(cur_time, iface)
else:
  result = result + str_failure.format(cur_time)

'''
Load the config from disk
'''
conf = get_config()

'''
Send the string via SMS to my telephone
'''
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(conf['email'],conf['pass'])
server.sendmail(conf['email'],
                conf['conn'],
                result)
server.quit()
sys.exit(0)
