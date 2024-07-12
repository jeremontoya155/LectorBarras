import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
import cv2
import pyzbar.pyzbar as pyzbar
import openpyxl as xl
import numpy as np

# Función para seleccionar la carpeta
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        process_images(folder_path)

# Función para procesar las imágenes y extraer códigos de barra
def process_images(folder_path):
    # Extensiones de archivos de imagen comunes
    image_extensions = [".tif", ".tiff"]
    files = [f for f in os.listdir(folder_path) if any(f.lower().endswith(ext) for ext in image_extensions)]
    total_files = len(files)
    progress_bar['maximum'] = total_files

    wb = xl.Workbook()
    ws = wb.active
    ws.title = "Codigos de Barra"
    ws.append(["Receta", "Autorizacion", "Ruta Archivo"])

    errores_wb = xl.Workbook()
    errores_ws = errores_wb.active
    errores_ws.title = "Errores"
    errores_ws.append(["Archivo", "Ruta Completa"])

    recetas = []

    for i, filename in enumerate(files):
        image_path = os.path.join(folder_path, filename)
        barcodes = read_barcodes(image_path)
        if barcodes:
            ws.append(barcodes + [image_path])
            recetas.append(barcodes[0])  # Añadir el primer código de barra (Receta) a la lista
        else:
            errores_ws.append([filename, image_path])
        progress_bar['value'] = i + 1
        root.update_idletasks()

    if messagebox.askyesno("Proceso completado", "Desea cargar manualmente los valores de recetas para los errores antes de continuar?"):
        for row in errores_ws.iter_rows(min_row=2, values_only=True):
            filename, image_path = row
            receta = simpledialog.askstring("Entrada manual", f"Ingrese el código de receta para {filename}:")
            autorizacion = simpledialog.askstring("Entrada manual", f"Ingrese el código de autorización para {filename}:")
            if receta and autorizacion:
                ws.append([receta, autorizacion, image_path])
                recetas.append(receta)

    # Pedir al usuario dónde guardar el archivo Excel de códigos de barra
    excel_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if excel_path:
        wb.save(excel_path)
        messagebox.showinfo("Proceso completado", f"Se ha generado el archivo Excel en:\n{excel_path}")

    # Pedir al usuario dónde guardar el archivo de texto de recetas
    txt_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if txt_path:
        save_recetas_to_txt(txt_path, recetas)
        messagebox.showinfo("Proceso completado", f"Se ha generado el archivo de texto en:\n{txt_path}")

    # Pedir al usuario dónde guardar el archivo Excel de errores
    errores_excel_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if errores_excel_path:
        errores_wb.save(errores_excel_path)
        messagebox.showinfo("Proceso completado", f"Se ha generado el archivo Excel de errores en:\n{errores_excel_path}")

    progress_bar['value'] = 0  # Resetear la barra de progreso

    # Obtener lista de archivos de errores .tif para abrir
    errores_tif_files = [filename for filename, _ in errores_ws.iter_rows(min_row=2, values_only=True)
                         if filename.lower().endswith((".tif", ".tiff"))]

    # Preguntar al usuario si desea abrir los archivos .tif de errores
    if errores_tif_files:
        if messagebox.askyesno("Abrir archivos de errores", "¿Desea abrir los archivos .tif de errores ahora?"):
            for filename in errores_tif_files:
                image_path = os.path.join(folder_path, filename)
                open_tif_file(image_path)

