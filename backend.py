from tkinter import messagebox
import requests
import pandas as pd
import matplotlib.pyplot as plt

class WorldBankData:
    def __init__(self, indicator, country):
        self.indicator = indicator
        self.country = country

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

class GraphPlotter:
    def __init__(self, years, values):
        self.years = years
        self.values = values

    def plot(self, graph_type):
        
        plt.figure(figsize=(10, 5))
        if graph_type == "Çizgi":
            plt.plot(self.years, self.values, marker='o', linestyle='-', color='b')
        elif graph_type == "Sütun":
            plt.bar(self.years, self.values, color='g')
        elif graph_type == "Nokta":
            plt.scatter(self.years, self.values, color='r')
        elif graph_type == "Pasta":
            plt.pie(self.values, labels=self.years, autopct='%1.1f%%')

        plt.title(f'Ticaretin GSYH\'ya Oranı - Türkiye ({self.years[0]}-{self.years[-1]})', fontsize=14)
        plt.xlabel('Yıl', fontsize=12)
        plt.ylabel('Ticaretin GSYH\'ya Oranı (%)', fontsize=12)
        plt.grid(True)
        
        
