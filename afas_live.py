# GOAL: Scrape artist names and their concert dates from https://www.afaslive.nl/agenda
import json
from sqlalchemy import create_engine
from datetime import datetime
import requests
from bs4 import BeautifulSoup
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

query = "SELECT * FROM stage.concerts_emailer WHERE venue = 'AFAS Live';"
our_data = pd.read_sql(query, engine)

response = requests.get('https://www.afaslive.nl/agenda')
soup = BeautifulSoup(response.content, features='html.parser')
concerts = soup.find_all('figcaption')
artists = []
concert_dates = []
for concert in concerts:
    artist = concert.find('h3').string
    concert_date = concert.find('time').text
    concert_date = ' '.join(concert_date.split(' ')[1:]) # The first word is a week day. We don't need it
    concert_date = datetime.strptime(concert_date, '%d %B %Y').date()

    known = our_data[(our_data['artist'] == artist) & (our_data['concert_date'] == concert_date)]

    # Append artist and concert_date to the lists if we don't yet have them stored in the database
    if known.empty:
        artists.append(artist)
        concert_dates.append(concert_date)

df = pd.DataFrame({'artist': artists, 'concert_date': concert_dates})
df['scrape_date'] = scrape_date
df['venue'] = 'AFAS Live'

if not df.empty:
    df.to_sql('concerts_emailer', engine, schema='stage', if_exists='append', index=False)
else:
    print('No new concerts found in AFAS Live')






