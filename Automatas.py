#En esta librería se encuentran las implementaciones de todas las funciones referidas a los autómatas

import string
from Simbolo import Simbolo

numeros = string.digits  # Conjutno digitos
letras = string.ascii_letters  # Conjunto letras
simbolos = string.punctuation  # Simbolos puntuación
espacios = string.whitespace  # Espacios en blanco: tab, saltos linea, etc.
op_relacionales = ['>', '<', '=', '>=', '<=', '<>']
op_aritmeticos = ['+', '-', '/', '*']
s_puntuaciones = ';()[]'


def deltaIdentificador(estado, simbolo):
    '''Reconoce transiciones de automata de identificador'''
    if (estado == 0):
        if simbolo in letras:
            return 1
        else:
            return 2
    elif (estado == 1):
        if (simbolo in letras+numeros+'_'):
            return 1
        else:
            return 2
    else:
        return 2


def deltaConstanteEntera(estado, simbolo):
    '''Reconoce transiciones de automata de constante entera'''
    if (estado == 0):
        if simbolo in numeros:
            return 1
        elif simbolo == '-':
            return 2
        else:
            return 3
    elif (estado == 1):
        if (simbolo in numeros):
            return 1
        else:
            return 3
    elif (estado == 2):
        if simbolo in numeros:
            return 1
        else:
            return 3
    else:
        return 3


def deltaConstanteReal(estado, simbolo):
    '''Reconoce transiciones de automata de constante real'''
    if (estado == 0):
        if simbolo in numeros:
            return 1
        elif simbolo == '-':
            return 3
        else:
            return 5
    elif (estado == 1):
        if simbolo in numeros:
            return 1
        elif simbolo == '.':
            return 2
        else:
            return 5
    elif (estado == 2):
        if simbolo in numeros:
            return 4
        else:
            return 5
    elif (estado == 3):
        if simbolo in numeros:
            return 1
        else:
            return 5
    elif (estado == 4):
        if simbolo in numeros:
            return 4
        else:
            return 5
    elif (estado == 5):
        return 5


def deltaOperadorRelacional(estado, simbolo):
    '''Reconoce transiciones de automata de operador relacional'''
    if estado == 0:
        if simbolo == '<':
            return 2
        elif simbolo == '=':
            return 1
        elif simbolo == '>':
            return 3
        else:
            return 4
    elif estado == 1:
        return 4
    elif estado == 2:
        if simbolo == '>' or simbolo == '=':
            return 1
        else:
            return 4
    elif estado == 3:
        if simbolo == '=':
            return 1
        else:
            return 4
    else:
        return 4


def deltaOperadorAritmetico(estado, simbolo):
    '''Reconoce transiciones de automata de operador aritmetico'''
    if estado == 0:
        if simbolo in op_aritmeticos:
            return 1
        else:
            return 2
    else:
        return 2


def deltaAsignacion(estado, simbolo):
    '''Reconoce transiciones de automata de asignación'''
    if estado == 0:
        if simbolo == ':':
            return 1
        else:
            return 3
    if estado == 1:
        if simbolo == '=':
            return 2
        else:
            return 3
    if estado == 2 or estado == 3:
        return 3


def esIdentificador(linea, posicion):
    '''Reconoce si una subcadena pertenece a el tipo de componente lexico
    identificador. Devuelve este resultado, el indice de la cadena en el que
    la subcadena perteneció al componente, y el símbolo(con dicho lexema y el
    tipo de componente léxico)'''
    F = [1]
    e_muertos = [2]
    # sigma = letras + numeros + "_"
    estado_actual = 0
    lexema = ''
    ind = posicion
    # Indice donde el indice de cuando el estado era era final
    ind_aux = -1

    while (ind < (len(linea))) and (estado_actual not in e_muertos):
        caracter = linea[ind]
        estado_actual = deltaIdentificador(estado_actual, caracter)

        if estado_actual in F:
            lexema = linea[posicion:ind+1]
            ind_aux = ind
        ind += 1

    if ind_aux != -1:
        return True, ind_aux, Simbolo(lexema, 'IDENTIFICADOR')
    else:
        return False, posicion, None


def esConstanteEntera(linea, posicion):
    '''Reconoce si una subcadena pertenece a el tipo de componente lexico
    contante entera. Devuelve este resultado, el indice de la cadena en el que
    la subcadena perteneció al componente, y el símbolo(con dicho lexema y el
    tipo de componente léxico)'''
    F = [1]
    e_muertos = [3]
    # sigma = letras + numeros + s_puntuaciones
    estado_actual = 0
    lexema = ''
    ind = posicion
    # Indice donde el indice de cuando el estado era era final
    ind_aux = -1

    while (ind < (len(linea))) and (estado_actual not in e_muertos):
        caracter = linea[ind]
        estado_actual = deltaConstanteEntera(estado_actual, caracter)

        if estado_actual in F:
            lexema = linea[posicion:ind+1]
            ind_aux = ind
        ind += 1

    if ind_aux != -1:
        return True, ind_aux, Simbolo(lexema, 'CONSTANTE ENTERA')
    else:
        return False, posicion, None


def esConstanteReal(linea, posicion):
    '''Reconoce si una subcadena pertenece a el tipo de componente lexico
    constante real. Devuelve este resultado, el indice de la cadena en el que
    la subcadena perteneció al componente, y el símbolo(con dicho lexema y el
    tipo de componente léxico)'''
    F = [1, 4]
    e_muertos = [5]
    # sigma = numeros + '-' + '.'
    estado_actual = 0
    lexema = ''
    ind = posicion
    # Indice donde el indice de cuando el estado era era final
    ind_aux = -1

    while (ind < (len(linea))) and (estado_actual not in e_muertos):
        caracter = linea[ind]
        estado_actual = deltaConstanteReal(estado_actual, caracter)

        if estado_actual in F:
            lexema = linea[posicion:ind+1]
            ind_aux = ind
        ind += 1

    if ind_aux != -1:
        return True, ind_aux, Simbolo(lexema, 'CONSTANTE REAL')
    else:
        return False, posicion, None


