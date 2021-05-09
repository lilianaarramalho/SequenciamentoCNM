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

        for i in range(len(inicio)):

            inicio_paragem=inicio[i]
            fim_paragem=fim[i]

            str_data=datetime.datetime.strptime('22:00','%H:%M')


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

    df = pd.read_csv('data/10. stock mes.csv', sep=",", encoding="ISO-8859-1")
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
    df.rename(columns={'material': 'material'}, inplace=True)

    # adicionar tempo de estabilização

    df_est=pd.read_csv('data/11. tempo estabilizacao.csv',sep=",",encoding='UTF-8')
    df_est['material'] = df_est['material'].astype(int)

    df=df.merge(df_est,left_on='material',right_on='material',how="left")

    df['data'] = df.apply(lambda row: row['data'] + pd.DateOffset(days=row['dias']),axis=1)

    df = df.groupby(['MaterialKey', 'data']).sum() \
        .groupby(level=0).cumsum().reset_index()

    df = df.reset_index()

    df_bruto=df.copy()

    return df_bruto

def calcular_data_bruto(row):

    global df_bruto

    componente = row['Componente']
    quantidade = row['Qtd. componente']
    df_componente = df_bruto[(df_bruto['MaterialKey'] == componente) & (df_bruto['Total'] >= quantidade)]
    df_data = df_bruto[df_bruto['MaterialKey'] == componente]

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

def calcular_bl(row):

    if row['Centro trabalho']=='CNMLAMPL' or row['Centro trabalho']=='CNMLAMLX':
        if row['dim1']>=1000:
            return "metricas"
        else:
            return "inglesas"
    else:
        return "PL"

def import_ovs():

    data_min()
    global df_bruto

    header_list = ["Name", "Dept", "Start Date"]
    df_ofs=pd.read_csv('data/08. ofs.csv',encoding='ISO-8859-1',sep=',',header=0)
    df_ofs=df_ofs.fillna(0)
    df_ofs.columns
    df_ofs['Ordem'] = df_ofs['Ordem'].astype(int)
    df_ofs['Qtd.teórica']=df_ofs['Qtd.teórica'].astype(float)

    # verificar cliente final - Assumimos CCS quando não tem OV.

    df_ovs = pd.read_csv('data/09. cliente_final.csv', encoding='ISO-8859-1', sep=",")
    df_ovs = df_ovs[['Ordem', 'Planeador', 'Ordem Venda / Transf', 'Componente']]
    df_mto=df_ovs.copy()
    df_mto=df_mto[['Ordem Venda / Transf','Planeador']]
    df_mto=df_mto.dropna()
    df_mto=df_mto.drop_duplicates()
    df_mto=df_mto.sort_values(by='Planeador')
    df_ofs=df_ofs.merge(df_mto,left_on="Ordem Venda / Transf",right_on="Ordem Venda / Transf",how='left')
    df_ofs=df_ofs.sort_values(by='Ordem Venda / Transf')
    df_ofs['Planeador']=df_ofs['Planeador'].fillna('CCS')
    df_ofs.loc[(df_ofs.Planeador != 'CCS'),'Planeador']='Ext'
    df_ofs=df_ofs.drop_duplicates(['Ordem'], keep="first")
    df_ofs_toremove=df_ofs[(df_ofs['Semana']<datetime.datetime.now().isocalendar()[1]-2) & (df_ofs['Centro trabalho']=='CNMRETBL')]
    df_ofs=pd.concat([df_ofs, df_ofs_toremove, df_ofs_toremove]).drop_duplicates(keep=False)

    # filtrar centros de trabalho

    lista=['CNMRETBL','CNMSERPL','CNMLAMLX','CNMLAMPL']
    df_ofs=df_ofs[df_ofs['Centro trabalho'].isin(lista)]

    #para ver as que já foram concluídas e quantidade declarada

    df_cubo=pd.read_csv('data/07. cubo mes.csv',encoding='ISO-8859-1',sep=",")
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
    df_por_fechar=df_ofs[df_ofs['quantidade']<=1]
    df_por_fechar.to_csv('data/14. ordens por encerrar.csv', index=False)
    df_ofs=df_ofs[df_ofs['quantidade']>1]
    df_ofs=df_ofs.sort_values(by='Semana')

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

    df_ofs['dim3']=df_ofs['Denominação'].str.split('X').str[2]
    df_ofs['dim3'] = df_ofs['dim3'].str.split(' ').str[0]

    df_ofs['precedenciaBl']=df_ofs.apply(lambda row: calcular_bl(row),axis=1)

    return df_ofs

