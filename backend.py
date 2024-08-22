from tkinter import messagebox
import requests
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from sklearn.linear_model import LinearRegression

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


    def plot(self, graph_type, trendline=False):
        plt.figure(figsize=(10, 5))
        if graph_type == "Çizgi":
            plt.plot(self.years, self.values, marker='o', linestyle='-', color='b')
        elif graph_type == "Sütun":
            plt.bar(self.years, self.values, color='g')
        elif graph_type == "Nokta":
            plt.scatter(self.years, self.values, color='r')
        elif graph_type == "Pasta":
            plt.pie(self.values, labels=self.years, autopct='%1.1f%%')
        if trendline and graph_type != "Pasta":
            self.add_trendline()
        plt.title(f'Ticaretin GSYH\'ya Oranı - Türkiye ({self.years[0]}-{self.years[-1]})', fontsize=14)
        plt.xlabel('Yıl', fontsize=12)
        plt.ylabel('Ticaretin GSYH\'ya Oranı (%)', fontsize=12)
        plt.grid(True)
        
    
    def add_trendline(self):
        # NumPy kullanarak lineer regresyon hesaplama
        slope, intercept, r_value, p_value, std_err = stats.linregress(self.years, self.values)
        trend = np.array(self.years) * slope + intercept
        plt.plot(self.years, trend, color='orange', linestyle='--', label='Eğilim Çizgisi')
        plt.legend()
        
        
    def predict_next_values(self, periods=5, method="linear"):
        future_years = np.arange(self.years[-1] + 1, self.years[-1] + periods + 1)
        if method == "linear":
            model = LinearRegression()
            model.fit(np.array(self.years).reshape(-1, 1), self.values)
            predictions = model.predict(future_years.reshape(-1, 1))
        elif method == "exp_smoothing":
            model = SimpleExpSmoothing(self.values).fit()
            predictions = model.forecast(periods)
        
        return future_years, predictions
    
        
    def calculate_standard_deviation(self):
        return pd.Series(self.values).std()
    

    def calculate_median(self):
        return pd.Series(self.values).median()
    

    def calculate_mean(self):
        return pd.Series(self.values).mean()
        
        
