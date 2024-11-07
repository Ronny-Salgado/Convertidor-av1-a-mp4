import os
import time  # Asegúrate de importar el módulo time
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from convert_av1_to_mp4 import convertir_av1_a_mp4
import threading

class ConvertidorAV1aMP4:
    def __init__(self, root):
        self.root = root
        self.root.title("Convertidor de AV1 a MP4")
        self.root.geometry("500x300")

        # Habilita la funcionalidad de arrastrar y soltar
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.arrastrar_archivo)

        # Texto de Instrucción
        self.label = tk.Label(root, text="Arrastra o selecciona un archivo AV1 para convertir:")
        self.label.pack(pady=10)

        # Botón de conversión
        self.boton_convertir = tk.Button(root, text="Convertir a MP4", command=self.convertir)
        self.boton_convertir.pack(pady=20)

        # Spinner de carga (animación de puntos suspensivos)
        self.spinner_label = tk.Label(root, text="Convirtiendo", font=("Helvetica", 16))
        self.spinner_label.pack(pady=10)
        self.spinner_label.pack_forget()

        # Archivo seleccionado
        self.archivo_av1 = None
        self.ffmpeg_path = None

        # Variable para la animación de puntos
        self.spinner_running = False

    def seleccionar_ffmpeg(self):
        # Permitir al usuario seleccionar ffmpeg.exe si no está en el PATH
        self.ffmpeg_path = filedialog.askopenfilename(
            title="Selecciona el archivo ffmpeg.exe",
            filetypes=[("Ejecutable", "*.exe")]
        )
        if not self.ffmpeg_path:
            messagebox.showerror("Error", "No se seleccionó ffmpeg. La conversión no se puede realizar.")

    def arrastrar_archivo(self, event):
        self.archivo_av1 = event.data.strip('{}')  # Elimina llaves en caso de que haya espacios en la ruta
        self.label.config(text=f"Archivo seleccionado: {os.path.basename(self.archivo_av1)}")

    def convertir(self):
        if not self.archivo_av1:
            messagebox.showwarning("Advertencia", "Por favor selecciona un archivo AV1.")
            return

        # Obtener el directorio y el nombre del archivo de entrada
        directorio, nombre_archivo = os.path.split(self.archivo_av1)
        nombre_convertido = f"Convertido_{nombre_archivo.replace('.av1', '.mp4')}"
        archivo_mp4 = os.path.join(directorio, nombre_convertido)

        # Verificar si ffmpeg está disponible o solicitar la ruta
        if not self.ffmpeg_path:
            self.seleccionar_ffmpeg()
            if not self.ffmpeg_path:
                return

        # Mostrar el spinner de carga
        self.spinner_label.pack()
        self.spinner_running = True

        # Iniciar la conversión en un hilo separado para evitar que la interfaz se congele
        threading.Thread(target=self.iniciar_conversion, args=(archivo_mp4,)).start()
        threading.Thread(target=self.animar_spinner).start()

    def animar_spinner(self):
        while self.spinner_running:
            for estado in ["Convirtiendo.", "Convirtiendo..", "Convirtiendo..."]:
                if not self.spinner_running:
                    break
                self.spinner_label.config(text=estado)
                self.root.update_idletasks()
                time.sleep(0.5)

    def iniciar_conversion(self, archivo_mp4):
        # Llama a la función de conversión
        resultado = convertir_av1_a_mp4(self.archivo_av1, archivo_mp4, self.actualizar_progreso, self.ffmpeg_path)

        # Detener el spinner de carga
        self.spinner_running = False
        self.spinner_label.pack_forget()

        # Mostrar mensaje de finalización según el resultado
        if resultado == 0:
            messagebox.showinfo("Conversión Completa", f"Archivo convertido exitosamente a {archivo_mp4}")
        else:
            messagebox.showerror("Error", "Error durante la conversión.")

    def actualizar_progreso(self, progreso):
        # Esta función queda vacía ya que no se usará la barra de progreso
        pass


if __name__ == "__main__":
    root = TkinterDnD.Tk()  # Cambia `tk.Tk()` por `TkinterDnD.Tk()`
    app = ConvertidorAV1aMP4(root)
    root.mainloop()
