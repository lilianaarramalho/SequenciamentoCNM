import pandas as pd
import datetime
import math
from maquina import *
from of import *
from slot import *

def calcular_hora_inicio(row):
    format='%H:%M:%S'
    if row['TURNO']==1 or ((row['TURNO']-1)/3).is_integer():
        return datetime.datetime.strptime('06:00:00',format)
    elif ((row['TURNO'])/3).is_integer():
        return datetime.datetime.strptime('22:00:00', format)
    else:
        return datetime.datetime.strptime('14:00:00', format)

def calcular_hora_fim(row):
    format='%H:%M:%S'
    if row['TURNO']==1 or ((row['TURNO']-1)/3).is_integer():
        return datetime.datetime.strptime('14:00:00',format)
    elif ((row['TURNO'])/3).is_integer():
        return datetime.datetime.strptime('06:00:00', format)
    else:
        return datetime.datetime.strptime('22:00:00', format)

def calcular_data_inicio(row):
    now = datetime.datetime.now()
    monday = now - datetime.timedelta(days=now.weekday())
    dias=math.ceil(row['TURNO']/3)-1
    result=monday + datetime.timedelta(days=dias)
    result=result.strftime("%d/%m/%Y")
    return result

def calcular_data_fim(row):

    data = datetime.datetime.strptime(row['Data'], '%m/%d/%Y')

    if row['Hora Inicio'].hour>row['Hora Fim'].hour:
        data = data + datetime.timedelta(days=1)

    data = datetime.datetime.strftime(data, '%d/%m/%Y')
    return data

def adicionar_semana(df_semanal):
    max_turno=df_semanal['TURNO'].max()

    result=df_semanal.copy()
    result['TURNO']=result['TURNO']+max_turno

    return result

