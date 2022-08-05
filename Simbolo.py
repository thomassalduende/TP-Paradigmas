class Simbolo():
    def __init__(self, lexema='', complex=''):
        self.lexema = lexema
        self.complex = complex

    def getLexema(self):
        '''Devuelve el atributo lexema del símbolo'''
        return self.lexema

    def getCompLex(self):
        '''Devuelve el atributo componente léxico del símbolo'''
        return self.complex

    def __str__(self):
        return self.getLexema(), ' >> ', self.getCompLex()