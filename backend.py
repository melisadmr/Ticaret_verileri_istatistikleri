import requests
import pandas as pd

class WorldBankAPI:
    def __init__(self, country="TUR", indicator="NE.TRD.GNFS.ZS"):
        self.country = country
        self.indicator = indicator

    def fetch_data(self, start_year, end_year):
        url = f"http://api.worldbank.org/v2/country/{self.country}/indicator/{self.indicator}?date={start_year}:{end_year}&format=json"
        response = requests.get(url)
        data = response.json()

        years = []
        values = []

        for entry in data[1]:
            year = entry['date']
            value = entry['value']
            
            years.append(int(year))
            values.append(value)

        return years, values