# Función para leer códigos de barra de una imagen
def read_barcodes(image_path):
    try:
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        height, width = image.shape

        # Técnicas de preprocesamiento mejoradas
        preprocessings = [
            lambda img: img,
            lambda img: cv2.resize(img, (width * 2, height * 2)),
            lambda img: cv2.GaussianBlur(img, (5, 5), 0),
            lambda img: cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2),
            lambda img: cv2.threshold(img, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
            lambda img: cv2.Canny(img, 100, 200)  # Detección de bordes como nueva técnica
        ]

        for preprocess in preprocessings:
            processed_image = preprocess(image)
            barcodes = pyzbar.decode(processed_image)

            if barcodes:
                # Procesamiento y validación mejorados
                decoded_codes = []
                for barcode in sorted(barcodes, key=lambda x: x.rect.top):
                    for encoding in ["utf-8", "latin1", "ascii"]:
                        try:
                            barcode_data = barcode.data.decode(encoding)
                            # Validación de formato (ejemplo: si esperas un código de 13 dígitos)
                            if len(barcode_data) == 13:
                                decoded_codes.append(barcode_data)
                                break
                        except UnicodeDecodeError:
                            continue

                if len(decoded_codes) >= 2:
                    return decoded_codes[:2]

        # Si no se encontraron códigos de barras, prueba técnicas de contraste adicionales
        additional_preprocessings = [
            lambda img: cv2.equalizeHist(img),
            lambda img: cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2),
            lambda img: cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1],
            lambda img: cv2.morphologyEx(img, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))
        ]

        for preprocess in additional_preprocessings:
            processed_image = preprocess(image)
            barcodes = pyzbar.decode(processed_image)

            if barcodes:
                decoded_codes = []
                for barcode in sorted(barcodes, key=lambda x: x.rect.top):
                    for encoding in ["utf-8", "latin1", "ascii"]:
                        try:
                            barcode_data = barcode.data.decode(encoding)
                            if len(barcode_data) == 13:
                                decoded_codes.append(barcode_data)
                                break
                        except UnicodeDecodeError:
                            continue

                if len(decoded_codes) >= 2:
                    return decoded_codes[:2]

        # Si no se encontraron códigos de barras después de aplicar todas las técnicas de contraste
        # Prueba enderezar la imagen y recortar la parte superior
        edges = cv2.Canny(image, 100, 200)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

        if lines is not None:
            angles = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
                angles.append(angle)

            angle = np.median(angles)
            M = cv2.getRotationMatrix2D((width // 2, height // 2), angle, 1)
            rotated = cv2.warpAffine(image, M, (width, height))

            # Recortar la parte superior de la imagen
            top_crop = int(height * 0.25)
            rotated = rotated[top_crop:, :]

            # Aplicar técnicas de preprocesamiento a la imagen enderezada y recortada
            for preprocess in preprocessings + additional_preprocessings:
                processed_image = preprocess(rotated)
                barcodes = pyzbar.decode(processed_image)

                if barcodes:
                    decoded_codes = []
                    for barcode in sorted(barcodes, key=lambda x: x.rect.top):
                        for encoding in ["utf-8", "latin1", "ascii"]:
                            try:
                                barcode_data = barcode.data.decode(encoding)
                                if len(barcode_data) == 13:
                                    decoded_codes.append(barcode_data)
                                    break
                            except UnicodeDecodeError:
                                continue

                    if len(decoded_codes) >= 2:
                        return decoded_codes[:2]

        # Si no se encontraron códigos de barras después de enderezar y recortar
        return []

    except Exception as e:
        print(f"Error al procesar la imagen {image_path}: {e}")
        return []

# Función para abrir el archivo .tif seleccionado
def open_tif_file(image_path):
    try:
        if os.path.exists(image_path):
            os.startfile(image_path)
    except Exception as e:
        print(f"No se pudo abrir la imagen {image_path}: {e}")

# Función para guardar las recetas en un archivo de texto
def save_recetas_to_txt(txt_path, recetas):
    try:
        with open(txt_path, 'w') as f:
            for receta in recetas:
                f.write(receta + "\n")
    except Exception as e:
        print(f"Error al guardar el archivo de texto {txt_path}: {e}")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Extractor de Códigos de Barra")
root.geometry("600x400")
root.config(background="#2c3e50")

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12, "bold"), padding=10, background="#3498db", foreground="black")
style.map("TButton", background=[("active", "#2980b9")])

title_label = ttk.Label(root, text="Extractor de Códigos de Barra", font=("Helvetica", 16, "bold"), background="#2c3e50", foreground="white")
title_label.pack(pady=20)

select_button = ttk.Button(root, text="Seleccionar Carpeta", command=select_folder)
select_button.pack(pady=20)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=20)

root.mainloop()
