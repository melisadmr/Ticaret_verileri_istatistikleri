import tkinter as tk
from tkinter import ttk,messagebox
from evds import evdsAPI
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# EVDS API bağlanma
evds = evdsAPI('UyFuSmnH7n')

# Seri kodları ve başlıklar
data_series = {
    'Dış Ticaret İhracat Miktar Endeksi (ölçüm bazında)': 'TP.DT.IH.MIK.D01.2010',
    'İhracat Miktar Endeks (Yatırım (Sermaye) Malları)': 'TP.DT.IH.MIK.D02.2010',
    'İhracat Miktar Endeks (Yatırım (Sermaye) Malları (Taşımacılık Araçları Hariç))': 'TP.DT.IH.MIK.D03.2010',
    'İhracat Miktar Endeks (Sanayi İle İlgili Taşımacılık Araç Ve Gereçleri)': 'TP.DT.IH.MIK.D04.2010',
    'İhracat Miktar Endeks (Sanayi İçin İşlem Görmemiş Hammaddeler)': 'TP.DT.IH.MIK.D06.2010',
    'İhracat Miktar Endeks (Sanayi İçin İşlem Görmüş Hammaddeler)': 'TP.DT.IH.MIK.D07.2010',
    'İhracat Miktar Endeks (Esası Yiyecek Ve İçecek Olan İşlenmiş Hammaddeler)': 'TP.DT.IH.MIK.D10.2010',
    'İhracat Miktar Endeks (İşlem Görmüş Diğer Yakıt Ve Yağlar)': 'TP.DT.IH.MIK.D11.2010',
    'İhracat Miktar Endeks (Tüketim Malları)': 'TP.DT.IH.MIK.D12.2010',
    'İhracat Miktar Endeks (Binek Otomobilleri)': 'TP.DT.IH.MIK.D13.2010',
    'İhracat Miktar Endeks (Motor Benzini Ve Diğer Hafif Yağlar)': 'TP.DT.IH.MIK.D19.2010'
}

def plot_data(series_code, title, start_date, end_date,graph_type):
    try:
        data = evds.get_data([series_code], startdate=start_date, enddate=end_date)
        df = pd.DataFrame(data)
        df['Tarih'] = pd.to_datetime(df['Tarih'], format='%Y-%m')

        plt.figure(figsize=(10, 6))
        if graph_type == "Çizgi":
            plt.plot(df['Tarih'], df[series_code.replace('.', '_')], marker='o', linestyle='-', color='b')
        elif graph_type == "Sütun":
            plt.bar(df['Tarih'], df[series_code.replace('.', '_')], color='g')
        elif graph_type == "Nokta":
            plt.scatter(df['Tarih'], df[series_code.replace('.', '_')], color='r')
        elif graph_type == "Pasta":
            plt.pie(df[series_code.replace('.', '_')], labels=df['Tarih'], autopct='%1.1f%%')
        
        plt.title(title)
        plt.xlabel('Tarih')
        plt.ylabel('Değer')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Hata", f"Veri çekme hatası: {e}")

