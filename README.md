<h1>Extractor de Códigos de Barra</h1>
  <p>Este proyecto es una aplicación de escritorio en Python que permite extraer códigos de barras de imágenes en formato .tif y .tiff. Utiliza la biblioteca OpenCV para el procesamiento de imágenes y pyzbar para la decodificación de códigos de barras.</p>

  <h2>Requisitos</h2>
  <ul>
      <li>Python 3.x</li>
      <li>tkinter</li>
      <li>OpenCV</li>
      <li>pyzbar</li>
      <li>openpyxl</li>
      <li>numpy</li>
  </ul>

  <h2>Instalación</h2>
  <p>Para instalar las dependencias necesarias, puedes utilizar pip:</p>
  <pre><code>pip install tkinter opencv-python pyzbar openpyxl numpy</code></pre>

  <h2>Uso</h2>
  <p>Para ejecutar la aplicación, simplemente ejecuta el archivo Python:</p>
  <pre><code>python <em>nombre_del_archivo.py</em></code></pre>

  <h2>Funcionalidades</h2>
  <ul>
      <li>Seleccionar una carpeta con imágenes .tif y .tiff.</li>
      <li>Procesar las imágenes y extraer códigos de barras.</li>
      <li>Guardar los códigos de barras en un archivo Excel.</li>
      <li>Guardar una lista de códigos de receta en un archivo de texto.</li>
      <li>Guardar los errores en un archivo Excel y permitir la entrada manual de códigos para los errores.</li>
  </ul>

  <h2>Interfaz de Usuario</h2>
  <p>La aplicación tiene una interfaz gráfica simple creada con tkinter.</p>
  <ul>
      <li>Botón para seleccionar la carpeta con las imágenes.</li>
      <li>Barra de progreso para indicar el progreso del procesamiento.</li>
      <li>Mensajes de diálogo para guardar los archivos generados y manejar errores.</li>
  </ul>

  <h2>Detalles del Código</h2>
  <h3>Función <code>select_folder()</code></h3>
  <p>Abre un cuadro de diálogo para seleccionar la carpeta que contiene las imágenes a procesar.</p>

  <h3>Función <code>process_images(folder_path)</code></h3>
  <p>Procesa todas las imágenes en la carpeta seleccionada, extrae los códigos de barras y guarda los resultados en archivos Excel y de texto.</p>

  <h3>Función <code>read_barcodes(image_path)</code></h3>
  <p>Lee los códigos de barras de una imagen utilizando diversas técnicas de preprocesamiento de imágenes.</p>

  <h3>Función <code>open_tif_file(image_path)</code></h3>
  <p>Abre un archivo .tif seleccionado.</p>

  <h3>Función <code>save_recetas_to_txt(txt_path, recetas)</code></h3>
  <p>Guarda los códigos de receta en un archivo de texto.</p>

  <h2>Licencia</h2>
  <p>Este proyecto está licenciado bajo la <a href="https://opensource.org/licenses/MIT">Licencia MIT</a>.</p>
