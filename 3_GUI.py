import io
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from PIL import Image, ImageTk
import requests
import csv
import pandas as pd
from requests_html import HTMLSession

class WebImageClassifierApp:
    def __init__(self, root, csv_path):
        self.root = root
        self.root.title("Web Image Classifier")
        self.session = HTMLSession()

        self.csv_path = csv_path

        # Leer el CSV
        self.df = pd.read_csv(self.csv_path, encoding='latin1')
        self.df.to_csv("backup.csv", encoding='latin1')
        self.pages = self.df['urls'].tolist()
        self.categories = self.df['word'].tolist()
        self.categorization = self.df['categorization'].tolist()
        self.current_page_index = 0

        self.max_width = 500
        self.max_height = 700

        # Configurar GUI
        self.setup_gui()

        # Mostrar la primera página
        self.load_page()

    def setup_gui(self):


        # Frame para la navegación y categorización
        nav_frame = tk.Frame(self.root)
        nav_frame.pack(padx=10, pady=10)

        # Botones de navegación
        self.prev_button = tk.Button(nav_frame, text="Anterior", command=self.prev_image)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(nav_frame, text="Siguiente", command=self.next_image)
        self.next_button.pack(side=tk.LEFT, padx=10)

        # Entrada para el número de página
        self.page_entry_label = tk.Label(nav_frame, text="Ir a imagen:")
        self.page_entry_label.pack(side=tk.LEFT, padx=10)

        self.page_entry = tk.Entry(nav_frame, width=5)
        self.page_entry.pack(side=tk.LEFT)

        self.go_to_button = tk.Button(nav_frame, text="Ir", command=self.go_to_page)
        self.go_to_button.pack(side=tk.LEFT, padx=10)

        # Etiqueta de categoría y botones de categorización
        self.category_label = tk.Label(self.root, text="Categoría:")
        self.category_label.pack(pady=5, anchor='w', side='top', fill='both')

        categorize_frame = tk.Frame(self.root)
        categorize_frame.pack(padx=10, pady=10)

        self.categorize_button_ok = tk.Button(categorize_frame, text="Buena", command=self.categorize_image_ok, bg="#8AE996")
        self.categorize_button_ok.pack(side=tk.RIGHT, padx=10)

        self.categorize_button_bad = tk.Button(categorize_frame, text="Mala", command=self.categorize_image_bad, bg="#E99698")
        self.categorize_button_bad.pack(side=tk.LEFT, padx=10)

        # Frame para la imagen y categoría
        self.image_frame = tk.Frame(self.root)
        self.image_frame.pack(padx=10, pady=10)

        self.image_label = tk.Label(self.image_frame, text="Imagen")
        self.image_label.pack(padx=10, pady=10)

        # Menú
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Guardar CSV", command=self.save_csv)


    def resize_image(self, image, max_width, max_height):
        original_width, original_height = image.size
        ratio = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        return image.resize((new_width, new_height), Image.LANCZOS)

    def load_page(self):
        url = self.pages[self.current_page_index]

        response = requests.get(url)
        self.current_image = Image.open(io.BytesIO(response.content))

        self.current_image = self.resize_image(self.current_image, self.max_width, self.max_height)
        self.img_tk = ImageTk.PhotoImage(self.current_image)
        self.image_label.config(image=self.img_tk)

        # Mostrar la categoría actual
        self.category_label.config(text=f"Categoría: {self.categories[self.current_page_index]}")

    def next_image(self):
        if self.current_page_index < len(self.pages) - 1:
            self.current_page_index += 1
            self.load_page()
        else:
            messagebox.showinfo("Fin de las páginas", "Ya has alcanzado la última página.")

    def prev_image(self):
        if self.current_page_index > 0:
            self.current_page_index -= 1
            self.load_page()
        else:
            messagebox.showinfo("Inicio de las páginas", "Estás en la primera página.")

    def go_to_page(self):
        try:
            page_number = int(self.page_entry.get()) - 1
            if 0 <= page_number < len(self.pages):
                self.current_page_index = page_number
                self.load_page()
            else:
                messagebox.showerror("Error", f"Número de página fuera de rango (1 - {len(self.pages)})")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número válido de página.")
    def categorize_image_ok(self):
        
        self.categorization[self.current_page_index] = True
        self.next_image()

    def categorize_image_bad(self):
        
        self.categorization[self.current_page_index] = False
        self.next_image()
   

    def save_csv(self):

        self.df['categorization'] = self.categorization
      
        # Guardar el CSV final
        self.df.to_csv(self.csv_path, index=False, encoding='latin1')

        messagebox.showinfo("Guardado", f"Archivo CSV guardado en {self.csv_path}")

# Inicializar la aplicación
root = tk.Tk()
app = WebImageClassifierApp(root, 'image_results_fixed.csv')
root.mainloop()