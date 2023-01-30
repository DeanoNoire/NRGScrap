import requests
import pandas as pd
from datetime import date,timedelta
import csv
import os
import shutil

#Dnes
today = date.today()
d1 = today.strftime("%Y-%m-%d")

#Zítra
today = today + timedelta(days=1)
d2 = today.strftime("%Y-%m-%d")

outputPath = "/usr/share/hassio/homeassistant/nrg/"
NullTemplateFile = "/home/deano/scripts/NRGScrap/outputNullTemplate/output2.json"

urlKurz = "https://data.kurzy.cz/json/meny/b[6].json"

url = "https://www.ote-cr.cz/cs/kratkodobe-trhy/elektrina/denni-trh/@@chart-data?report_date=" + d1
urlZitra = "https://www.ote-cr.cz/cs/kratkodobe-trhy/elektrina/denni-trh/@@chart-data?report_date=" + d2

rKurz = requests.get(urlKurz)
dataKurz = rKurz.json()
euro = dataKurz['kurzy']['EUR']['dev_stred']

#Dnes
r = requests.get(url)
data = r.json()
entries = data['data']['dataLine'][1]['point']
df = pd.DataFrame(entries)

df['y'] = pd.to_numeric(df['y'])
df['z'] = df['y'] * euro / 1000.00
df = df.drop('x', axis = 1)
df = df.drop('y', axis = 1)
df.to_json(outputPath+'output.json',orient = 'columns')

#Zítra

rZitra = requests.get(urlZitra)
dataZitra = rZitra.json()
try: 
    entriesZitra = dataZitra['data']['dataLine'][1]['point']
    dfZitra = pd.DataFrame(entries)
    dfZitra['y'] = pd.to_numeric(dfZitra['y'])
    dfZitra['z'] = dfZitra['y'] * euro / 1000.00
    dfZitra = dfZitra.drop('x', axis = 1)
    dfZitra = dfZitra.drop('y', axis = 1)
    dfZitra.to_json(outputPath+'output2.json',orient = 'columns')

except:
    print("Není zítřek - přeplácnu json nullovým")
    shutil.copyfile(NullTemplateFile,outputPath+'output2.json')
    

#Kurz do JSONu
with open(outputPath+'kurz.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow([str(euro)])

print(str(euro))
    