def calcular_prioridade(semana):

    semana_atual=datetime.datetime.now().isocalendar()[1]
    return semana-semana_atual

def import_ofs():

    global ofs
    global maquinas

    ofs=[]

    df_ofs=import_ovs()
    df_acabamentos=importar_acabamentos()


    for index,row in df_ofs.iterrows():

        #id, cod_of,minutos,quantidade,codigo_material,descricao_material,material,bl,acabamento,ct,prioridade,estado,quantidade_precedencia, codigo_precedencia,descricao_precedencia,data,outsider,dim1,dim2,precedenciaBL)
        cod_of=row['Ordem']
        minutos=row['minutos']
        quantidade=row['quantidade']
        codigo_material=row['Material']
        descricao_material=row['Denominação']
        material=row['material']
        bl=row['dim3']
        acabamento=row['acabamento']
        ct=row['Centro trabalho']

        if ct=='CNMRETBL':
            prioridade=calcular_prioridade(datetime.datetime.now().isocalendar()[1])
        else:
            prioridade=calcular_prioridade(row['Semana'])
        estado=0
        quantidade_precedencia=row['Qtd. componente']
        codigo_precedencia=row['Componente']
        descricao_precedencia=row['Denominação componente']
        data=row['Semana']
        outsider=row['outsider']
        dim1=row['dim1']
        dim2=row['dim2']
        precedenciaBL=row['precedenciaBl']
        data_min=row['data_min_prec']

        #todo adicionar estado em produção - pedir à ana ligeiro para adicionar maquina

        new_of=of(index, cod_of,minutos,quantidade,codigo_material,descricao_material,material,bl,acabamento,ct,prioridade,estado,quantidade_precedencia, codigo_precedencia,descricao_precedencia,data,outsider,dim1,dim2,precedenciaBL,data_min)
        ofs.append(new_of)

        id_maquinas=[]

        if ct=="CNMLAMPL":
            lista_maquinas = df_acabamentos[(df_acabamentos['ACABAMENTO']==acabamento) & (df_acabamentos['VALUE']==1)]
            lista_maquinas=lista_maquinas['MAQUINA'].tolist()
            for j in range(len(lista_maquinas)):
                for i in range(len(maquinas)):
                    if maquinas[i].nome==lista_maquinas[j]:
                        id_maquinas.append(i)
        else:
            for i in range(len(maquinas)):
                if maquinas[i].nome == ct:
                    id_maquinas.append(i)

        new_of.vetor_maquinas = id_maquinas

    return ofs

def import_stocks():

    global materialkey
    global stock
    materialkey = []
    stock=[]

    df_stocks = pd.read_csv('data/10. stock mes.csv', sep=",",error_bad_lines=False)
    df_stocks=df_stocks.dropna()
    df_stocks= df_stocks.iloc[1:]
    df_stocks = df_stocks.rename(columns={'Sum Quantity': 'MaterialKey', 'Unnamed: 3': 'Total'}, inplace=False)

    print(df_stocks)
    df_stocks['MaterialKey'] = df_stocks['MaterialKey'].astype(int)
    df_stocks['Total'] = df_stocks['Total'].astype(float)
    df_stocks = df_stocks.groupby(['MaterialKey'])[["Total"]].sum()
    df_stocks=df_stocks.reset_index()

    count_refs = 0

    for index, row in df_stocks.iterrows():

        materialkey.append(row['MaterialKey'])

        stock.append(row['Total'])

        count_refs += 1

    df_stocks.to_csv('data/15. stocks importados.csv')

    return materialkey,stock

def get_ids(lista):

    ids=[]

    for index in range(len(lista)):
        ids.append(index)

    return ids

def sort_delta(ids,vetor):

    ids.sort(key=lambda x: (vetor[x].estado,vetor[x].delta,vetor[x].descricao_material,vetor[x].acabamento,vetor[x].quantidade,vetor[x].ct), reverse=False)
    ids.sort(key=lambda x: (vetor[x].ct), reverse=True)

    return ids

