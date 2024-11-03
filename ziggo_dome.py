# GOAL: Scrape artist names and their concert dates from https://ziggodome.nl/en/agenda
import requests
import json
from datetime import datetime
import pandas as pd

scrape_date = datetime.today()

response = requests.get('https://ziggodome.nl/api/agenda')
response_data = json.loads(response.content)['data']
concert_dates = [i['showDate'][:10] for i in response_data]
artists = [i['performerName'] for i in response_data]

data = {'concert_date': concert_dates, 'artist': artists}
df = pd.DataFrame(data)
df['scrape_date'] = scrape_date
df['venue'] = 'Ziggo Dome'



