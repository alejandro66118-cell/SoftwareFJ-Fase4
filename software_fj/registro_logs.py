"""
registro_logs.py
Configuracion del archivo de logs del sistema Software FJ.

Todos los eventos (INFO) y errores (ERROR/WARNING) se escriben en el archivo
'software_fj.log'. No se usa base de datos: el archivo de logs es el unico
almacenamiento en disco permitido por el enunciado.
"""

# Importa el modulo estandar de logging de Python
import logging
# Importa os para construir la ruta del archivo de logs
import os

# Ruta del archivo de logs: carpeta raiz del proyecto
RUTA_LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "software_fj.log")


# Funcion que crea (una sola vez) y devuelve el logger del sistema
def obtener_logger(nombre="SoftwareFJ"):
    """Devuelve un logger configurado para escribir en archivo y consola."""
    # Obtiene (o crea) el logger con el nombre indicado
    logger = logging.getLogger(nombre)
    # Si ya tiene manejadores, se devuelve tal cual para no duplicar lineas
    if logger.handlers:
        return logger
    # Nivel minimo que se registrara: INFO (eventos) y superiores (errores)
    logger.setLevel(logging.INFO)
    # Formato de cada linea: fecha, nivel, modulo y mensaje
    formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(module)s | %(message)s")
    # Manejador que escribe en el archivo de logs con codificacion UTF-8
    manejador_archivo = logging.FileHandler(RUTA_LOG, mode="a", encoding="utf-8")
    # Asigna el formato al manejador de archivo
    manejador_archivo.setFormatter(formato)
    # Agrega el manejador de archivo al logger
    logger.addHandler(manejador_archivo)
    # Evita que el mensaje se propague al logger raiz (no se duplica en consola)
    logger.propagate = False
    # Devuelve el logger listo para usar
    return logger
