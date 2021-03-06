
from functions import *
from import_data import *
global grupos


atualizar_ct_outsiders()
id_ofs=get_ids(ofs)

verificar_em_producao()

sort_delta(id_ofs,ofs)

for index in range(len(ofs)):
    if ofs[index].estado==1:
        print(ofs[index].cod_of)

grupos=criar_total_grupos(id_ofs)

n_impossivel=verificar_precedencias(grupos)
id_grupos=get_ids(grupos)
sort_delta(id_grupos,grupos)

ordens_alocadas=0



limpar_grupos()

limpar_sem_blocos()

atualizar_quantidade_retificadora()

alterar_data_min_ret()

sort_delta(id_grupos,grupos)

maquinas_descricoes=[]

ofs_lidas=[]

for index in range(len(ofs)):
    new_of={'of':ofs[index].cod_of,'descricao':ofs[index].descricao_material,'quantidade':ofs[index].quantidade,'quantidade precedencia':ofs[index].quantidade_precedencia,'centro de trabalho': ofs[index].ct, 'n.º maquinas': len(ofs[index].vetor_maquinas)}
    ofs_lidas.append(new_of)

df = pd.DataFrame(ofs_lidas)
df.to_csv('data/16. ofs lidas.csv')

while ordens_alocadas+n_impossivel<len(id_grupos):

    id_prontos = calcular_ofs_prontas(grupos)

    if len(id_prontos) > 0:

        print('of: ' + str(grupos[id_prontos[0]].descricao_material))

        current_of=grupos[id_prontos[0]]
        id_grupo=id_prontos[0]

        if current_of.ct=="CNMLAMLXOUT":
            print('debug')

        min_data_maquina, id_inicio_turno, id_maquina = definir_turno_min(current_of.vetor_maquinas)

        if current_of.descricao in maquinas_descricoes:

            posicao=maquinas_descricoes.index(current_of.descricao)

            if (id_maquina in maquinas_descricoes[posicao])==False and len(maquinas_descricoes[posicao])==2:

                min_data_maquina, id_inicio_turno, id_maquina = definir_turno_min(maquinas_descricoes[posicao])

            elif len(maquinas_descricoes[posicao])<2:

                maquinas_descricoes[posicao].append(id_maquina)

        else:

            maquinas_descricoes.append(current_of.descricao)
            pos=maquinas_descricoes.index(current_of.descricao)
            maquinas_descricoes[pos]=id_maquina

        min_data_global=max(min_data_maquina,current_of.data_min)

        if min_data_global-min_data_maquina>=60:

            print('subocupação de ' + str(min_data_global-min_data_maquina))
            print('data inicio é ' + str(min_data_global))

            data_in_prioridade = min_data_global
            ct=current_of.ct
            data_final=0

            count=1

            while data_final < data_in_prioridade and count < len(id_prontos):

                id_pending=id_prontos[count]

                if grupos[id_prontos[count]].ct==ct:

                    of_prencher=grupos[id_prontos[count]]

                    id_preencher = id_prontos[count]

                    min_data_maquina_preencher, id_inicio_turno_preencher, id_maquina_preencher = definir_turno_min(of_prencher.vetor_maquinas)

                    min_data_global_preencher = max(min_data_maquina_preencher, of_prencher.data_min)

                    turno_preencher=id_inicio_turno_preencher

                    if math.ceil(min_data_global_preencher) < math.ceil(data_in_prioridade):

                        if turno_preencher == -1:

                            n_impossivel += 1

                            tornar_of_impossivel(id_preencher)

                        else:

                            max_turno = len(maquinas[id_maquina_preencher].id_slot_inicio_turno)
                            remanescente_preencher = of_prencher.t_producao / maquinas[id_maquina_preencher].oee


                            data_inicio = min_data_global_preencher
                            data_fim = calcular_data_fim_maquina(data_inicio, of_prencher.t_producao,
                                                                    id_maquina_preencher)



                            if data_fim == -1:
                                n_impossivel += 1
                                tornar_of_impossivel(id_preencher)

                            else:

                                atualizar_of_datas(id_preencher, data_inicio, data_fim)

                                print('current of ' + str(of_prencher.cod_of) + ' começa em: ' + str(of_prencher.data_inicio) + ' acaba em: ' + str(of_prencher.data_fim) + ' no centro de trabalho ' + str(of_prencher.ct))

                                ordens_alocadas+=1
                                alocar_of(id_preencher,id_maquina_preencher,turno_preencher)
                                definir_min_maquina(id_maquina_preencher,of_prencher.data_fim)
                                update_capacidade(remanescente_preencher, turno_preencher, max_turno, id_maquina_preencher)
                                data_final=of_prencher.data_inicio

                                for id_of in range(len(of_prencher.id_sucedencias)):
                                    update_delta(of_prencher.id_sucedencias[id_of], id_preencher)


                count += 1

        turno = id_inicio_turno

        if turno == -1:

            n_impossivel += 1
            tornar_of_impossivel(id_grupo)

        else:

            data_inicio=min_data_global

            data_fim=calcular_data_fim_maquina(data_inicio,current_of.t_producao / maquinas[id_maquina].oee, id_maquina)

            atualizar_of_datas(id_grupo,data_inicio,data_fim)

            print('current of ' + str(current_of.cod_of) + ' começa em: ' + str(
                current_of.data_inicio) + ' acaba em: ' + str(current_of.data_fim) + ' no centro de trabalho ' + str(current_of.ct))

            if current_of.data_fim==-1:

                n_impossivel += 1
                tornar_of_impossivel(id_grupo)


            else:

                ordens_alocadas += 1
                alocar_of(id_grupo,id_maquina,turno)

                definir_min_maquina(id_maquina, current_of.data_fim)
                max_turno = len(maquinas[id_maquina].id_slot_inicio_turno)
                remanescente = current_of.t_producao / maquinas[id_maquina].oee
                update_capacidade(remanescente, turno, max_turno,id_maquina)

            for id_of in range(len(current_of.id_sucedencias)):

                update_delta(current_of.id_sucedencias[id_of], id_grupo)

            sort_delta(id_grupos,grupos)

    else:

        break

gerar_output_final(0)













