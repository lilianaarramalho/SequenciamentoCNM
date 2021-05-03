
from functions import *
from import_data import *
global grupos

id_ofs=get_ids(ofs)
sort_delta(id_ofs,ofs)
grupos=criar_total_grupos(id_ofs)
id_grupos=get_ids(grupos)
sort_delta(id_grupos,grupos)

n_impossivel=verificar_precedencias(grupos)
ordens_alocadas=0

soma=0
for index in range(len(grupos)):
    if grupos[index].outsider==1:
        soma+=1


while ordens_alocadas+n_impossivel<len(id_grupos):

    id_prontos = calcular_ofs_prontas(grupos)

    if len(id_prontos) > 0:

        print('of: ' + str(grupos[id_prontos[0]].descricao_material))

        current_of=grupos[id_prontos[0]]
        id_grupo=id_prontos[0]

        min_data_maquina, id_inicio_turno, id_maquina = definir_turno_min(current_of.vetor_maquinas)

        min_data_outsider=data_min_outsider(current_of)

        min_data_global=max(min_data_maquina,current_of.data_min,min_data_outsider)

        if min_data_global-min_data_maquina>=60:

            print('subocupação de ' + str(min_data_global-min_data_maquina))
            print('data inicio é ' + str(min_data_global))

            data_in_prioridade = min_data_global
            ct=current_of.ct
            data_final=0

            count=1

            while data_final < data_in_prioridade and count < len(id_prontos):

                if grupos[id_prontos[count]].ct==ct:

                    of_prencher=grupos[id_prontos[count]]

                    id_preencher = id_prontos[count]

                    min_data_maquina_preencher, id_inicio_turno_preencher, id_maquina_preencher = definir_turno_min(of_prencher.vetor_maquinas)

                    min_data_outsider_preencher = data_min_outsider(of_prencher)

                    min_data_global_preencher = max(min_data_maquina, of_prencher.data_min, min_data_outsider)

                    turno_preencher=id_inicio_turno_preencher

                    if min_data_global_preencher < data_in_prioridade:

                        if turno_preencher == -1:

                            n_impossivel += 1

                            of_prencher.id_slot_inicio_turno = 999999
                            of_prencher.pronta_a_iniciar = 0

                        else:

                            max_turno = len(maquinas[id_maquina_preencher].id_slot_inicio_turno)
                            remanescente_preencher = of_prencher.t_producao / maquinas[id_maquina_preencher].oee
                            of_prencher.data_inicio = min_data_global_preencher
                            of_prencher.data_fim = calcular_data_fim_maquina(of_prencher.data_inicio, of_prencher.t_producao,
                                                                    id_maquina_preencher)

                            if of_prencher.data_fim == -1:
                                n_impossivel += 1
                                of_prencher.id_slot_inicio_turno = 999999
                                of_prencher.pronta_a_iniciar = 0

                            else:

                                ordens_alocadas+=1
                                of_prencher.id_alocada = id_maquina_preencher
                                of_prencher.id_slot_inicio_turno = maquinas[id_maquina_preencher].id_slot_inicio_turno[turno]
                                maquinas[id_maquina_preencher].min_alocada = of_prencher.data_fim
                                update_capacidade(remanescente_preencher, turno_preencher, max_turno, id_maquina_preencher)
                                data_final=of_prencher.data_inicio

                count += 1

        turno = id_inicio_turno

        if turno == -1:

            n_impossivel += 1
            current_of.id_slot_inicio_turno = 999999
            current_of.pronta_a_iniciar = 0

        else:


            current_of.data_inicio=min_data_global
            current_of.data_fim = calcular_data_fim_maquina(current_of.data_inicio,
                                                    current_of.t_producao / maquinas[id_maquina].oee, id_maquina)
            if current_of.data_fim==-1:
                n_impossivel += 1
                current_of.id_slot_inicio_turno = 999999
                current_of.pronta_a_iniciar = 0

            else:

                ordens_alocadas += 1
                current_of.id_alocada = id_maquina
                current_of.id_slot_inicio_turno = maquinas[id_maquina].id_slot_inicio_turno[turno]
                maquinas[id_maquina].min_alocada = current_of.data_fim
                max_turno = len(maquinas[id_maquina].id_slot_inicio_turno)
                remanescente = current_of.t_producao / maquinas[id_maquina].oee
                update_capacidade(remanescente, turno, max_turno,id_maquina)

            for id_of in range(len(current_of.id_sucedencias)):
                update_delta(current_of.id_sucedencias[id_of], id_grupo)

            sort_delta(id_grupos,grupos)

    else:

        break

gerar_output_final(1)