def get_limite(precedenciaBL):

    limite=0

    if precedenciaBL == "metricas":
        limite = 15
    elif precedenciaBL == 'inglesas':
        limite = 12

    return limite

def criar_grupo(id,quantidade,descricao):

    global grupos
    global ofs



    cod_of = ofs[id].cod_of
    minutos = quantidade/ofs[id].quantidade*ofs[id].t_producao
    codigo_material = ofs[id].codigo_material
    descricao_material = ofs[id].descricao_material
    material = ofs[id].material
    bl = ofs[id].bl
    acabamento = ofs[id].acabamento
    ct = ofs[id].ct
    prioridade = ofs[id].prioridade
    estado = 0
    quantidade_precedencia = math.ceil(quantidade/ofs[id].quantidade*ofs[id].quantidade_precedencia)
    codigo_precedencia = ofs[id].codigo_precedencia
    descricao_precedencia = ofs[id].descricao_precedencia
    data = ofs[id].data
    outsider = ofs[id].outsider
    dim1 = ofs[id].dim1
    dim2 = ofs[id].dim2
    data_min=ofs[id].data_min
    precedenciaBL = ofs[id].precedenciaBL
    index=len(grupos)

    new_grupo=of(index, cod_of,minutos,quantidade,codigo_material,descricao_material,material,bl,acabamento,ct,prioridade,estado,quantidade_precedencia, codigo_precedencia,descricao_precedencia,data,outsider,dim1,dim2,precedenciaBL,data_min)
    grupos.append(new_grupo)

    ofs[id].id_grupos.append(index)
    ofs[id].quantidade_grupos.append(quantidade)

    new_grupo.id_of.append(id)
    new_grupo.quantidade_of.append(quantidade)
    new_grupo.vetor_maquinas=ofs[id].vetor_maquinas
    new_grupo.descricao=new_grupo.ct + ' ' + descricao

    for index in range(len(ofs[id].id_sucedencias)):
        new_grupo.id_sucedencias.append(ofs[id].id_sucedencias[index])

def get_match_ids(lista,match):
    result = []
    for i, x in enumerate(lista):
        if x==match:
            result.append(i)
    return result

def update_grupo(id,quantidade,id_grupo):

    global grupos
    global ofs

    grupos[id_grupo].quantidade+=quantidade
    grupos[id_grupo].t_producao+=quantidade/ofs[id].quantidade*ofs[id].t_producao
    precedencia=math.ceil(quantidade/ofs[id].quantidade*ofs[id].quantidade_precedencia)
    grupos[id_grupo].quantidade_precedencia+=precedencia

    ofs[id].id_grupos.append(id_grupo)
    ofs[id].quantidade_grupos.append(quantidade)

    grupos[id_grupo].id_of.append(id)
    grupos[id_grupo].quantidade_of.append(quantidade)


    if len(ofs[id].vetor_maquinas)<len(grupos[id_grupo].vetor_maquinas):
        grupos[id_grupo].vetor_maquinas=ofs[id].vetor_maquinas

    if ofs[id].delta<grupos[id_grupo].delta:
        grupos[id_grupo].delta=ofs[id].delta

    if ofs[id].data_min>grupos[id_grupo].data_min:
        grupos[id_grupo].data_min=ofs[id].data_min

    for index in range(len(ofs[id].id_sucedencias)):
        grupos[id_grupo].append(ofs[id].id_sucedencias[index])

def alocar_lista_de_grupos(id_of, quantidade_of, blocos, limite,new_descricao):

    global grupos
    global ofs

    descricao=[]
    quantidade=[]

    n_ofs = blocos // limite
    quantidade_grupo = quantidade_of * limite / blocos
    blocos_remanescentes = blocos - n_ofs * limite
    quantidade_remanescente = quantidade_of * blocos_remanescentes / blocos

    for i in range(n_ofs):
        criar_grupo(id_of, quantidade_grupo,new_descricao)
        descricao.append(new_descricao)
        quantidade_bl = limite
        quantidade.append(quantidade_bl)

    if quantidade_remanescente > 1:
        criar_grupo(id_of, quantidade_remanescente,new_descricao)
        descricao.append(new_descricao)
        quantidade_bl = blocos_remanescentes
        quantidade.append(quantidade_bl)

    return descricao,quantidade

