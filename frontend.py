import os
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib import pyplot as plt
from backend import WorldBankData, GraphPlotter
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Dünya Bankası Verileri")
        self.root.geometry("800x600")
        
        # Arka plan resmi
        self.background_image = Image.open("kto.logo.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        
        # Giriş ekranı
        self.create_welcome_screen()

    def create_welcome_screen(self):
        self.welcome_screen = tk.Toplevel(self.root)
        self.welcome_screen.title("Giriş Ekranı")
        self.welcome_screen.geometry("800x600")
        
        # Arka plan görseli
        background_label = tk.Label(self.welcome_screen, image=self.background_photo)
        background_label.place(relwidth=1, relheight=1)
        
        welcome_label = tk.Label(self.welcome_screen, text="Hoşgeldiniz!", font=("Arial", 24,"bold"), bg="lightgray")
        welcome_label.pack(pady=50)
        
        start_button = tk.Button(self.welcome_screen, text="GRAFİK OLUŞTUR", font=("Arial", 16,"bold"), command=self.open_main_screen, bg="aquamarine", fg="black")
        start_button.place(x=150, y=480)
        
        analyze_button = tk.Button(self.welcome_screen, text="VERİ ANALİZİ", font=("Arial", 16,"bold"), command=self.open_analysis_screen, bg="lightcoral", fg="black")
        analyze_button.place(x=400, y=480)
        

    def open_main_screen(self):
        self.welcome_screen.destroy()  # Giriş ekranını kapatma
        self.create_main_screen()

    def create_main_screen(self):
        self.main_screen = tk.Toplevel(self.root)
        self.main_screen.title("Dünya Bankası Verileri")
        self.main_screen.geometry("800x600")

        # Arka plan görseli
        background_label = tk.Label(self.main_screen, image=self.background_photo)
        background_label.place(relwidth=1, relheight=1)

        # Kullanıcının yıl aralıklarını girmesi için giriş kutuları ve etiketleri oluşturma
        self.create_input_widgets()

        # Grafik türü seçimi için ComboBox
        self.graph_type_label = tk.Label(self.main_screen, text="Grafik Türünü Seçin:", font=("Arial", 12,"bold"))
        self.graph_type_label.pack(pady=5)
        
        self.graph_type = ttk.Combobox(self.main_screen, values=["Çizgi", "Sütun", "Nokta", "Pasta"], font=("Arial", 12))
        self.graph_type.set("Grafik Türü")
        self.graph_type.pack(pady=5)

        # "Grafiği Göster" butonu
        self.show_graph_button = tk.Button(self.main_screen, text="Grafiği Göster", command=self.plot_graph, bg="lightblue", fg="black", font=("Arial", 12, "bold"))
        self.show_graph_button.pack(pady=20)

        # "Geri Dön" butonu
        self.back_button = tk.Button(self.main_screen, text="GERİ", command=self.go_back_to_welcome_screen, bg="red", fg="black", font=("Arial", 12, "bold"))
        self.back_button.pack(pady=20)
        # "kaydet" butonu 
        self.save_button = tk.Button(self.main_screen, text="Grafiği Kaydet", command=self.save_graph, bg="lightgreen", fg="black", font=("Arial", 12, "bold"))
        self.save_button.pack(pady=20)
        #tahmin et butonu
        self.predict_button = tk.Button(self.main_screen, text="Tahmin Yap", command=self.predict_future, bg="orange", fg="black", font=("Arial", 12, "bold"))
        self.predict_button.pack(pady=20)
        
    def create_input_widgets(self):
        self.start_year_label = tk.Label(self.main_screen, text="Başlangıç Yılı:", font=("Arial", 12,"bold"))
        self.start_year_label.pack(pady=5)
        self.start_year_entry = tk.Entry(self.main_screen, font=("Arial", 12))
        self.start_year_entry.pack(pady=5)

        self.end_year_label = tk.Label(self.main_screen, text="Bitiş Yılı:", font=("Arial", 12,"bold"))
        self.end_year_label.pack(pady=5)
        self.end_year_entry = tk.Entry(self.main_screen, font=("Arial", 12))
        self.end_year_entry.pack(pady=5)

    def plot_graph(self):
        start_year = self.start_year_entry.get()
        end_year = self.end_year_entry.get()


         
        if not start_year.isdigit() or not end_year.isdigit():
            messagebox.showerror("Hata", "Lütfen geçerli bir yıl aralığı girin.")
            return

        data_fetcher = WorldBankData("NE.TRD.GNFS.ZS", "TUR")
        years, values = data_fetcher.fetch_data(start_year, end_year)

        graph_type = self.graph_type.get()
        if graph_type == "Grafik Türü":  # Kullanıcı seçim yapmadıysa
            messagebox.showerror("Hata", "Lütfen bir grafik türü seçin!")
        
        else:
          plotter = GraphPlotter(years, values)
          plotter.plot(graph_type, trendline=True)  # Eğilim çizgisini eklemek için trendline=True ekleyin
          self.current_fig = plt.gcf()
          self.current_graph_type = graph_type
          plt.show()
    def predict_future(self):
        start_year = self.start_year_entry.get()
        end_year = self.end_year_entry.get()
        data_fetcher = WorldBankData("NE.TRD.GNFS.ZS", "TUR")
        years, values = data_fetcher.fetch_data(start_year, end_year)
        periods = 5 # Kaç dönem ileriye tahmin yapılacak
        plotter = GraphPlotter(years,values)
        future_years, predictions = plotter.predict_next_values(periods=periods, method="linear")
        
        # Tahmin edilen değerleri çiz
        plt.figure(figsize=(10, 5))
        plt.plot(years, values, marker='o', linestyle='-', color='b', label="Gerçek Değerler")
        plt.plot(future_years, predictions, marker='o', linestyle='--', color='r', label="Tahmin Edilen Değerler")
        plt.title("Veri Tahmini")
        plt.xlabel("Yıl")
        plt.ylabel("Ticaretin GSYH'ya Oranı (%)")
        plt.legend()
        plt.grid(True)
        plt.show()
        
    def go_back_to_welcome_screen(self):
        self.main_screen.destroy()  # Ana ekranı kapatma
        self.create_welcome_screen()  # Giriş ekranını tekrar gösterme
    def go_back_to_welcome_screen_from_analysis(self):
        self.analysis_screen.destroy()  # Ana ekranı kapatma
        self.create_welcome_screen()  # Giriş ekranını tekrar gösterme
    def open_analysis_screen(self):
        self.welcome_screen.destroy()  # Giriş ekranını kapatma
        self.create_analysis_screen()
    def create_analysis_screen(self):
        self.analysis_screen = tk.Toplevel(self.root)
        self.analysis_screen.title("Veri Analizi")
        self.analysis_screen.geometry("800x600")

        # # Arka plan görseli
        # background_label = tk.Label(self.analysis_screen, image=self.background_photo)
        # background_label.place(relwidth=1, relheight=1)
      
# Görseli yerleştir
        background_label = tk.Label(self.analysis_screen, image=self.background_photo)
        background_label.place(x=220, y=250)

        # Kullanıcının yıl aralıklarını girmesi için giriş kutuları ve etiketleri oluşturma
        self.create_input_widgets_for_analysis()
        self.result_label = tk.Label(self.analysis_screen, text="", font=("Arial", 12, "bold"))
        self.result_label.pack(pady=20, anchor="se", side=tk.BOTTOM)

       
    # Butonlar
    
        std_dev_button = tk.Button(self.analysis_screen, text="Standart Sapma", command=self.show_standard_deviation, bg="lightblue", fg="black", width=12, height=3,font=("Arial", 12, "bold"))
        std_dev_button.place(x=150,y=180)

        median_button = tk.Button(self.analysis_screen, text="Medyan", command=self.show_median, bg="lightblue", fg="black",width=10, height=3, font=("Arial", 12, "bold"))
        median_button.place(x=350,y=180)

        mean_button = tk.Button(self.analysis_screen, text="Ortalama", command=self.show_mean, bg="lightblue", fg="black",width=10, height=3, font=("Arial", 12, "bold"))
        mean_button.place(x=550,y=180)

     # "Geri Dön" butonu
        
        self.back_button = tk.Button(self.analysis_screen, text="GERİ", command=self.go_back_to_welcome_screen_from_analysis, bg="red", fg="black",width=10, height=3, font=("Arial", 12, "bold"))
        self.back_button.place(x=0,y=525)
        
    def create_input_widgets_for_analysis(self):
        self.start_year_label = tk.Label(self.analysis_screen, text="Başlangıç Yılı:", font=("Arial", 12,"bold"))
        self.start_year_label.pack(pady=5)
        self.start_year_entry = tk.Entry(self.analysis_screen, font=("Arial", 12))
        self.start_year_entry.pack(pady=5)

        self.end_year_label = tk.Label(self.analysis_screen, text="Bitiş Yılı:", font=("Arial", 12,"bold"))
        self.end_year_label.pack(pady=5)
        self.end_year_entry = tk.Entry(self.analysis_screen, font=("Arial", 12))
        self.end_year_entry.pack(pady=5)
   
    def show_standard_deviation(self):
        start_year = self.start_year_entry.get()
        end_year = self.end_year_entry.get()

        if not start_year.isdigit() or not end_year.isdigit():
            messagebox.showerror("Hata", "Lütfen geçerli bir yıl aralığı girin.")
            return

        data_fetcher = WorldBankData("NE.TRD.GNFS.ZS", "TUR")
        years, values = data_fetcher.fetch_data(start_year, end_year)
        plotter = GraphPlotter(years, values)
        std_dev = plotter.calculate_standard_deviation()
        # messagebox.showinfo("Standart Sapma", f"Verilerin Standart Sapması: {std_dev:.2f}")
        result_text = f"{start_year}-{end_year} arası Standart Sapma: {std_dev}"
        messagebox.showinfo("Standart Sapma", result_text)
        
        current_text = self.result_label.cget("text")
        new_text = current_text + "\n" + result_text if current_text else result_text
        self.result_label.config(text=new_text)

    def show_median(self):
        start_year = self.start_year_entry.get()
        end_year = self.end_year_entry.get()

        if not start_year.isdigit() or not end_year.isdigit():
            messagebox.showerror("Hata", "Lütfen geçerli bir yıl aralığı girin.")
            return

        data_fetcher = WorldBankData("NE.TRD.GNFS.ZS", "TUR")
        years, values = data_fetcher.fetch_data(start_year, end_year)
        plotter = GraphPlotter(years, values)
        median = plotter.calculate_median()
        # messagebox.showinfo("Medyan", f"Verilerin Medyanı: {median:.2f}")
        result_text = f"{start_year}-{end_year} arası Medyan: {median}"
        messagebox.showinfo("Medyan", result_text)
        
        current_text = self.result_label.cget("text")
        new_text = current_text + "\n" + result_text if current_text else result_text
        self.result_label.config(text=new_text)
       

    def show_mean(self):
        start_year = self.start_year_entry.get()
        end_year = self.end_year_entry.get()

        if not start_year.isdigit() or not end_year.isdigit():
            messagebox.showerror("Hata", "Lütfen geçerli bir yıl aralığı girin.")
            return

        data_fetcher = WorldBankData("NE.TRD.GNFS.ZS", "TUR")
        years, values = data_fetcher.fetch_data(start_year, end_year)
        plotter = GraphPlotter(years, values)
        mean = plotter.calculate_mean()
        # messagebox.showinfo("Ortalama", f"Verilerin Ortalaması: {mean:.2f}")
        result_text = f"{start_year}-{end_year} arası Ortalama: {mean}"
        messagebox.showinfo("Ortalama", result_text)
       
        current_text = self.result_label.cget("text")
        new_text = current_text + "\n" + result_text if current_text else result_text
        self.result_label.config(text=new_text)
    def save_graph(self):
        if hasattr(self, 'current_fig'):
            # Benzersiz dosya adı oluşturma (grafik türü + zaman damgası)
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            save_path = os.path.join(os.getcwd(), f"{self.current_graph_type}_grafik_{timestamp}.png")
            self.current_fig.savefig(save_path)
            messagebox.showinfo("Başarılı", f"Grafik kaydedildi: {save_path}")
        else:
            messagebox.showerror("Hata", "Kaydedilecek bir grafik yok. Önce grafiği oluşturun.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.withdraw()  # Ana pencereyi gizle
    root.mainloop()
   