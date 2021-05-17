class of(object):

    def __init__(self,id, cod_of,minutos,quantidade,codigo_material,descricao_material,material,bl,acabamento,ct,prioridade,estado,quantidade_precedencia, codigo_precedencia,descricao_precedencia,data,outsider,dim1,dim2,precedenciaBL,data_min_prec):

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
        self.id_alocada=-1
        self.vetor_maquinas=[]
        self.data_min=data_min_prec
        self.pronta_a_iniciar=0
        self.delta=prioridade
        self.id_precedencia=-1
        self.id_sucedencias=[]
        self.estado=estado
        self.quantidade_precedencia=quantidade_precedencia
        self.codigo_precedencia=codigo_precedencia
        self.descricao_precedencia=descricao_precedencia
        self.data=data
        self.precedenciaBL=precedenciaBL
        self.dim1=dim1.strip()
        self.dim2=dim2.strip()
        self.outsider=outsider

        self.id_grupos=[]
        self.quantidade_grupos=[]

        self.id_of=[]
        self.quantidade_of=[]

        self.descricao=[]

        self.quantidade_inicial=quantidade

        self.semana_real=self.data
        self.data_min_real=self.data_min

    def __repr__(self):
        return str(self.cod_of)

    def adicionar_maquinas(self,maquinas):
        self.vetor_maquinas=maquinas