def criar_slots(df,df_paragens,maquina_atual):

    inicio=df_paragens['Hora Inicio'].tolist()
    fim=df_paragens['Hora Fim'].tolist()
    slot_maq=[]
    slot_in=[]
    slot_end=[]
    slot_turno=[]
    data_inicio=[]
    hora_inicio=[]
    hora_fim=[]
    turno=[]

    for index, row in df.iterrows():
        data_inicio.append(row['data inicio'])
        hora_inicio.append(row['hora inicio'])
        hora_fim.append(row['hora fim'])
        turno.append(row['TURNO'])

    for index in range(len(data_inicio)):
        inicio_turno=hora_inicio[index]
        fim_turno=hora_fim[index]
        count_mesmo_turno=0

        print(fim_turno.hour)
        for i in range(len(inicio)):

            inicio_paragem=inicio[i]
            fim_paragem=fim[i]

            str_data=datetime.datetime.strptime('22:00','%H:%M')

            if str(inicio_turno)=="22:00:00":
                print('degbu')


            if inicio_paragem>=inicio_turno and fim_paragem<=fim_turno:

                if inicio_paragem>inicio_turno:
                    if count_mesmo_turno==0:
                        slot_in.append(str(data_inicio[index]) + ' ' + str(inicio_turno))
                    else:
                        slot_in.append(str(data_inicio[index]) + ' ' + str(fim[i-1]))

                    slot_end.append(str(data_inicio[index]) + ' ' + str(inicio_paragem))
                    slot_maq.append(maquina_atual)
                    slot_turno.append(turno[index])

                    count_mesmo_turno += 1

                else:
                    hora_inicio[index]=fim_paragem
                    inicio_turno = hora_inicio[index]

            elif inicio_paragem>=inicio_turno and inicio_turno>fim_turno and fim_paragem>fim_turno and fim_turno.hour==6: # é porque a paragem ainda é no dia anterior
                if inicio_paragem>inicio_turno:
                    if count_mesmo_turno==0:
                        slot_in.append(str(data_inicio[index]) + ' ' + str(inicio_turno))
                    else:
                        slot_in.append(str(data_inicio[index]) + ' ' + str(fim[i-1]))

                    slot_end.append(str(data_inicio[index]) + ' ' + str(inicio_paragem))
                    slot_maq.append(maquina_atual)
                    slot_turno.append(turno[index])

                    count_mesmo_turno += 1

                else:
                    hora_inicio[index]=fim_paragem
                    inicio_turno = hora_inicio[index]

            elif inicio_paragem.hour<6 and fim_paragem<=fim_turno and inicio_paragem<=inicio_turno and inicio_turno>fim_turno:

                data=datetime.datetime.strptime(data_inicio[index],'%d/%m/%Y')

                if inicio_paragem==inicio_turno:
                    hora_inicio[index]=fim_paragem
                    inicio_turno=hora_inicio[index]

                else:
                    if count_mesmo_turno==0:
                        hora=inicio_turno
                    else:
                        hora=fim[i-1]

                    if hora.hour<6:
                        data_in = data + datetime.timedelta(days=1)
                        data_in = datetime.datetime.strftime(data_in, '%d/%m/%Y')

                    else:
                        data_in=datetime.datetime.strftime(data,'%d/%m/%Y')

                    if inicio_paragem.hour<6:
                        data_out=data + datetime.timedelta(days=1)
                        data_out = datetime.datetime.strftime(data_out, '%d/%m/%Y')
                    else:
                        data_out = datetime.datetime.strftime(data, '%d/%m/%Y')


                    slot_in.append(str(data_in) + ' ' + str(hora))
                    slot_end.append(str(data_out) + ' ' + str(inicio_paragem))
                    slot_maq.append(maquina_atual)
                    slot_turno.append(turno[index])

                    count_mesmo_turno += 1

            elif inicio_paragem.hour<6 and fim_turno<inicio_turno and inicio_paragem<fim_turno:
                data = datetime.datetime.strptime(data_inicio[index], '%d/%m/%Y')

                if inicio_paragem==inicio_turno:
                    hora_inicio[index]=fim_paragem
                    inicio_turno=hora_inicio[index]

                else:

                    if count_mesmo_turno == 0:
                        hora = inicio_turno
                    else:
                        hora = fim[i - 1]

                    if hora.hour < 6:
                        data_in = data + datetime.timedelta(days=1)
                        data_in = datetime.datetime.strftime(data, '%d/%m/%Y')

                    else:
                        data_in = datetime.datetime.strftime(data, '%d/%m/%Y')

                    if inicio_paragem.hour < 6:
                        data_out = data + datetime.timedelta(days=1)
                        data_out = datetime.datetime.strftime(data, '%d/%m/%Y')
                    else:
                        data_out = datetime.datetime.strftime(data, '%d/%m/%Y')

                    slot_in.append(str(data_in) + ' ' + str(hora))
                    slot_end.append(str(data_out) + ' ' + str(inicio_paragem))
                    slot_maq.append(maquina_atual)
                    slot_turno.append(turno[index])

                    count_mesmo_turno += 1

    df_slots=pd.DataFrame({'maquina':slot_maq,'in':slot_in,'out':slot_end,'turno':slot_turno})

    return df_slots

def dividir_slots(df_slots,df_previstas):

    slots_maq=[]
    slots_in=[]
    slots_out=[]
    df_slots=df_slots[df_slots['maquina']=='CNMRETBL']

    for index,row in df_slots.iterrows():
        slots_maq.append(row['maquina'])
        slots_in.append(row['in'])
        slots_out.append(row['out'])

    for index,row in df_previstas.iterrows():
        for i in range(len(slots_in)):

            prevista_in=row['in']
            prevista_out=row['out']
            slot_in=slots_in[i]
            slot_out=slots_out[i]

            if (prevista_in>=slot_in or (prevista_in<slot_in and prevista_in>slots_in[i-1])) and prevista_out<=slot_out and row['MAQUINA']==slots_maq[i]:
                slots_out[i]=row['in']
                if slots_out[i]<=slots_in[i]:
                    del slots_in[i]
                    del slots_out[i]
                    del slots_maq[i]
                slots_in.append(row['out'])
                slots_out.append(slots_out[i])
                slots_maq.append(slots_maq[i])

            elif prevista_out>=slot_in and prevista_out<=slot_in and row['MAQUINA']==slots_maq[i]:
                del slots_in[i]
                del slots_out[i]
                del slots_maq[i]

            elif prevista_out>=slot_out and prevista_in<=slot_out and prevista_in>=slot_in and row['MAQUINA']==slots_maq[i]:
                del slots_in[i]
                del slots_out[i]
                del slots_maq[i]

            elif prevista_out>slot_out and prevista_in<slot_in and row['MAQUINA']==slots_maq[i]:
                del slots_in[i]
                del slots_out[i]
                del slots_maq[i]

            elif prevista_in<slot_in and prevista_out<=slot_out and prevista_out>=slot_in and row['MAQUINA']==slots_maq[i]:
                slots_in[i]=row['out']

    df = pd.DataFrame({'maquina': slots_maq, 'in': slots_in, 'out': slots_out})
    df=df[df['maquina']=='CNMRETBL']
    df = df.sort_values(by=['maquina', 'in'])
    print(df)

