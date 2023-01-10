import requests
import pandas as pd
from datetime import date,timedelta


#Datum
today = date.today()
today = today + timedelta(days=1)
d1 = today.strftime("%Y-%m-%d")
print(d1)

urlBase = "https://www.ote-cr.cz/cs/kratkodobe-trhy/elektrina/denni-trh/@@chart-data?report_date="
datum = d1
url = urlBase + datum

r = requests.get(url)

data = r.json()
entries = data['data']['dataLine'][1]['point']
df = pd.DataFrame(entries)
print(df.to_string())