def group_material_dim(ids,ct):

    global ofs
    global maquinas
    global grupos

    ids_ct=[]
    descricao=[]
    quantidade=[]

    for index in range(len(ids)):
        id=ids[index]
        if ofs[id].ct==ct:
            ids_ct.append(id)

    for index in range(len(ids_ct)):

        id=ids_ct[index]
        new_descricao=str(ofs[id].material) + " " + str(ofs[id].dim1) + " " + str(ofs[id].dim2)
        if 'P050' in new_descricao:
            print('debug')
        blocos=math.ceil(ofs[id].quantidade_precedencia)
        limite=get_limite(ofs[id].precedenciaBL)
        quantidade_of=ofs[id].quantidade

        if new_descricao in descricao:
            ids_grupos=get_match_ids(descricao,new_descricao)
            count=0
            while blocos>0 and count<len(ids_grupos):
                id_grupo=ids_grupos[count]
                quantidade_utilizada=quantidade[id_grupo]
                if quantidade_utilizada+blocos<=limite:
                    update_grupo(id,quantidade_of,id_grupo)
                    quantidade[id_grupo] += blocos
                    blocos=0
                elif quantidade_utilizada<limite:
                    restante=limite-quantidade_utilizada
                    restante_of=restante/math.ceil(ofs[id].quantidade_precedencia)*ofs[id].quantidade
                    update_grupo(id, restante_of,id_grupo)
                    quantidade[id_grupo] += restante
                    blocos=blocos-restante
                count+=1
            if blocos>0:
                quantidade_of=blocos/math.ceil(ofs[id].quantidade_precedencia)*ofs[id].quantidade
                descricao_toappend,quantidade_toappend=alocar_lista_de_grupos(id, quantidade_of, blocos, limite,new_descricao)
                for i in range(len(descricao_toappend)):
                    descricao.append(descricao_toappend[i])
                    quantidade.append(quantidade_toappend[i])
        else:
            descricao_toappend, quantidade_toappend = alocar_lista_de_grupos(id, quantidade_of, blocos, limite,
                                                                             new_descricao)
            for i in range(len(descricao_toappend)):
                descricao.append(descricao_toappend[i])
                quantidade.append(quantidade_toappend[i])

    return grupos

def group_dim(ids,ct):

    global ofs
    global maquinas
    global grupos

    ids_ct=[]
    descricao=[]

    for index in range(len(ids)):
        id=ids[index]
        if ofs[id].ct==ct:
            ids_ct.append(id)

    for index in range(len(ids_ct)):
        id=ids_ct[index]
        new_descricao=str(ofs[id].dim1) + " " + str(ofs[id].dim2)
        blocos=math.ceil(ofs[id].quantidade_precedencia)
        limite=20
        t_producao=ofs[id].t_producao
        quantidade_of=ofs[id].quantidade

        if new_descricao in descricao:

            ids_grupos=get_match_ids(descricao,new_descricao)
            count=0

            while blocos>0 and count<len(ids_grupos):

                id_grupo=ids_grupos[count]

                if t_producao<=limite:
                    update_grupo(id,quantidade_of,id_grupo)
                    blocos=0

                count+=1

            if blocos>0:
                criar_grupo(id,ofs[id].quantidade,new_descricao)
                descricao.append(new_descricao)
        else:
            criar_grupo(id, ofs[id].quantidade, new_descricao)
            descricao.append(new_descricao)


    return grupos

def group_material(ids,ct):

    global ofs
    global maquinas
    global grupos

    ids_ct = []
    descricao = []
    quantidade = []

    for index in range(len(ids)):
        id = ids[index]
        if ofs[id].ct == ct:
            ids_ct.append(id)

    for index in range(len(ids_ct)):
        id = ids_ct[index]
        new_descricao = str(ofs[id].material)
        blocos = math.ceil(ofs[id].quantidade_precedencia)
        limite = get_limite(ofs[id].precedenciaBL)
        quantidade_of = ofs[id].quantidade
        if new_descricao in descricao:
            id_grupo = descricao.index(new_descricao)
            update_grupo(id, quantidade_of, id_grupo)
        else:
            criar_grupo(id,quantidade_of,new_descricao)

    return grupos

