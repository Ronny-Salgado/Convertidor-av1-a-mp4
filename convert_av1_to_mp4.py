import subprocess
import os

def detectar_gpu():
    # Comprobamos si CUDA está disponible (para NVIDIA)
    if "cuda" in subprocess.getoutput("ffmpeg -encoders").lower():
        return 'cuda'
    # Comprobamos si QSV está disponible (para Intel)
    if "qsv" in subprocess.getoutput("ffmpeg -encoders").lower():
        return 'qsv'
    # Comprobamos si AMF (AMD) está disponible
    if "amf" in subprocess.getoutput("ffmpeg -encoders").lower():
        return 'amf'
    # Si no hay GPU, regresamos 'cpu'
    return 'cpu'

def convertir_av1_a_mp4(archivo_av1, archivo_mp4, actualizar_progreso, ffmpeg_path):
    try:
        # Detectar la mejor opción de GPU o CPU
        gpu = detectar_gpu()

        # Iniciar comando de ffmpeg
        comando = [ffmpeg_path, '-i', archivo_av1]

        # Aceleración por hardware
        if gpu == 'cuda':
            comando += ['-c:v', 'h264_nvenc']  # Usar GPU NVIDIA con CUDA
        elif gpu == 'qsv':
            comando += ['-c:v', 'h264_qsv']  # Usar GPU Intel con QSV
        elif gpu == 'amf':
            comando += ['-c:v', 'h264_amf']  # Usar GPU AMD con AMF
        else:
            comando += ['-c:v', 'libx264']  # Si no hay GPU, usa CPU con libx264

        comando += ['-c:a', 'aac', '-b:a', '192k', '-preset', 'fast', archivo_mp4]

        # Ejecutar ffmpeg
        proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        
        # Monitorear la salida de ffmpeg para actualizar el progreso
        while True:
            salida = proceso.stderr.readline()  # Leer stderr para obtener el progreso
            if salida == '' and proceso.poll() is not None:
                break
            
        return proceso.returncode  # Devuelve el código de salida del proceso (0 es éxito)
    except Exception as e:
        print(f"Error en la conversión: {e}")
        return 1
