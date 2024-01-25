import re

def identifica_topico(line):
    number_preffix = ""
    words = line.split()
    first_word = words[0]
    for letter in first_word:
        if letter.isnumeric():
            number_preffix = number_preffix + letter
    if first_word[len(number_preffix):] == 'SERVIÇOS':
        return bool(1)
    return bool(0)

def processa_blocos(lista_blocos):
    conteudo_servico = ""
    servicos_list = []
    servicos_sublist = []
    categorias_servicos = []
    for bloco in lista_blocos:
        for line in bloco.splitlines():
            if identifica_topico(line):
                categorias_servicos.append(line)
            else:
                if line.split()[0].isnumeric():
                    if conteudo_servico != "":
                        servicos_sublist.append(conteudo_servico)
                    conteudo_servico = ""
                    conteudo_servico = conteudo_servico + line + " "
                elif line != "Serviço Aliquota Sigla":
                    conteudo_servico = conteudo_servico + line + " "
        if conteudo_servico != "":
            servicos_sublist.append(conteudo_servico)
            conteudo_servico = ""
        servicos_list.append(servicos_sublist.copy())
        servicos_sublist.clear()
    cria_sql_categoria_servico(categorias_servicos)
    cria_sql_servico(servicos_list)


def processa_servico(conteudo_servico):
    return True
    print(conteudo_servico)


def cria_sql_categoria_servico(categorias_servicos):
    sql_statement = "INSERT INTO categoria_servico (id, titulo_servico) VALUES\n"
    id_categoria = ""
    titulo_categoria = ""
    for categoria in categorias_servicos:
        for letter in categoria.split()[0]:
            if letter.isnumeric():
                id_categoria = id_categoria + letter
            else:
                break
        titulo_categoria = categoria[len(id_categoria):]
        sql_statement = sql_statement + f"('{id_categoria}', '{titulo_categoria}'), \n"
        id_categoria = ""
    print(sql_statement)


def cria_sql_servico(servicos_list):

    sql_statement = "INSERT INTO servico (id, descricao_servico, aliquota_servico, categoria_servico_id) VALUES\n"
    id_servico = 0
    descricao_servico = ""
    aliquota_servico = ""
    categoria_servico_id = 0
    aliquota_pattern = re.compile("[0-9],[0-9]{2}")
    for i in range(len(servicos_list)):
        categoria_servico_id = i + 1
        for servico in servicos_list[i]:
            for word in servico.split():
                if word.isnumeric():
                    id_servico = word
                elif aliquota_pattern.match(word):
                    aliquota_servico = word.replace(',', '.')
                else:
                    descricao_servico = descricao_servico + word + " "
            sql_statement = sql_statement + f"('{id_servico}', '{descricao_servico}', '{aliquota_servico}', '{categoria_servico_id}'), \n"
            descricao_servico = ""
            with open('finalsqlservicos.txt', 'w') as f:
                f.write(sql_statement)