def criar_total_grupos(id_ofs):

    global grupos
    global ofs

    grupos=[]
    group_material_dim(id_ofs, "CNMLAMPL")
    group_material_dim(id_ofs, "CNMLAMLX")
    group_material(id_ofs, "CNMSERPL")
    group_material(id_ofs, "CNMRETBL")

    return grupos

def verificar_precedencias(vetor):


    n_impossivel=0
    impossivel=False
    por_planear=[]

    for id in range(len(vetor)):
        of=vetor[id].cod_of

        if id==34:
            print('debug')

        for index in range(len(vetor[id].id_of)):
            index_of=vetor[id].id_of[index]
            if ofs[index_of].cod_of==1600057531:
                print('debug')

        if vetor[id].id_precedencia==-1:
            codigo_precedencia=vetor[id].codigo_precedencia
            descricao_precedencia=vetor[id].descricao_precedencia
            if descricao_precedencia[:2]=="BL" and codigo_precedencia in materialkey:
                id_material=materialkey.index(codigo_precedencia)
                quantidade_material=vetor[id].quantidade_precedencia
                stock_material=stock[id_material]
                if stock_material>=quantidade_material:
                    stock[id_material]=stock[id_material]-quantidade_material
                    stock_material=stock[id_material]
                    vetor[id].pronta_a_iniciar = 1
                elif "/000" in descricao_precedencia:
                    vetor[id].pronta_a_iniciar=0
                    n_impossivel += 1

                elif "/ORT" in descricao_precedencia:
                    encontrei=False
                    id_precedencia=0
                    while encontrei==False and id_precedencia<len(vetor):
                        if vetor[id].codigo_precedencia==vetor[id_precedencia].codigo_material and vetor[id_precedencia].quantidade + stock[id_material]>=vetor[id].quantidade_precedencia :
                            vetor[id].id_precedencia=id_precedencia
                            vetor[id_precedencia].id_sucedencias.append(id)
                            if vetor[id_precedencia].delta>vetor[id].delta:
                                vetor[id_precedencia].delta=vetor[id].delta
                            encontrei=True
                        else:
                            id_precedencia+=1

                    if encontrei==False:
                        vetor[id].pronta_a_iniciar = 0
                        n_impossivel += 1

            elif "/000" in descricao_precedencia:
                vetor[id].pronta_a_iniciar = 0
                n_impossivel+=1

            elif "/ORT" or "PL CC" in descricao_precedencia:
                encontrei = False
                id_precedencia = 0
                while encontrei == False and id_precedencia < len(vetor):
                    if vetor[id].codigo_precedencia == vetor[id_precedencia].codigo_material:
                        vetor[id].id_precedencia = id_precedencia
                        vetor[id_precedencia].id_sucedencias.append(id)
                        encontrei = True
                    else:
                        id_precedencia += 1
                if encontrei==False:
                    n_impossivel += 1

    return n_impossivel

def calcular_ofs_prontas(vetor):

    lista=[]

    for index in range(len(vetor)):
        if vetor[index].pronta_a_iniciar==1 and vetor[index].id_slot_inicio_turno==-1:
            lista.append(index)

    lista=sort_delta(lista,vetor)

    return lista

def definir_turno_min(vetor_maquinas):

    global maquinas

    id_inicio_turno=-1
    minimo_global=999999999
    id=-1

    #print('numero de maquinas' + str(len(vetor_maquinas)))

    for id_maquina in range(len(vetor_maquinas)):
        if maquinas[vetor_maquinas[id_maquina]].nome=='CNMLAM03' and len(vetor_maquinas)==2:
            min_data_maquina=maquinas[vetor_maquinas[id_maquina]].min_alocada+48*60
        else:
            min_data_maquina = maquinas[vetor_maquinas[id_maquina]].min_alocada
        #print('data minima na maquina ' + str(maquinas[vetor_maquinas[id_maquina]].nome) + ' é ' + str(min_data) + ' com n slots ' + str(len(maquinas[vetor_maquinas[id_maquina]].id_slot_inicio_turno)))
        for index in range(len(maquinas[vetor_maquinas[id_maquina]].id_slot_inicio_turno)):
            inicio_slot=slots[maquinas[vetor_maquinas[id_maquina]].id_slot_inicio_turno[index]].inicio
            capacidade_turno=maquinas[vetor_maquinas[id_maquina]].vetor_capacidade[index]
            if (min_data_maquina>=inicio_slot and capacidade_turno>0 and min_data_maquina<minimo_global) or (min_data_maquina<=inicio_slot and capacidade_turno>0 and min_data_maquina<minimo_global):
                id_inicio_turno=index
                id=vetor_maquinas[id_maquina]
                minimo_global=min_data_maquina

    return minimo_global,id_inicio_turno,id

