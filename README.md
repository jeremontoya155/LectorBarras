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
      <li>tkcalendar</li>
      <li>Babel</li>
      <li>Babel.numbers</li>
  </ul>

  <h2>Instalación</h2>
  <p>Para instalar las dependencias necesarias, puedes utilizar pip:</p>
  <pre><code>pip install tkinter opencv-python pyzbar openpyxl numpy tkcalendar Babel</code></pre>

  <h2>Uso</h2>
  <p>Para ejecutar la aplicación, simplemente ejecuta el archivo Python:</p>
  <pre><code>python <em>nombre_del_archivo.py</em></code></pre>

  <h2>Empaquetar la Aplicación como Ejecutable</h2>
  <p>Para convertir el script de Python en un ejecutable, puedes usar la herramienta <a href="https://pypi.org/project/auto-py-to-exe/">auto-py-to-exe</a>.</p>
  <h3>Instalación de auto-py-to-exe</h3>
  <pre><code>pip install auto-py-to-exe</code></pre>

  <h3>Uso de auto-py-to-exe</h3>
  <p>Para ejecutar la herramienta, usa el siguiente comando:</p>
  <pre><code>auto-py-to-exe</code></pre>
  <p>En la interfaz de auto-py-to-exe, selecciona el archivo Python que deseas convertir y ajusta las configuraciones según tus necesidades. Asegúrate de agregar los siguientes hidden imports:</p>
  <ul>
      <li>pyzbar</li>
      <li>cv2</li>
      <li>tkcalendar</li>
      <li>Babel</li>
      <li>Babel.numbers</li>
      <li>numpy</li>
  </ul>

  <h3>Configuraciones de auto-py-to-exe</h3>
  <ul>
      <li><strong>Script Location:</strong> Selecciona tu archivo Python.</li>
      <li><strong>Onefile:</strong> Marca esta opción para crear un único archivo ejecutable.</li>
      <li><strong>Console Window:</strong> Desmarca esta opción si no deseas que se muestre una ventana de consola.</li>
      <li><strong>Hidden Imports:</strong> Agrega los imports ocultos necesarios. Ejemplo:
          <pre><code>--hidden-import pyzbar --hidden-import cv2 --hidden-import tkcalendar --hidden-import Babel --hidden-import Babel.numbers --hidden-import numpy</code></pre>
      </li>
  </ul>

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
