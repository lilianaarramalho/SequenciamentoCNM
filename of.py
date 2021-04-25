class of(object):

    def __init__(self,id, cod_of,minutos,quantidade,codigo_material,descricao_material,material,bl,acabamento,ct,prioridade,estado,quantidade_precedencia, codigo_precedencia,descricao_precedencia,data,outsider):

        self.id=id
        self.cod_of = cod_of
        self.t_producao = minutos
        self.quantidade = quantidade
        self.codigo_material = codigo_material
        self.descricao_material = descricao_material
        self.material=material
        self.bl=bl
        self.acabamento=acabamento
        self.ct = ct
        self.prioridade=prioridade
        self.data_inicio=15
        self.id_slot_inicio_turno=-1
        self.data_fim=-1
        self.id_alocada=0
        self.vetor_maquinas=[]
        self.data_min=99999
        self.pronta_a_iniciar=0
        self.delta=prioridade
        self.id_precedencia=-1
        self.id_sucedencias=[]
        self.estado=estado
        self.quantidade_precedencia=quantidade_precedencia
        self.codigo_precedencia=codigo_precedencia
        self.descricao_precedencia=descricao_precedencia
        self.data=data
        self.origem=[]
        self.quantidade_origem=[]
        self.precedenciaBL="PL"
        self.dim1=self.descricao_material[self.descricao_material.find("/")+4 : descricao_material.find("X")]
        self.dim2=self.descricao_material[self.descricao_material.find(self.dim1)+5:self.descricao_material.find(self.dim1)+8]
        self.outsider=outsider

        if "BL" in self.descricao_precedencia:
            if int(self.dim1)>=1000:
                self.precedenciaBL="metricas"
            else:
                self.precedenciaBL="inglesas"



    def __repr__(self):
        return str(self.cod_of)

    def adicionar_maquinas(self,maquinas):
        self.vetor_maquinas=maquinas

    def adicionar_produto(self,data_prioridade,data_entrega):
        self.vetor_data_min.append(data_prioridade)
        self.vetor_data_entrega.append(data_entrega)

    def update_data_min(self):

        self.data_min=15