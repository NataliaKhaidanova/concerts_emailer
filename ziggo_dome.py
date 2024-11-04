# GOAL: Scrape artist names and their concert dates from https://ziggodome.nl/en/agenda
import json
from sqlalchemy import create_engine
from datetime import datetime
import requests
import pandas as pd

# INIT --------------------------------------------------------------------------------------------------
with open('ini.json', 'r') as ini_file:
    settings = json.load(ini_file)['concerts_emailer']

database = settings['database']
user = settings['user']
password = settings['password']
host = settings['host']
port = settings['port']

# Set up a database connection
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')
# -------------------------------------------------------------------------------------------------------
scrape_date = datetime.today()

query = "SELECT * FROM stage.concerts_emailer WHERE venue = 'Ziggo Dome';"
our_data = pd.read_sql(query, engine)

response = requests.get('https://ziggodome.nl/api/agenda')
response_data = json.loads(response.content)['data']
concert_dates = [i['showDate'][:10] for i in response_data]
artists = [i['performerName'] for i in response_data]

if len(concert_dates) != len(artists):
    print(f"len(concert_dates): {len(concert_dates)}, len(artists): {len(artists)}")
    raise Exception("Length of concert_dates doesn't match length of artists")

new_concert_dates = []
new_artists = []
known: list[list] = our_data[['concert_date', 'artist']].values.tolist()
for concert_date, artist in zip(concert_dates, artists):
    if [concert_date, artist] not in known:
        new_concert_dates.append(concert_date)
        new_artists.append(artist)

data = {'concert_date': new_concert_dates, 'artist': new_artists}
df = pd.DataFrame(data)
df['scrape_date'] = scrape_date
df['venue'] = 'Ziggo Dome'