def verificar_passado(row):
    current_date = datetime.datetime.now()

    if row['out']<current_date:
        return 1
    elif row['in']<current_date and row['out']>current_date:
        return current_date
    else:
        return row['in']

def importar_acabamentos():

    #importar acabamentos com maquinas alocadas
    df_acabamentos=pd.read_csv('data/01. acabamentos.csv',sep=",",encoding='UTF-8')
    df_acabamentos['ACABAMENTO'] = df_acabamentos['ACABAMENTO'].astype(str)
    lista=df_acabamentos.columns.tolist()
    lista=lista[1:]
    df_acabamentos=pd.melt(df_acabamentos, id_vars=['ACABAMENTO'], var_name='MAQUINA', value_name='VALUE')
    return df_acabamentos

def importar_clientes():

    #importar clientes com maquinas alocadas
    df_clientes = pd.read_csv('data/02. clientes.csv', sep=",", encoding='UTF-8')
    df_clientes['Cliente'] = df_clientes['Cliente'].astype(str)
    lista = df_clientes.columns.tolist()
    lista = lista[1:]
    df_clientes = pd.melt(df_clientes, id_vars=['Cliente'], var_name='MAQUINA', value_name='VALUE')
    return df_clientes

def import_maquinas():

    global maquinas
    df_maquinas=pd.read_csv('data/03. maquinas.csv', sep=",", encoding='UTF-8')

    count_maquinas = 0
    maquinas=[]

    for index, row in df_maquinas.iterrows():
        new_maquina = maquina(count_maquinas, row['CENTRO DE TRABALHO'], row['SUBGRUPO'], row['MAQUINA'], row['OEE'])
        maquinas.append(new_maquina)
        count_maquinas += 1

    return maquinas

