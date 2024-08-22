import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from matplotlib import pyplot as plt
import pandas as pd
from backend import WorldBankData, GraphPlotter
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import merkezbankası

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
        
    def scroll_text(self, label, text):
        # Mevcut metni bir karakter sola kaydır
        new_text = text[1:] + text[0]
        # Label'in text özelliğini güncelle
        label.config(text=new_text)
        # 200 ms sonra bu fonksiyonu tekrar çağırarak animasyonu devam ettir
        self.root.after(200, self.scroll_text, label, new_text)


    def create_welcome_screen(self):
        self.welcome_screen = tk.Toplevel(self.root)
        self.welcome_screen.title("KTO İstatistik")
        self.welcome_screen.geometry("800x600")
        # Arka plan görseli
        background_label = tk.Label(self.welcome_screen, image=self.background_photo)
        background_label.place(relwidth=1, relheight=1)
        welcome_text = "HOŞGELDİNİZ!  "
        welcome_label = tk.Label(self.welcome_screen, text=welcome_text, font=("Arial", 34,"bold"), bg="lightgray")
        welcome_label.pack(pady=50)
        # Kaydırma animasyonunu başlat
        self.scroll_text(welcome_label, welcome_text)
        start_button = tk.Button(self.welcome_screen, text="GRAFİK OLUŞTUR", font=("Arial", 16,"bold"), command=self.open_selection_window, bg="aquamarine", fg="black",width=15, height=5)
        start_button.place(x=0, y=470)
        analyze_button = tk.Button(self.welcome_screen, text="VERİ ANALİZİ", font=("Arial", 16,"bold"), command=self.open_analysis_screen, bg="dodgerblue", fg="black",width=15, height=5)
        analyze_button.place(x=200, y=470)
        help_button = tk.Button(self.welcome_screen, text="YARDIM", font=("Arial", 16,"bold"), command=self.open_help_screen, bg="orange", fg="black",width=15, height=5)
        help_button.place(x=400, y=470)
        about_button = tk.Button(self.welcome_screen, text="HAKKINDA", font=("Arial", 16,"bold"), command=self.open_about_screen, bg="lightcoral", fg="black",width=15, height=5)
        about_button.place(x=600, y=470)
        

    def open_main_screen(self):
        if hasattr(self, 'selection_window'):
            self.selection_window.destroy()  # Seçim penceresini kapatma
        self.welcome_screen.destroy()  # Giriş ekranını kapatma
        self.create_main_screen()
    def create_central_bank_screen(self):
        self.central_bank_screen = tk.Toplevel(self.root)
        self.central_bank_screen.title("Merkez Bankası Verileri")
        self.central_bank_screen.geometry("800x600")
        background_label = tk.Label(self.central_bank_screen, image=self.background_photo)
        background_label.place(relwidth=1, relheight=1)
         # "Geri Dön" butonu
        self.back_button = tk.Button(self.central_bank_screen, text="GERİ", command=self.go_back_to_welcome_screen_from_central, bg="red", fg="black", width=10, height=3, font=("Arial", 12, "bold"))
        self.back_button.place(x=0,y=525)
        # Seçim menüsü
        self.combo_box = ttk.Combobox(self.central_bank_screen, values=list(merkezbankası.data_series.keys()),width=35,height=9)
        self. combo_box.set("Bir veri seçin")  # Varsayılan değer
        self.combo_box.place(x=15 , y=110)
        # Başlangıç ve bitiş tarihleri
        tk.Label(self.central_bank_screen,font=("Arial", 12,"bold"), text="Başlangıç Tarihi (gg-aa-yyyy):").place(x=0, y=10)
        self.start_date_entry = tk.Entry(self.central_bank_screen,font=("Arial", 12,"bold"))
        self.start_date_entry.place(x=230,y=10)
        tk.Label(self.central_bank_screen,font=("Arial", 12,"bold"), text="Bitiş Tarihi (gg-aa-yyyy):").place(x=0,y=60)
        self.end_date_entry = tk.Entry(self.central_bank_screen,font=("Arial", 12,"bold"))
        self.end_date_entry.place(x=230,y=60)
        # Grafiği çizme butonu
        self.plot_button = tk.Button(self.central_bank_screen, text="OLUŞTUR", font=("Arial", 14,"bold"), width=7,height=3,bg="aquamarine", fg="black",command=self.plot_central_bank_graph)
        self.plot_button.place(x=450, y=35)
       
        # Grafik türü seçimi için ComboBox
        self.graph_type_label = tk.Label(self.central_bank_screen, text="Grafik Tipi:", font=("Arial", 12,"bold"))
        self.graph_type_label.place(x=0 , y=160)
        self.graph_type = ttk.Combobox(self.central_bank_screen, values=["Çizgi", "Sütun", "Nokta", "Pasta"], font=("Arial", 12))
        self.graph_type.set("Grafik Türü")
        self.graph_type.place(x=120 , y=160)

        
    def open_central_bank_screen(self):
        if hasattr(self, 'selection_window'):
            self.selection_window.destroy()  # Seçim penceresini kapatma
        self.welcome_screen.destroy()  # Giriş ekranını kapatma
        self.create_central_bank_screen()


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
        self.graph_type_label = tk.Label(self.main_screen, text="Grafik Tipi:", font=("Arial", 12,"bold"))
        self.graph_type_label.place(x=0 , y=110)
        self.graph_type = ttk.Combobox(self.main_screen, values=["Çizgi", "Sütun", "Nokta", "Pasta"], font=("Arial", 12))
        self.graph_type.set("Grafik Türü")
        self.graph_type.place(x=120 , y=110)
        # "Grafiği Göster" butonu
        self.show_graph_button = tk.Button(self.main_screen, text="OLUŞTUR", command=self.plot_graph, bg="lightblue", fg="black",width=10, height=3, font=("Arial", 12, "bold"))
        self.show_graph_button.place(x=360,y=40)
        # "Geri Dön" butonu
        self.back_button = tk.Button(self.main_screen, text="GERİ", command=self.go_back_to_welcome_screen, bg="red", fg="black", width=10, height=3, font=("Arial", 12, "bold"))
        self.back_button.place(x=0,y=525)
        # "kaydet" butonu 
        self.save_button = tk.Button(self.main_screen, text="KAYDET", command=self.save_graph, bg="lightgreen", fg="black",width=10, height=3, font=("Arial", 12, "bold"))
        self.save_button.place(x=510,y=40)
        #tahmin et butonu
        self.predict_button = tk.Button(self.main_screen, text="TAHMİN", command=self.predict_future, bg="orange", fg="black",width=10, height=3, font=("Arial", 12, "bold"))
        self.predict_button.place(x=660,y=40)
        
        
    def create_input_widgets(self):
        self.start_year_label = tk.Label(self.main_screen, text="Başlangıç Yılı:", font=("Arial", 12,"bold"))
        self.start_year_label.place(x=0, y=10)
        self.start_year_entry = tk.Entry(self.main_screen, font=("Arial", 12))
        self.start_year_entry.place(x=120,y=10)
        self.end_year_label = tk.Label(self.main_screen, text="Bitiş Yılı:", font=("Arial", 12,"bold"))
        self.end_year_label.place(x=0, y=60)
        self.end_year_entry = tk.Entry(self.main_screen, font=("Arial", 12))
        self.end_year_entry.place(x=120, y=60)
        
        
    def plot_central_bank_graph(self):
      selected_title =self.combo_box.get()
      series_code = merkezbankası.data_series[selected_title]  
      start_date = self.start_date_entry.get()
      end_date = self.end_date_entry.get()
      graph_type = self.graph_type.get()
      try:
          if graph_type == "Grafik Türü":  # Kullanıcı seçim yapmadıysa
             messagebox.showerror("Hata", "Lütfen bir grafik türü seçin!")
          pd.to_datetime(start_date, format='%d-%m-%Y')
          pd.to_datetime(end_date, format='%d-%m-%Y')
          if pd.to_datetime(start_date) > pd.to_datetime(end_date):
             messagebox.showerror("Hata", "Başlangıç tarihi bitiş tarihinden büyük olamaz.")
             return
         
          merkezbankası.plot_data(series_code, selected_title, start_date, end_date,graph_type)
        
      except ValueError:
         messagebox.showerror("Hata", "Geçersiz tarih formatı. Tarihler 'gün-ay-yıl' formatında olmalıdır.")
    
    
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
        
        
    def go_back_to_welcome_screen_from_central(self):
        self.central_bank_screen.destroy()  # Ana ekranı kapatma
        self.create_welcome_screen()  # Giriş ekranını tekrar gösterme
        
        
    def open_analysis_screen(self):
        self.welcome_screen.destroy()  # Giriş ekranını kapatma
        self.create_analysis_screen()
        
        
    def create_analysis_screen(self):
        self.analysis_screen = tk.Toplevel(self.root)
        self.analysis_screen.title("Veri Analizi")
        self.analysis_screen.geometry("800x600")
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
            
    
            
    def open_help_screen(self):
      self.help_screen = tk.Toplevel(self.root)
      self.help_screen.title("Yardım")
      self.help_screen.geometry("600x400")
      help_label = tk.Label(self.help_screen, text="\nBu uygulamanın nasıl kullanılacağını öğrenmek \n için lütfen aşağıdaki bağlantıya tıklayınız\n", font=("Arial", 12), justify="left" ,bg="orange")
      help_label.pack(pady=20, padx=20)
      download_link = tk.Label(self.help_screen, text="İndirmek için tıklayınız", fg="blue", cursor="hand2")
      download_link.pack(pady=5)
      download_link.bind("<Button-1>", self.download_help_document)
    
    def download_help_document(self, event):
        # Yardım dokümanı yolunu belirleyin
        doc_path = "yardım.pdf"  # Yardım dokümanınızın dosya yolu

        # Kullanıcıya dosyanın nereye kaydedileceğini sor
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if save_path:
            # Dosyayı belirtilen yere kopyala
            shutil.copy(doc_path, save_path)
            tk.messagebox.showinfo("İndirme Tamamlandı", "Yardım dokümanı başarıyla indirildi!")



    def open_about_screen(self):
      self.about_screen = tk.Toplevel(self.root)
      self.about_screen.title("Hakkında")
      self.about_screen.geometry("600x400")
      about_label = tk.Label(self.about_screen, text=" Bu uygulama, Kayseri Ticaret Odası için ticaretin \n GSYH'ya oranını görselleştirmek ve analiz etmek \n amacıyla geliştirilmiştir.", font=("Arial", 12), justify="left",bg="lightcoral")
      about_label.pack(pady=20, padx=20)
      
      
    def open_selection_window(self):
        self. selection_window = tk.Toplevel(self.root)
        self.selection_window.title("Veri Seçimi")
        self.selection_window.geometry("400x200")
        label = tk.Label(self.selection_window, text="Veri kaynağını seçin:",font=("Arial", 14, "bold"))
        label.pack(pady=10)
        # Dünya Bankası verileri butonu
        world_bank_button = tk.Button(self.selection_window, text="Dünya Bankası Verileri", 
                                      command=self.open_main_screen,bg="lightblue", fg="black", width=17, height=3,font=("Arial", 12, "bold"))
        world_bank_button.pack(pady=5)
        # Merkez Bankası verileri butonu
        central_bank_button = tk.Button(self.selection_window, text="Merkez Bankası Verileri", 
                                        command=self.open_central_bank_screen , bg="lightblue", fg="black", width=17, height=3,font=("Arial", 12, "bold"))
        central_bank_button.pack(pady=5)
        
        
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.withdraw()  # Ana pencereyi gizle
    root.mainloop()
   