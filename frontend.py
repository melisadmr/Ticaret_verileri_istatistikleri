import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib import pyplot as plt
from backend import WorldBankData, GraphPlotter
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        
        start_button = tk.Button(self.welcome_screen, text="Dünya Bankası Verileri", font=("Arial", 16,"bold"), command=self.open_main_screen, bg="aquamarine", fg="black")
        start_button.place(x=150, y=480)

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
        self.back_button = tk.Button(self.main_screen, text="Geri Dön", command=self.go_back_to_welcome_screen, bg="lightcoral", fg="black", font=("Arial", 12, "bold"))
        self.back_button.pack(pady=20)
        
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
         plotter.plot(graph_type)
         plt.show()
        
    def go_back_to_welcome_screen(self):
        self.main_screen.destroy()  # Ana ekranı kapatma
        self.create_welcome_screen()  # Giriş ekranını tekrar gösterme

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.withdraw()  # Ana pencereyi gizle
    root.mainloop()
   