def import_slots():

    df_semanal=pd.read_csv('data/04. disponibilidade semanal.csv',sep=",",encoding='UTF-8')
    df_semanal = pd.melt(df_semanal, id_vars=['MAQUINA'], var_name='TURNO', value_name='VALUE')
    df_semanal['TURNO'] = df_semanal['TURNO'].astype(int)

    df_semanal = df_semanal.append(adicionar_semana(df_semanal))

    df_semanal['hora inicio']=df_semanal.apply(lambda row:calcular_hora_inicio(row),axis=1)
    df_semanal['hora inicio']=pd.to_datetime(df_semanal['hora inicio'],format='%H:%M:%S', errors='coerce').dt.time

    df_semanal['hora fim'] = df_semanal.apply(lambda row: calcular_hora_fim(row), axis=1)
    df_semanal['hora fim'] = pd.to_datetime(df_semanal['hora fim'], format='%H:%M:%S', errors='coerce').dt.time

    df_semanal['data inicio']=df_semanal.apply(lambda row: calcular_data_inicio(row),axis=1)

    df_paragens=pd.read_csv('data/05. paragens diarias.csv',sep=',',encoding= 'unicode_escape')
    df_paragens['Hora Inicio']=pd.to_datetime(df_paragens['Hora Inicio'],format='%H:%M',errors='coerce').dt.time
    df_paragens['Hora Fim'] = pd.to_datetime(df_paragens['Hora Fim'], format='%H:%M', errors='coerce').dt.time

    #criar slots para cada uma das máquinas
    lista_maquinas=df_semanal.MAQUINA.unique()
    df_slots = pd.DataFrame(columns=['maquina', 'in', 'out'])

    for index in range(len(lista_maquinas)):
        maquina_atual=lista_maquinas[index]
        df=df_semanal[df_semanal['MAQUINA']==maquina_atual]

        df_slots=df_slots.append(criar_slots(df,df_paragens,maquina_atual))

    df_slots['in'] = pd.to_datetime(df_slots['in'],format='%d/%m/%Y %H:%M:%S',errors='coerce')
    df_slots['out'] = pd.to_datetime(df_slots['out'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
    df_slots=df_slots.drop_duplicates()
    df_slots=df_slots.sort_values(by=['maquina','in'])

    #partir slots com paragens previstas
    #TODO: VER MELHOR QUESTÃO DAS PARAGENS IMPREVISTAS
    df_previstas=pd.read_csv('data/06. outras paragens.csv',sep=",",encoding= 'UTF-8')
    df_previstas=df_previstas.dropna()
    if df_previstas.shape[0]!=0:
        df_previstas['Hora Fim'] = pd.to_datetime(df_previstas['Hora Fim'], format='%H:%M', errors='coerce').dt.time
        df_previstas['Hora Inicio'] = pd.to_datetime(df_previstas['Hora Inicio'], format='%H:%M', errors='coerce').dt.time
        df_previstas['data fim']=df_previstas.apply(lambda row: calcular_data_fim(row), axis=1)
        df_previstas['Data'] = pd.to_datetime(df_previstas['Data'], format='%m/%d/%Y', errors='coerce')
        df_previstas['Data'] = df_previstas['Data'].apply(lambda x: datetime.datetime.strftime(x, '%d/%m/%Y'))
        df_previstas['out']=df_previstas['data fim'].astype(str) + ' ' + df_previstas['Hora Fim'].astype(str)
        df_previstas['in'] = df_previstas['Data'].astype(str) + ' ' + df_previstas['Hora Inicio'].astype(str)
        df_previstas['in']=pd.to_datetime(df_previstas['in'],format='%d/%m/%Y %H:%M:%S',errors='coerce')
        df_previstas['out'] = pd.to_datetime(df_previstas['out'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
        dividir_slots(df_slots,df_previstas)

    return df_slots

def slots_to_mins():
    df_slots = import_slots()
    df=df_slots.copy()
    current_date=datetime.datetime.now()

    df['in']=df.apply(lambda row: verificar_passado(row),axis=1)
    df=df[df['in']!=1]
    df['in']=df.apply(lambda row: pd.Timedelta(row['in']-current_date).total_seconds()/60,axis=1)
    df['out'] = df.apply(lambda row: pd.Timedelta(row['out'] - current_date).total_seconds() / 60, axis=1)
    df['capacidade'] = df['out']-df['in']

    return df

def alocar_slots():

    df_slots=slots_to_mins()
    global maquinas
    global slots
    slots=[]
    count_slots = 0

    for index,row in df_slots.iterrows():

        for id_maquina in range(len(maquinas)):

            if row['maquina']==maquinas[id_maquina].nome or row['maquina']==maquinas[id_maquina].ct:

                new_slot = slot(count_slots, id_maquina, row['in'], row['out'], row['turno'])
                slots.append(new_slot)
                maquinas[id_maquina].vetor_slots.append(count_slots)
                count_slots += 1

    return slots

def definir_capacidades():

    global maquinas

    #definir a capacidade das maquinas para cada turno
    for index in range(len(maquinas)):

        turnos = []
        count_turnos=0

        for i in range(len(maquinas[index].vetor_slots)):

            capacidade = slots[maquinas[index].vetor_slots[i]].fim - slots[maquinas[index].vetor_slots[i]].inicio

            if slots[maquinas[index].vetor_slots[i]].turno in turnos:

                id_turno = turnos.index(slots[maquinas[index].vetor_slots[i]].turno)
                #print('id do turno ' + str(id_turno))

                maquinas[index].update_turno(id_turno, capacidade)

            else:

                count_turnos +=1

                turnos.append(slots[maquinas[index].vetor_slots[i]].turno)

                maquinas[index].adicionar_turno(slots[maquinas[index].vetor_slots[i]].id, capacidade)

def verificar_outsider(df):

    lista=[]

    for index,row in df.iterrows():
        componente=row['Componente']
        df_componente=df[(df['Material']==componente) & (df['Centro trabalho']=='CNMSERPL')]
        if df_componente.empty==False:
            lista.append(row['Ordem'])

    return lista

def first_row_as_headers(df):

    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header

    return df

def data_min():

    global df_bruto

    df = pd.read_csv('data/10. stock mes.csv', sep=";", encoding="UTF-8")
    df = first_row_as_headers(df)
    df = df.dropna()
    df['dia'] = df['Lot'].str[4:6]
    df['mes'] = df['Lot'].str[6:8]
    df['ano'] = df['Lot'].str[8:]
    df['data'] = df['dia'] + "/" + df['mes'] + "/" + df['ano']
    df = df[df['MaterialName'].str.contains("BL CC").fillna(False)]
    df = df[df['Lot'].str.contains("AGB").fillna(False)]
    df = df[~df['data'].str.contains("[a-zA-Z]").fillna(False)]

    df['data'] = pd.to_datetime(df['data'], dayfirst=True, errors='coerce')

    df = df[['MaterialKey', 'Total', 'MaterialName', 'data']]
    df['Total'] = df['Total'].astype(int)
    df['MaterialKey'] = df['MaterialKey'].astype(int)
    df['acabamento'] = df['MaterialName'].str.split(' ').str[3]
    df = df[df['acabamento'] == '000']
    df['MaterialName'] = df['MaterialName'].str.upper()
    df['dim'] = df['MaterialName'].str.split(' ').str[4]
    df['dim'] = df['dim'].str.split('X').str[0]
    df['dim'] = df['dim'].astype(int)
    df = df[df['dim'] >= 930]
    df['material']=df['MaterialName'].str.split(' ').str[2]
    df['material']=df['material'].astype(int)

    # adicionar tempo de estabilização

    df_est=pd.read_csv('data/11. tempo estabilizacao.csv',sep=",",encoding='UTF-8')

    df=df.merge(df_est,on="material",how="left")

    df['data'] = df.apply(lambda row: row['data'] + pd.DateOffset(days=row['dias']),axis=1)

    df = df.groupby(['MaterialKey', 'data']).sum() \
        .groupby(level=0).cumsum().reset_index()

    print(df[df['MaterialKey']==70001631])

    df = df.reset_index()

    df_bruto=df.copy()

    return df_bruto

def calcular_data_bruto(row):

    global df_bruto

    componente = row['Componente']
    if componente==70001631:
        print('componente')
    quantidade = row['Qtd. componente']
    df_componente = df_bruto[(df_bruto['MaterialKey'] == componente) & (df_bruto['Total'] >= quantidade)]
    df_data = df_bruto[df_bruto['MaterialKey'] == componente]

    if row['Ordem']==1600059821:
        print('hello')
    if df_componente.empty == False:
        linha = df_componente.iloc[0]
        data = linha['data']
        df_bruto['Total'] = df_bruto.apply(lambda x: x['Total']-quantidade if x['MaterialKey'] == componente else x['Total'], axis=1)
        return data
    elif df_componente.empty==True and df_data.empty==False:
        data=datetime.datetime.now()+datetime.timedelta(days=7)
        return data
    else:
        return datetime.datetime.now()

def atualizar_data(row):

    if row['data_min_prec']<=0:
        return 0
    else:
        return row['data_min_prec']

def import_ovs():
    data_min()
    global df_bruto

    df_ofs=pd.read_csv('data/08. ofs.csv',encoding='UTF-8',sep=";")
    df_ofs=df_ofs.fillna(0)
    df_ofs['Ordem'] = df_ofs['Ordem'].astype(int)
    df_ofs['Qtd.teórica']=df_ofs['Qtd.teórica'].astype(float)

    # verificar cliente final - Assumimos CCS quando não tem OV.

    df_ovs = pd.read_csv('data/09. cliente_final.csv', encoding='UTF-8', sep=";")
    df_ovs = df_ovs[['Ordem', 'Planeador', 'Ordem Venda / Transf', 'Componente']]
    df_mto=df_ovs.copy()
    df_mto=df_mto[['Ordem Venda / Transf','Planeador']]
    df_mto=df_mto.dropna()
    df_mto=df_mto.drop_duplicates()
    df_ofs=df_ofs.merge(df_mto,left_on="Ordem Venda / Transf",right_on="Ordem Venda / Transf",how='left')
    df_ofs=df_ofs.sort_values(by='Ordem Venda / Transf')
    df_ofs['Planeador']=df_ofs['Planeador'].fillna('CCS')
    df_ofs.loc[(df_ofs.Planeador != 'CCS'),'Planeador']='Ext'

    # filtrar centros de trabalho

    lista=['CNMRETBL','CNMSERPL','CNMLAMLX','CNMLAMPL']
    df_ofs=df_ofs[df_ofs['Centro trabalho'].isin(lista)]

    #para ver as que já foram concluídas e quantidade declarada

    df_cubo=pd.read_csv('data/07. cubo mes.csv',encoding='UTF-8',sep=";")
    df_cubo = df_cubo.iloc[3:]
    new_header = df_cubo.iloc[0]
    df_cubo = df_cubo[1:]
    df_cubo.columns = new_header
    df_cubo=df_cubo[['OrderName','OrderOperationStatus','Total']]
    df_cubo['order_name']=df_cubo['OrderName'].str.split('.').str[1]
    df_cubo = df_cubo.fillna(0)
    df_cubo['order_name'] = df_cubo['order_name'].astype(int)
    df_cubo['Total']=df_cubo['Total'].astype(float)

    df_ofs=df_ofs.merge(df_cubo,left_on="Ordem",right_on="order_name",how="left")
    df_ofs=df_ofs[df_ofs['OrderOperationStatus']!='Encerada']
    df_ofs['Total']=df_ofs['Total'].fillna(0)
    df_ofs['quantidade']=df_ofs['Qtd.teórica']-df_ofs['Total']
    df_ofs['quantidade precedencia']=df_ofs['quantidade']/df_ofs['Qtd.teórica']*df_ofs['Qtd. componente']
    df_ofs['minutos'] = df_ofs['quantidade'] / df_ofs['Qtd.teórica'] * df_ofs['Capacidade Alocada']*60
    df_ofs=df_ofs[df_ofs['quantidade']>1]

    df_ofs['acabamento'] = df_ofs['Denominação'].str.split('/').str[-1]
    df_ofs['acabamento'] = df_ofs['acabamento'].str.split(' ').str[0]

    df_ofs['Material'] = df_ofs['Material'].astype(int)
    df_ofs['Componente'] = df_ofs['Componente'].astype(int)

    df_ofs['outsider']=0

    lista=verificar_outsider(df_ofs)
    df_ofs.loc[df_ofs.Ordem.isin(lista), 'outsider'] = 1

    #verificar data minima de cada of tendo em conta o precedente e a quantidade necessária.
    df_ofs['data_min_prec']=df_ofs.apply(lambda row: calcular_data_bruto(row),axis=1)
    df_ofs['data_min_prec'] = df_ofs.apply(lambda row: pd.Timedelta(row['data_min_prec'] - datetime.datetime.now()).total_seconds() / 60, axis=1)
    df_ofs['data_min_prec']=df_ofs.apply(lambda row: atualizar_data(row),axis=1)

    df_ofs['material']=df_ofs['Denominação'].str.split('/').str[0]
    df_ofs['material']=df_ofs['material'].str[-4:]

    df_ofs['Denominação']=df_ofs['Denominação'].str.upper()

    df_ofs['dim1']=df_ofs['Denominação'].str.split('X').str[0]
    df_ofs['dim1']=df_ofs['dim1'].str.split('/').str[1]
    df_ofs['dim1'] = df_ofs['dim1'].str[4:]
    df_ofs['dim1']=df_ofs['dim1'].astype(int)

    df_ofs['dim2']=df_ofs['Denominação'].str.split('X').str[1]
    df_ofs['dim2']=df_ofs['dim2'].str.split(' ').str[0]
    df_ofs['dim2'] = df_ofs['dim2'].astype(int)

    df_ofs['dim3']=df_ofs['Denominação'].str.split('X').str[2]
    df_ofs['dim3'] = df_ofs['dim3'].str.split(' ').str[0]

    return df_ofs