def data_min_outsider(current_of):

    new_min=0

    start_hour=datetime.datetime.now()

    if start_hour.hour<20 and start_hour.hour>6 and current_of.outsider==1:
        start_hour=start_hour.replace(hour=22,minute=0)
        new_min=(start_hour - datetime.now()).total_seconds() / 60.0

    return new_min

def calcular_data_fim_maquina(t_start,tempo_teorico, id_maquina):

    # Percorrer as slots e determinar o momento final (não considerar ocupação)
    maq = maquinas[id_maquina]

    # Calculo tempo a alocar= setup da máquina + tempo produtivo
    tempo_alocar = tempo_teorico

    n_slots = len(maq.vetor_slots)-1
    t_finish = t_start
    tempo_em_falta = tempo_alocar
    index = 0

    encontrei=False
    count=0

    while encontrei==False and count<n_slots:
        if slots[maquinas[id_maquina].id_slot_inicio_turno[index]].inicio>t_start:
            encontrei=True
            index=count
        count+=1

    # Percorrer as várias slots at++e determinar o momento final

    while index <= n_slots and tempo_em_falta > 0:
        # print('index ' + str(index))

        slot = slots[maq.vetor_slots[index]]

        s_slot = slot.inicio

        #print('inicio da slot a analisar: ' + str(s_slot))
        f_slot = slot.fim

        # Se for Slot Inicial
        if t_start >= s_slot and t_start <= f_slot:

            if f_slot - t_start >= tempo_em_falta:
                t_finish = t_start + tempo_em_falta
                tempo_em_falta = 0

                #capacidades.append(nova_linha)

            else:
                tempo_em_falta=tempo_em_falta - (f_slot - t_start)


        elif t_start <= s_slot:

            if f_slot - s_slot >= tempo_em_falta:  # Se o restante couber na slot
                t_finish = s_slot + tempo_em_falta
                tempo_em_falta = 0

            else:
                tempo_em_falta = tempo_em_falta - (f_slot - s_slot)

        # Incremento

        index += 1

    if t_finish > 0:
        return t_finish
    else:
        print("Erro ao calcular calculo_finish_from_start")
        return -1

def update_delta(id_of,id_grupo):

    grupos[id_of].data_min = grupos[id_grupo].data_fim

    grupos[id_of].pronta_a_iniciar=1

def update_capacidade(remanescente,turno,max_turno,id_maquina):

    global maquinas

    while remanescente > 0 and turno < max_turno:  # transformar em função

        if maquinas[id_maquina].vetor_capacidade[turno] != 0:

            print(maquinas[id_maquina].vetor_capacidade[turno])

            remanescente = maquinas[id_maquina].diminuir_capacidade(turno, remanescente)

            if maquinas[id_maquina].vetor_capacidade[turno] == 0:
                turno += 1
        else:
            turno+=1

    return remanescente

