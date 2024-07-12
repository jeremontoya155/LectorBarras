import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import cv2
from pyzbar.pyzbar import decode
import openpyxl as xl

# Función para seleccionar la carpeta
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        process_images(folder_path)

# Función para procesar las imágenes y extraer códigos de barra
def process_images(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith(".tif")]
    total_files = len(files)
    progress_bar['maximum'] = total_files
    
    wb = xl.Workbook()
    ws = wb.active
    ws.title = "Codigos de Barra"
    ws.append(["Receta", "Autorizacion"])

    recetas = []

    for i, filename in enumerate(files):
        image_path = os.path.join(folder_path, filename)
        barcodes = read_barcodes(image_path)
        if barcodes:
            ws.append(barcodes)
            recetas.append(barcodes[0])  # Añadir el primer código de barra (Receta) a la lista
        progress_bar['value'] = i + 1
        root.update_idletasks()

    # Pedir al usuario dónde guardar el archivo Excel
    excel_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if excel_path:
        wb.save(excel_path)
        messagebox.showinfo("Proceso completado", f"Se ha generado el archivo Excel en:\n{excel_path}")

    # Pedir al usuario dónde guardar el archivo de texto
    txt_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if txt_path:
        save_recetas_to_txt(txt_path, recetas)
        messagebox.showinfo("Proceso completado", f"Se ha generado el archivo de texto en:\n{txt_path}")

    progress_bar['value'] = 0  # Resetear la barra de progreso

# Función para leer códigos de barra de una imagen
def read_barcodes(image_path):
    try:
        image = cv2.imread(image_path)
        height, width, _ = image.shape

        # Decodificar los códigos de barra en la imagen
        barcodes = decode(image)

        if barcodes:
            # Ordenar los códigos de barra por su posición vertical (y)
            barcodes_sorted = sorted(barcodes, key=lambda x: x.rect.top)

            decoded_codes = []
            for barcode in barcodes_sorted:
                # Intentar decodificar el código de barra en varias codificaciones
                for encoding in ["utf-8", "latin1", "ascii"]:
                    try:
                        barcode_data = barcode.data.decode(encoding)
                        decoded_codes.append(barcode_data)
                        break
                    except UnicodeDecodeError:
                        continue

            # Asegurarse de que siempre haya al menos dos códigos
            while len(decoded_codes) < 2:
                decoded_codes.append("")

            return decoded_codes[:2]
        
        return ["", ""]  # No se encontraron suficientes códigos de barra

    except Exception as e:
        print(f"Error al procesar la imagen {image_path}: {e}")
        return ["", ""]  # Manejo básico de errores para continuar con otras imágenes

# Función para guardar los números de receta en un archivo de texto
def save_recetas_to_txt(txt_path, recetas):
    try:
        with open(txt_path, "w") as txt_file:
            for receta in recetas:
                txt_file.write(f"{receta}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Error al guardar el archivo de texto: {e}")

# Configuración de la interfaz de usuario
root = tk.Tk()
root.title("Extractor de Códigos de Barra")
root.geometry("600x300")
root.configure(bg="#2c3e50")

style = ttk.Style(root)
style.theme_use("clam")
style.configure("TButton", font=("Helvetica", 12, "bold"), padding=10, background="#2980b9", foreground="#ecf0f1")
style.map("TButton", background=[("active", "#3498db")])
style.configure("TLabel", font=("Helvetica", 12, "bold"), background="#2c3e50", foreground="#ecf0f1")
style.configure("TProgressbar", thickness=30, troughcolor="#34495e", background="#2980b9")

label = ttk.Label(root, text="Selecciona la carpeta con imágenes .tif:")
label.pack(pady=20)

button = ttk.Button(root, text="Seleccionar Carpeta", command=select_folder)
button.pack(pady=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate", length=500)
progress_bar.pack(pady=20)

root.mainloop()
