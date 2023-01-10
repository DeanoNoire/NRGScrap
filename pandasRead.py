import requests
import pandas as pd
from datetime import date,timedelta

#Datum
today = date.today()
#today = today + timedelta(days=1)
d1 = today.strftime("%Y-%m-%d")

urlKurz = "https://data.kurzy.cz/json/meny/b[6].json"

url = "https://www.ote-cr.cz/cs/kratkodobe-trhy/elektrina/denni-trh/@@chart-data?report_date=" + d1

rKurz = requests.get(urlKurz)
dataKurz = rKurz.json()
euro = dataKurz['kurzy']['EUR']['dev_stred']


r = requests.get(url)

data = r.json()
entries = data['data']['dataLine'][1]['point']
df = pd.DataFrame(entries)

df['y'] = pd.to_numeric(df['y'])
df['z'] = df['y'] * euro / 1000.00
print(df.to_string())