def gerar_output_final(method):

    global ofs
    global grupos

    por_planear = []
    planeado = []

    if method==1: #grupos

        for index in range(len(ofs)):

            ids=ofs[index].id_grupos

            for id in range(len(ids)):

                id_groupby = ofs[index].id_grupos[id]

                if grupos[id_groupby].id_slot_inicio_turno == -1:

                    row_to_plan = {'semana': ofs[index].data, 'of': ofs[index].cod_of,
                                   'descricao material': ofs[index].descricao_material,
                                   'descricao consumo': ofs[index].descricao_precedencia,'ct':ofs[index].ct}

                    por_planear.append(row_to_plan)

                else:

                    min=(ofs[index].quantidade_grupos[id]/ofs[index].quantidade)*ofs[index].t_producao
                    quantidade=ofs[index].quantidade_grupos[id]/ofs[index].quantidade*ofs[index].quantidade

                    duracao=datetime.timedelta(minutes=min)
                    duracao=str(duracao)

                    if grupos[id_groupby].id_precedencia!=-1:
                        precedencia=grupos[grupos[id_groupby].id_precedencia]
                        fim_precedencia=datetime.datetime.now() + datetime.timedelta(minutes=precedencia.data_fim)
                    else:
                        fim_precedencia=datetime.datetime.now()+datetime.timedelta(minutes=grupos[id_groupby].data_min)

                    new_row = {'semana':ofs[index].data,'Máquina': maquinas[grupos[id_groupby].id_alocada].nome,'OF': ofs[index].cod_of,
                               'Início': datetime.datetime.now() + datetime.timedelta(minutes=grupos[id_groupby].data_inicio),'Duração':duracao,'Quantidade': quantidade,
                               'Descrição Material': ofs[index].descricao_material,'consumo blocos':grupos[id_groupby].quantidade_precedencia,'grupo':id_groupby,'data fim precedencia':fim_precedencia}

                    planeado.append(new_row)
    else:

        for index in range(len(grupos)):

            id_grupo=grupos[index].id

            if id_grupo==110:
                print('debug')

            for codigo in range(len(grupos[index].id_of)):

                id_of=grupos[index].id_of[codigo]

                if ofs[id_of].cod_of==1600061549:
                    print('debug')

                if grupos[index].id_slot_inicio_turno == -1:

                    row_to_plan = {'semana': ofs[id_of].data, 'of': ofs[id_of].cod_of,
                                   'descricao material': ofs[id_of].descricao_material,
                                   'descricao consumo': ofs[id_of].descricao_precedencia, 'ct': ofs[id_of].ct}

                    por_planear.append(row_to_plan)

                else:

                    posicao_grupo=ofs[id_of].id_grupos.index(index)

                    min = (ofs[id_of].quantidade_grupos[posicao_grupo] / ofs[id_of].quantidade) * ofs[id_of].t_producao
                    quantidade = ofs[id_of].quantidade_grupos[posicao_grupo]

                    duracao = datetime.timedelta(minutes=min)
                    duracao = str(duracao)

                    if grupos[index].id_precedencia != -1:
                        precedencia = grupos[grupos[index].id_precedencia]
                        fim_precedencia = datetime.datetime.now() + datetime.timedelta(minutes=precedencia.data_fim)
                    else:
                        fim_precedencia = datetime.datetime.now() + datetime.timedelta(
                            minutes=grupos[index].data_min)

                    new_row = {'semana': ofs[id_of].data, 'Máquina': maquinas[grupos[index].id_alocada].nome,
                               'OF': ofs[id_of].cod_of,
                               'Início': datetime.datetime.now() + datetime.timedelta(
                                   minutes=grupos[index].data_inicio), 'Duração': duracao,
                               'Quantidade': quantidade,
                               'Descrição Material': ofs[id_of].descricao_material,
                               'consumo blocos': grupos[index].quantidade_precedencia, 'grupo': index,
                               'data fim precedencia': fim_precedencia}

                    planeado.append(new_row)



    df = pd.DataFrame(por_planear)
    df.to_csv('data/12. impossiveis.csv')

    df = pd.DataFrame(planeado)
    df.to_csv('data/13. output final.csv')

def definir_min_maquina(id_maquina,data_fim):

    global maquinas

    maquinas[id_maquina].min_alocada = data_fim

    print(maquinas[id_maquina].min_alocada)

def tornar_of_impossivel(id_of):

    global grupos

    grupos[id_of].id_slot_inicio_turno = 999999
    grupos[id_of].pronta_a_iniciar = 0

def atualizar_of_datas(id_of,data_inicio,data_fim):

    global grupos

    grupos[id_of].data_inicio=data_inicio
    grupos[id_of].data_fim=data_fim

def alocar_of(id_grupo,id_maquina,turno):

    global grupos

    grupos[id_grupo].id_alocada = id_maquina
    grupos[id_grupo].id_slot_inicio_turno = maquinas[id_maquina].id_slot_inicio_turno[turno]

def limpar_grupos():

    global grupos

    for index in range(len(grupos)):

        if grupos[index].ct=='CNMRETBL' and len(grupos[index].id_sucedencias)==0:

            grupos[index].pronta_a_iniciar=0

            grupos[index].id_slot_inicio=-1














