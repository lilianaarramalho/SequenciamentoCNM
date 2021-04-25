class slot(object):

    def __init__(self,id,maquina,inicio, fim, turno):

        self.id=id
        self.maquina=maquina
        self.inicio=inicio
        self.fim=fim
        self.turno=turno

    def __repr__(self):
        return str(self.id)

    def duracao(self):
        return self.fim-self.inico

