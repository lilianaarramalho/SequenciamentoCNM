class maquina(object):

    def __init__(self,id,ct,subgrupo,nome,oee):
        self.nome=nome
        self.id = id
        self.ct=ct
        self.vetor_slots=[]
        self.vetor_capacidade=[]
        self.vetor_capacidade_inicial=[]
        self.id_slot_inicio_turno=[]
        self.vetor_materiais=[]
        self.vetor_dimensoes=[]
        self.min_alocada=15
        self.oee=oee
        self.bl=""
        self.subgrupo=subgrupo
        # setups diferentes turno. guardar dimensoes

    def __repr__(self):
        return str(self.nome)

    def adicionar_turno(self,id_slot,capacidade):
        self.vetor_capacidade.append(capacidade)
        self.vetor_capacidade_inicial.append(capacidade)
        self.id_slot_inicio_turno.append(id_slot)

    def update_turno(self,index,capacidade):
        self.vetor_capacidade[index]=self.vetor_capacidade[index]+capacidade
        self.vetor_capacidade_inicial[index]=self.vetor_capacidade_inicial[index]+capacidade

    def diminuir_capacidade(self,index,capacidade):

        #print('capacidade in: ' +str(self.vetor_capacidade[index]) + 'turno' + str(index) )

        if capacidade>self.vetor_capacidade[index]:

            remanescente=capacidade - self.vetor_capacidade[index]
            self.vetor_capacidade[index] = 0

            #retorna remanescente
            #print('capacidade out: ' + str(self.vetor_capacidade[index])+ ' turno ' + str(index))
            #print('remanescente: ' + str(remanescente))

            return remanescente

        else:

            self.vetor_capacidade[index] = self.vetor_capacidade[index] - capacidade

            #print('capacidade out: ' + str(self.vetor_capacidade[index])+ 'turno' + str(index))
            #print('remanescente: ' + str(0))
            return 0
