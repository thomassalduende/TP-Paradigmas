import os


def abrirArchivo(nombre_archivo):
    '''Realiza la apertura del archivo de texto, de la ruta especificada'''
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_completa = os.path.join(carpeta_actual, nombre_archivo)

    return open(ruta_completa)


def cerrarArchivo(archivo):
    '''Realiza el cierre del archivo de texto especificado'''
    archivo.close()


def leerLineas(nombre_archivo):
    '''Devuelve una lista de todas las líneas del archivo de texto especificado'''
    with abrirArchivo(nombre_archivo) as archivo:
        lineas = []
        for linea in archivo:
            if linea.find('') != -1:
                linea = linea[:len(linea)-1]
            lineas.append(linea)
        return lineas
