from Simbolo import Simbolo
from Manejo_Archivos import leerLineas
from Automatas import *


class Analizador():
    """Tabla de símbolos en el que son almacenados todos los símbolos, tanto 
    precargados como los analizados y cargados luego del análisis.
    Al crearse inicializa su tabla de símbolos con las palabras reservadas, analiza el archivo que
    encuentre en la ruta establecida, y luego muestra la tabla completa."""
    
    def __init__(self, ruta):
        self.tabla_simbolos = []
        self._inicializarTabla()
        self._analizarArchivo(ruta)
        self.mostrarTabla()

    def _inicializarTabla(self):
        '''Inicializa tabla de simbolos con las palabras reservadas'''
        self.tabla_simbolos = [Simbolo('FUNCTION', 'Palabra Reservada'),
                               Simbolo('PROCEDURE', 'Palabra Reservada'),
                               Simbolo('PROGRAM', 'Palabra Reservada'),
                               Simbolo('WHILE', 'Palabra Reservada'),
                               Simbolo('IF', 'Palabra Reservada'),
                               Simbolo('ELSE', 'Palabra Reservada'),
                               Simbolo('THEN', 'Palabra Reservada'),
                               Simbolo('TO', 'Palabra Reservada'),
                               Simbolo('DO', 'Palabra Reservada'),
                               Simbolo('TRUE', 'Palabra Reservada'),
                               Simbolo('FALSE', 'Palabra Reservada'),
                               Simbolo('AND', 'Palabra Reservada'),
                               Simbolo('OR', 'Palabra Reservada'),
                               Simbolo('NOT', 'Palabra Reservada'),
                               Simbolo('AS', 'Palabra Reservada'),
                               Simbolo('ARRAY', 'Palabra Reservada'),
                               Simbolo('BEGIN', 'Palabra Reservada'),
                               Simbolo('END', 'Palabra Reservada'),
                               Simbolo('BREAK', 'Palabra Reservada'),
                               Simbolo('CASE', 'Palabra Reservada'),
                               Simbolo('CONTINUE', 'Palabra Reservada'),
                               Simbolo('DEFAULT', 'Palabra Reservada'),
                               Simbolo('DIV', 'Palabra Reservada'),
                               Simbolo('EXIT', 'Palabra Reservada'),
                               Simbolo('FILE', 'Palabra Reservada'),
                               Simbolo('FINALLY', 'Palabra Reservada'),
                               Simbolo('FOR', 'Palabra Reservada'),
                               Simbolo('GOTO', 'Palabra Reservada'),
                               Simbolo('MOD', 'Palabra Reservada'),
                               Simbolo('OF', 'Palabra Reservada'),
                               Simbolo('READ', 'Palabra Reservada'),
                               Simbolo('WRITE', 'Palabra Reservada'),
                               Simbolo('RECORD', 'Palabra Reservada'),
                               Simbolo('REPEAT', 'Palabra Reservada'),
                               Simbolo('SELF', 'Palabra Reservada'),
                               Simbolo('SET', 'Palabra Reservada'),
                               Simbolo('STRING', 'Palabra Reservada'),
                               Simbolo('TRY', 'Palabra Reservada'),
                               Simbolo('TYPE', 'Palabra Reservada'),
                               Simbolo('UNIT', 'Palabra Reservada'),
                               Simbolo('USES', 'Palabra Reservada'),
                               Simbolo('VAR', 'Palabra Reservada'),
                               Simbolo('WITH', 'Palabra Reservada')]

    def _getTabla(self):
        '''Devuelve la tabla de simbolo'''
        return self.tabla_simbolos

    def _buscarSimbolo(self, tabla, simbolo):
        '''Busca simbolo, comparando su lexema con los de la tabla. No diferen-
        cia mayúsculas ni minúsculas. Devuelve la posición del simbolo, o -1 si
        no se encuentra en tabla'''
        pos = -1
        for i in range(0, len(tabla)):
            if (simbolo.getLexema().upper() == tabla[i].getLexema().upper()):
                pos = i
                break
            i = i+1
        return pos

    def agregarSimbolo(self, simbolo):
        '''Agrega simbolo a tabla de simbolos, en caso de que no se encuentre'''
        tabla = self._getTabla()
        if self._buscarSimbolo(tabla, simbolo) == -1:
            tabla.append(simbolo)

    def mostrarTabla(self):
        '''Muestra la tabla, simbolo por vez: su lexema y que componente lexico
        representa'''
        tabla = self._getTabla()
        for elemento in tabla:
            print(elemento.getLexema(), ' >> ', elemento.getCompLex())
        

    def _analizarArchivo(self, nombre_archivo):
        '''Analiza el archivo, separando los distintos componentes, según los
        autómatas que utiliza'''

        lineas_archivo = leerLineas(nombre_archivo)

        for linea in lineas_archivo:
            self._analizarLinea(linea)
        
    def _analizarLinea(self, linea):
        '''Analiza cada linea, separando los distintos componentes, según los
        autómatas que utiliza'''

        pos = 0

        while pos < len(linea):
            # Almacena valores que devuelve la funcion es...
            p_aux = 0
            s_aux = Simbolo()
            # Almacena valores del simbolo con mayores caracteres reconocido
            p_max = -1
            s_max = None

            estado, p_aux, s_aux = esIdentificador(linea, pos)
            if estado and p_aux > p_max:
                p_max = p_aux
                s_max = s_aux

            estado, p_aux, s_aux = esConstanteEntera(linea, pos)
            if estado and p_aux > p_max:
                p_max = p_aux
                s_max = s_aux

            estado, p_aux, s_aux = esConstanteReal(linea, pos)
            if estado and p_aux > p_max:
                p_max = p_aux
                s_max = s_aux

            estado, p_aux, s_aux = esOperadorRelacional(linea, pos)
            if estado and p_aux > p_max:
                p_max = p_aux
                s_max = s_aux

            estado, p_aux, s_aux = esOperadorAritmetico(linea, pos)
            if estado and p_aux > p_max:
                p_max = p_aux
                s_max = s_aux

            estado, p_aux, s_aux = esPuntuacion(linea, pos)
            if estado and p_aux > p_max:
                p_max = p_aux
                s_max = s_aux

            estado, p_aux, s_aux = esAsignacion(linea, pos)
            if estado and p_aux > p_max:
                p_max = p_aux
                s_max = s_aux

            estado, p_aux, s_aux = esEspacio(linea, pos)
            if estado and p_aux > p_max:
                p_max = p_aux
                s_max = s_aux

            if s_max is not None:
                self.agregarSimbolo(s_max)

            pos = p_max+1  # +1 para que avance una posición de la máxima
