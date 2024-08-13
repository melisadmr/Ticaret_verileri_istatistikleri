import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Pillow kütüphanesi

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Giriş Ekranı")
        self.root.geometry("800x600")
        
        # Arka plan görseli
        self.background_image = Image.open("kto.logo.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        
        # Giriş ekranını oluşturma
        self.create_welcome_screen()

    def create_welcome_screen(self):
        # Giriş ekranı için arka plan görseli
        background_label = tk.Label(self.root, image=self.background_photo)
        background_label.place(relwidth=1, relheight=1)
        
        welcome_label = tk.Label(self.root, text="Hoşgeldiniz!", font=("Arial", 24), bg="lightblue")
        welcome_label.pack(pady=50)
        
        start_button = tk.Button(self.root, text="Dünya Bankası Ticaret Verileri", font=("Arial", 16), command=self.open_main_screen, bg="lightgreen", fg="black")
        start_button.pack(pady=20)

    def open_main_screen(self):
        # Giriş ekranındaki tüm öğeleri kaldır
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.title("Dünya Bankası Verileri")

        # Ana ekranı oluştur
        self.create_main_screen()

    def create_main_screen(self):
        # Arka plan görseli
        background_label = tk.Label(self.root, image=self.background_photo)
        background_label.place(relwidth=1, relheight=1)

        # Butonların stilini ayarlama
        button_style = {
            "bg": "green",
            "fg": "black",
            "font": ("Arial", 12, "bold"),
            "padx": 10,
            "pady": 5
        }

        # Kullanıcının yıl aralıklarını girmesi için giriş kutuları ve etiketleri oluşturma
        self.start_year_label = tk.Label(self.root, text="Başlangıç Yılı:", font=("Arial", 12))
        self.start_year_label.pack(pady=5)
        self.start_year_entry = tk.Entry(self.root, font=("Arial", 12))
        self.start_year_entry.pack(pady=5)

        self.end_year_label = tk.Label(self.root, text="Bitiş Yılı:", font=("Arial", 12))
        self.end_year_label.pack(pady=5)
        self.end_year_entry = tk.Entry(self.root, font=("Arial", 12))
        self.end_year_entry.pack(pady=5)

        # "Grafiği Göster" butonunu oluşturma
        self.show_graph_button = tk.Button(self.root, text="GRAFİK ÇİZ", command=self.plot_graph, **button_style)
        self.show_graph_button.pack(pady=20, padx=20)

        # "Geri Dön" butonunu oluşturma
        self.back_button = tk.Button(self.root, text="GERİ", command=self.go_back, **button_style)

    def fetch_data(self, start_year, end_year):
        indicator = "NE.TRD.GNFS.ZS"  # Ticaretin GSYH'ya oranı endikatörü
        country = "TUR"  # Türkiye için ISO kodu

        url = f"http://api.worldbank.org/v2/country/{country}/indicator/{indicator}?date={start_year}:{end_year}&format=json"

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

    def plot_graph(self):
        try:
            start_year = self.start_year_entry.get()
            end_year = self.end_year_entry.get()

            if not start_year.isdigit() or not end_year.isdigit():
                raise ValueError("Yıl aralıkları geçerli değil.")

            start_year = int(start_year)
            end_year = int(end_year)
            
            years, values = self.fetch_data(start_year, end_year)
            
            plt.figure(figsize=(10, 5))
            plt.plot(years, values, marker='o', linestyle='-', color='b')

            plt.title(f'Ticaretin GSYH\'ya Oranı - Türkiye ({years[0]}-{years[-1]})', fontsize=14)
            plt.xlabel('Yıl', fontsize=12)
            plt.ylabel('Ticaretin GSYH\'ya Oranı (%)', fontsize=12)

            plt.ylim(min(values) - 5, max(values) + 5)
            plt.grid(True)

            if hasattr(self, 'canvas'):
                self.canvas.get_tk_widget().destroy()
            
            self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.root)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            self.show_graph_button.pack_forget()
            self.start_year_label.pack_forget()
            self.start_year_entry.pack_forget()
            self.end_year_label.pack_forget()
            self.end_year_entry.pack_forget()
            
            self.back_button.pack(pady=20, padx=20)
        except Exception as e:
            print(f"Bir hata oluştu: {e}")

    def go_back(self):
        self.back_button.pack_forget()

        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()
            del self.canvas
        
        self.start_year_label.pack(pady=5)
        self.start_year_entry.pack(pady=5)
        self.end_year_label.pack(pady=5)
        self.end_year_entry.pack(pady=5)
        self.show_graph_button.pack(pady=20, padx=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
