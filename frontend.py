import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from backend import WorldBankAPI

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Dünya Bankası Verileri")
        self.root.geometry("800x600")
        self.root.withdraw()  # Bu satır ana pencereyi gizler
        

        self.backend = WorldBankAPI()

        self.background_image = Image.open("kto.logo.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.create_welcome_screen()

    def create_welcome_screen(self):
        self.welcome_screen = tk.Toplevel(self.root)
        self.welcome_screen.title("Giriş Ekranı")
        self.welcome_screen.geometry("800x600")
        
        background_label = tk.Label(self.welcome_screen, image=self.background_photo)
        background_label.place(relwidth=1, relheight=1)
        
        welcome_label = tk.Label(self.welcome_screen, text="HOŞGELDİNİZ!", font=("Arial", 40,"bold"), bg="lightgray")
        welcome_label.pack(pady=50)
        
        start_button = tk.Button(self.welcome_screen, text="Dünya Bankası Verileri", font=("Arial", 16,"bold"), command=self.open_main_screen, bg="aquamarine", fg="black")
        start_button.place(x=150, y=480)
    def open_main_screen(self):
        self.welcome_screen.destroy()
        self.create_main_screen()

    def create_main_screen(self):
        self.main_screen = tk.Toplevel(self.root)
        self.main_screen.title("Dünya Bankası Verileri")
        self.main_screen.geometry("800x600")

        background_label = tk.Label(self.main_screen, image=self.background_photo)
        background_label.place(relwidth=1, relheight=1)

        button_style = {
            "bg": "aquamarine",
            "fg": "black",
            "font": ("Arial", 14, "bold"),
            "padx": 10,
            "pady": 5
        }

        self.start_year_label = tk.Label(self.main_screen, text="Başlangıç Yılı:", font=("Arial", 14, "bold"))
        self.start_year_label.pack(pady=5)
        self.start_year_entry = tk.Entry(self.main_screen, font=("Arial", 12))
        self.start_year_entry.pack(pady=5)

        self.end_year_label = tk.Label(self.main_screen, text="Bitiş Yılı:", font=("Arial", 14, "bold"))
        self.end_year_label.pack(pady=5)
        self.end_year_entry = tk.Entry(self.main_screen, font=("Arial", 12))
        self.end_year_entry.pack(pady=5)

        self.show_graph_button = tk.Button(self.main_screen, text="GRAFİK ÇİZ", command=self.plot_graph, **button_style)
        self.show_graph_button.place(x=500, y=70)
        
        self.back_button = tk.Button(self.main_screen, text="GERİ", command=self.go_back, **button_style)

 

    def plot_graph(self):
        try:
            start_year = self.start_year_entry.get()
            end_year = self.end_year_entry.get()

            if not start_year.isdigit() or not end_year.isdigit():
                 messagebox.showerror("Geçersiz Girdi", "Yıl aralıkları geçerli değil. Lütfen geçerli yıllar giriniz.")
                 return

            start_year = int(start_year)
            end_year = int(end_year)
            
            years, values = self.backend.fetch_data(start_year, end_year)
            
            plt.figure(figsize=(10, 5))
            plt.plot(years, values, marker='o', linestyle='-', color='b')

            plt.title(f'Ticaretin GSYH\'ya Oranı - Türkiye ({years[0]}-{years[-1]})', fontsize=14)
            plt.xlabel('Yıl', fontsize=12)
            plt.ylabel('Ticaretin GSYH\'ya Oranı (%)', fontsize=12)

            plt.ylim(min(values) - 5, max(values) + 5)
            plt.grid(True)

            if hasattr(self, 'canvas'):
                self.canvas.get_tk_widget().destroy()
            
            self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.main_screen)
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