def especificarComplexOpRel(lexema):
    '''Define el tipo específico de op relacional'''
    if lexema == '>':
        return 'Operador: MAYOR'
    elif lexema == '<':
        return 'Operador: MENOR'
    elif lexema == '=':
        return 'Operador: IGUAL'
    elif lexema == '>=':
        return 'Operador: MAYORIGUAL'
    elif lexema == '<=':
        return 'Operador: MENORIGUAL'
    elif lexema == '<>':
        return 'Operador: DISTINTO'


def esOperadorRelacional(linea, posicion):
    '''Reconoce si una subcadena pertenece a el tipo de componente lexico
    op relacional. Devuelve este resultado, el indice de la cadena en el que
    la subcadena perteneció al componente, y el símbolo(con dicho lexema y el
    tipo de componente léxico)'''
    F = [1, 2, 3]
    e_muertos = [4]
    # sigma = op_relacionales
    estado_actual = 0
    lexema = ''
    ind = posicion
    # Indice donde el indice de cuando el estado era era final
    ind_aux = -1

    while (ind < (len(linea))) and (estado_actual not in e_muertos):
        caracter = linea[ind]
        estado_actual = deltaOperadorRelacional(estado_actual, caracter)

        if estado_actual in F:
            lexema = linea[posicion:ind+1]
            ind_aux = ind
        ind += 1

    if ind_aux != -1:
        return True, ind_aux, Simbolo(lexema, especificarComplexOpRel(lexema))
    else:
        return False, posicion, None


def especificarComplexOpAri(lexema):
    '''Define el tipo específico de op aritmetico'''
    if lexema == '+':
        return 'Operador: MAS'
    elif lexema == '-':
        return 'Operador: MENOS'
    elif lexema == '/':
        return 'Operador: COCIENTE'
    else:
        return 'Operador: PRODUCTO'


def esOperadorAritmetico(linea, posicion):
    '''Reconoce si una subcadena pertenece a el tipo de componente lexico
    op aritmetico. Devuelve este resultado, el indice de la cadena en el que
    la subcadena perteneció al componente, y el símbolo(con dicho lexema y el
    tipo de componente léxico)'''
    F = [1]
    e_muertos = [2]
    # sigma = op_aritmeticos
    estado_actual = 0
    lexema = ''
    ind = posicion
    # Indice donde el indice de cuando el estado era era final
    ind_aux = -1

    while (ind < (len(linea))) and (estado_actual not in e_muertos):
        caracter = linea[ind]
        estado_actual = deltaOperadorAritmetico(estado_actual, caracter)

        if estado_actual in F:
            lexema = linea[posicion:ind+1]
            ind_aux = ind
        ind += 1

    if ind_aux != -1:
        return True, ind_aux, Simbolo(lexema, especificarComplexOpAri(lexema))
    else:
        return False, posicion, None


def especificarComplexPuntuacion(lexema):
    '''Define el tipo específico de simbolo de puntuación'''
    if lexema == ':':
        return 'DOS PUNTOS'
    elif lexema == ';':
        return 'PUNTO Y COMA'
    elif lexema == '(':
        return 'PARENTESIS IZQ'
    elif lexema == ')':
        return 'PARENTESIS DER'
    elif lexema == '[':
        return 'CORCHETE IZQ'
    elif lexema == ']':
        return 'CORCHETE DER'
    elif lexema == '.':
        return 'PUNTO'
    else:
        return 'SIMBOLO GENERICO'


def esPuntuacion(linea, posicion):
    '''Reconoce si una subcadena pertenece a el tipo de componente lexico de
    simbolo de puntuación. Devuelve este resultado, el indice de la cadena en
    el que la subcadena perteneció al componente, y el símbolo(con dicho lexema
    y el tipo de componente léxico)'''
    caracter = linea[posicion]
    if simbolos.find(caracter) != -1:
        return True, posicion, Simbolo(caracter, especificarComplexPuntuacion(caracter))
    else:
        return False, posicion, None


def esAsignacion(linea, posicion):
    '''Reconoce si una subcadena pertenece a el tipo de componente lexico de
    asignación. Devuelve este resultado, el indice de la cadena en el que
    la subcadena perteneció al componente, y el símbolo(con dicho lexema y el
    tipo de componente léxico)'''
    F = [2]
    e_muertos = [3]
    # sigma = [':', '=']
    estado_actual = 0
    lexema = ''
    ind = posicion
    # Indice donde el indice de cuando el estado era era final
    ind_aux = -1

    while (ind < (len(linea))) and (estado_actual not in e_muertos):
        caracter = linea[ind]
        estado_actual = deltaAsignacion(estado_actual, caracter)

        if estado_actual in F:
            lexema = linea[posicion:ind+1]
            ind_aux = ind
        ind += 1

    if ind_aux != -1:
        return True, ind_aux, Simbolo(lexema, 'ASIGNACION')
    else:
        return False, posicion, None


def esEspacio(linea, posicion):
    '''Reconoce si una subcadena pertenece a el tipo de componente lexico de
    los distintos espacios. Devuelve este resultado'''
    comprobacion = linea[posicion] == ' '
    return comprobacion, posicion, None
