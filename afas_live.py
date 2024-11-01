# GOAL:
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

scrape_date = datetime.today()

response = requests.get('https://www.afaslive.nl/agenda')
soup = BeautifulSoup(response.content)
concerts = soup.find_all('figcaption')
artists = []
concert_dates = []
for concert in concerts:
    artists.append(concert.find('h3').string)
    concert_date = concert.find('time').text
    concert_date = ' '.join(concert_date.split(' ')[1:]) # The first word is a week day. We don't need it
    concert_date = datetime.strptime(concert_date, '%d %B %Y')
    concert_dates.append(concert_date)

data = {'artist': artists, 'concert_date': concert_dates}
df = pd.DataFrame(data)
df['scrape_date'] = scrape_date
df['venue'] = 'AFAS Live'

# Write to the database





