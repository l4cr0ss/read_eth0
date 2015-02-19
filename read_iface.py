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

# Library for running ifconfig via the shell
import subprocess

'''
Function to get the inet4 addr assigned to iface
'''
def get_iface_addr(name='eth0'):
  # grab the output of ifconfig and parse it into lines
  output = subprocess.check_output("ifconfig").split('\n')

  # look for iface in the output. once you find it grab the addr
  found = 0
  iface = ''
  for line in output:
    if name in line:
      found = 1
      continue

    if found:
      pfx_end = line.find(':') + 1
      sfx_beg = line.find(' ', 19)
      iface = line[pfx_end:sfx_beg]
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
Send the string via SMS to my telephone
'''
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login('<email account>','<email password')
server.sendmail('<email account>',
                '<cell number>@<carrier's sms gateway>',
                result)
server.quit()
sys.exit(0)
