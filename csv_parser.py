import csv
from collections import defaultdict
from html.parser import HTMLParser
from itertools import zip_longest
import os, shutil

import time

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

lines = []

with open('everyonebot_tweets.csv', 'r') as f:
    reader = csv.reader(f)
    for i, line in enumerate(reader):
      # id,created_at,user,text
      lines.append(line)


days = defaultdict(list)
h = HTMLParser()

for line in reversed(lines):
  id = line[0]
  created_at = line[1]
  user = line[2]
  text = h.unescape(line[3])

  stamp = created_at.split(' ')
  day = stamp[0]
  timestamp = stamp[1]
  timestamp = time.strptime(timestamp,"%H:%M:%S")
  poop = time.strftime("%-I%p", timestamp).lower()
  a = ((int(time.strftime("%-H", timestamp)) + 11) * 2) % 24
  timestamp = (chr(128336+a//2+a%2*12)) #+ poop
  days[day].append(timestamp +'\n' + text)

all = []

for day in sorted(days.keys()):
  all.extend(days[day])

things_per_column = 6
la = list(chunks(all, things_per_column * 2))
la = [list(chunks(x, things_per_column)) for x in la]

groups = [list(map(list, zip_longest(*x))) for x in la]

folder = './html'
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception as e:
        print(e)

pages_per_file = 100
idx = 0
fileidx = 0
for page in groups:
  filen = str(fileidx).zfill(3)
  with open ('html/should_'+filen+'.html', 'a') as out:
    if idx == 0:
      out.write("""
        <style>
          html, body {
            margin: 0;
            padding: 0;
          }
          html {
            box-sizing: border-box;
          }
          *, *:before, *:after {
            box-sizing: inherit;
          }
          pre {
            line-height: 1.25;
            white-space: pre-wrap;
            font-family: "Courier New",monospace;
            margin: 0 36pt;
            width: 50%;
          }
          pre:nth-child(odd) {
            margin-right: 48pt;
            margin-left: 24pt;
          }
          pre:nth-child(even) {
            margin-left: 48pt;
            margin-right: 24pt;
          }
          .row {
            display: flex;
            margin-bottom: 1.5em;
            height: calc(90% / 7);
          }
          .printPage {
            margin: 0;
            padding: 36pt;
            width: 792pt;
            height: 1224pt;
            clear: both;
            page-break-after: always;
            border: 1px solid black;
          }
          .printPage:nth-child(odd) {
            padding-left: 72pt;
            padding-right: 0;
          }
          .printPage:nth-child(even) {
            padding-right: 72pt;
            padding-left: 0;
          }
        </style>
        """)
    out.write('<div class="printPage">\n')
    for row in page:
      out.write('<div class="row">\n')
      for tweet in row:
        if tweet == None:
          continue
        out.write ('<pre>')
        lastIndex = tweet.rfind('https://t.co')
        if lastIndex == -1:
          lastIndex = len(tweet)
        out.write (tweet[:lastIndex].strip()+'\n')
        out.write ('</pre>\n')
      out.write ('</div>\n')
    out.write('</div>\n')
  idx += 1
  idx = idx % pages_per_file
  if idx == 0:
    fileidx += 1

