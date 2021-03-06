import re
from datetime import datetime
import pandas as pd
import json
from iteration_utilities import duplicates
with open('w.txt', "r", encoding='utf-8') as infile:
    outputData = { 'date': [], 'sender': [],'category': [], 'text': [] }
    for line in infile:
        matches = re.match(r'^(\d{1,2})\/(\d{1,2})\/(\d\d), (24:00|2[0-3]:[0-5][0-9]|[0-1][0-9]:[0-5][0-9]) - ((\S[^:]*?): )?(.*)$', line)
        if matches:
          outputData['date'].append(
            datetime(
              int(matches.group(3))+2000,
              int(matches.group(1)),
              int(matches.group(2)),
              hour=int(matches.group(4)[0:2]),
              minute=int(matches.group(4)[3:])
            ))
          outputData['sender'].append(matches.group(6) or "{undefined}")
          outputData['category'].append(matches.group(7).split(' ')[0] or "{undefined}")
          outputData['text'].append(matches.group(7).split(' ', 1)[1])

        elif len(outputData['text']) > 0:
          outputData['text'][-1] += "\n" + line[0:-1]
   
    outputData = pd.DataFrame(outputData)
    outputData.to_json('output.json',indent=4)

listt = []
starting_line='Scrolling through Whatsapp groups are a painful task. Let us give you a brief summary of what all happened on your PM Community group this week.'
listt.append(starting_line)
category1 = []
def noRepeat():
    regex_category = r'(#\w+|#+)'
    for (k,v) in outputData['category'].items():
      if v not in p:
         if re.search(regex_category,v):
            listt.append(re.findall(regex_category, v)) 
            listt.append(outputData['text'][k])
def Repeat(x): 
      _size = len(x) 
      repeated = [] 
      regex_category = r'(#\w+|#+)'
      for i in range(_size): 
        k = i + 1
        for j in range(k, _size): 
            if re.search(regex_category,x[i]):
              if x[i] == x[j] and x[i] not in repeated: 
                repeated.append(x[i]) 
                listt.append(re.findall(regex_category, x[i]) or "{undefined}") 
                for i in range(_size):
                  if x[i] == x[j]:
                    listt.append(outputData['text'][i])
                  else:
                    continue
      return repeated 
def inBetween():
    regex_category = r'(#\w+|#+)'
    for (k,v) in outputData['text'].items():
      if v not in p:
         if re.search(regex_category,v):
            listt.append(re.findall(regex_category, v)) 
            listt.append(outputData['text'][k])
p=Repeat(outputData['category'])
noRepeat()
inBetween()
print('\n'.join(map(str, listt)))