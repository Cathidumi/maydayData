import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def exibir_resultados_paginados(lista_original, titulo_busca, permitir_filtro_cidade=False):
    if not lista_original:
        print(f"Nenhum registro encontrado para {titulo_busca}.")
        input("Pressione Enter para voltar...")
        return

    lista_atual = lista_original
    pagina_tamanho = 10
    pagina_atual = 0
    filtro_ativo = None

    while True:
        clear_terminal()
        total = len(lista_atual)
        
        inicio = pagina_atual * pagina_tamanho
        fim = inicio + pagina_tamanho
        itens_pagina = lista_atual[inicio:fim]

        # Cabeçalho
        print(f"{' RESULTADOS DA BUSCA ':=^80}")
        print(f"Critério: {titulo_busca}")
        if filtro_ativo:
            print(f"   [Filtro Ativo: Cidade começa com '{filtro_ativo}']")
        
        print(f"Exibindo {inicio + 1}-{min(fim, total)} de {total} ocorrências")
        print("-" * 80)

        # Tabela
        print(f"|{'Código':^10}|{'Cidade / UF':^35}|{'Classificação':^30}|")
        print("-" * 80)

        for oc in itens_pagina:
            local = f"{oc.cidade.strip()}/{oc.uf}"
            classif = oc.classificacao.strip()[:28]
            print(f"|{oc.codigo:^10}| {local:<34}| {classif:<29}|")
        
        print("-" * 80)

        # --- MENU ---
        opcoes = []
        if fim < total: opcoes.append("[Enter] Próx")
        if pagina_atual > 0: opcoes.append("[A]nterior")
        
        if permitir_filtro_cidade and not filtro_ativo: 
            opcoes.append("[F]iltrar (Cidade)")
        elif filtro_ativo:
            opcoes.append("[L]impar Filtro")
            
        opcoes.append("[S]air")
        
        print("\nComandos: " + "  ".join(opcoes))
        comando = input(">> ").strip().lower()

        if comando == 's':
            break
        elif comando == '' and fim < total:
            pagina_atual += 1
        elif comando == 'a' and pagina_atual > 0:
            pagina_atual -= 1
            
        elif comando == 'f' and permitir_filtro_cidade and not filtro_ativo:
            termo = input("Filtrar cidade por (prefixo): ").strip().upper()
            if termo:
                nova = [x for x in lista_original if x.cidade.strip().startswith(termo)]
                if nova:
                    lista_atual = nova
                    filtro_ativo = termo
                    pagina_atual = 0
                else:
                    input("Nenhum resultado no filtro. Enter para voltar...")
                    
        elif comando == 'l' and filtro_ativo:
            lista_atual = lista_original
            filtro_ativo = None
            pagina_atual = 0

# BUSCA NA ÁRVORE B+
def busca_na_arvore(db, codigo=87125):
    try:
        ocorrencia = db.buscar_ocorrencia_por_id(codigo)
        if ocorrencia:
            aeronaves = db.ler_aeronaves(ocorrencia)
            tipos = db.ler_tipos(ocorrencia)
            recomendacoes = db.ler_recomendacoes(ocorrencia)

            if len(recomendacoes) > 0:
                rec_numero = recomendacoes[0].numero.strip()
                rec_status = recomendacoes[0].status.strip()
                rec_conteudo = recomendacoes[0].conteudo.strip()
                if len(rec_conteudo) > 57:
                    rec_conteudo3 = rec_conteudo[124:190]
                    rec_conteudo2 = rec_conteudo[57:124]
                    rec_conteudo = rec_conteudo[:57]
                else:
                    rec_conteudo2 = ""
                    rec_conteudo3 = ""

            else:
                rec_numero = "Não há recomendações"
                rec_status = "Não há recomendações"
                rec_conteudo = "Não há recomendações"
                rec_conteudo2 = ""
                rec_conteudo3 = ""

            local = f"{ocorrencia.cidade.strip()}/{ocorrencia.uf}"
            aeronave_destino = aeronaves[0].destino
            aeronave_destino = aeronave_destino[:23]
            aeronave_origem = aeronaves[0].origem
            aeronave_origem = aeronave_origem[:24]

            #print(f"Ocorrência encontrada: {ocorrencia}")
            print('-' * 141)
            print(f'|{'Ocorrência':^34}|{'Aeronave':^34}|{ 'Recomendações':^69}|')
            print('-' * 141)
            print(f"| Código: {ocorrencia.codigo:<24} | Modelo: {aeronaves[0].modelo:<24} | Número: {rec_numero:<60}|")
            print(f"| Local: {local:<25} | Origem: {aeronave_origem:<24} | Status: {rec_status:<60}|")
            print(f"| Classificação: {ocorrencia.classificacao.strip():<17} | Destino: {aeronave_destino:<23} | Conteúdo: {rec_conteudo:<58}|")
            print(f"| Aeronaves Envolvidas: {ocorrencia.total_aeros:<10} | Fatalidades: {aeronaves[0].fatalidades:<19} | {rec_conteudo2:<67} |") 
            print(f"| Investigação: {ocorrencia.status.strip():<18} | {'|':>34} {rec_conteudo3:<67} |")
            print('-' * 141)
            print(f'|{'Tipo':^69}|')
            print('-' * 71)
            print(f'| Tipo: {tipos[0].tipo:<61} |') # | Número: {recomendacoes[0].numero:<53}|')
            print(f'| Categoria: {tipos[0].categoria:<56} |') #| Status: {recomendacoes[0].status:<50}|')
            print(f'| Taxonomia: {tipos[0].taxonomia:<56} |') #| Conteúdo: {recomendacoes[0].conteudo:<50}|')
            print('-' * 71)

        else:
            print(f"Ocorrência com código {codigo} não encontrada.")
    except Exception as e:
        print(f"Erro ao buscar ocorrência: {e}")

def busca_na_trie_modelo(db, modelo_parcial="CESSNA"):
    try:
        ocorrencias = db.buscar_por_modelo(modelo_parcial)
        if ocorrencias:
            print(f"Ocorrências encontradas para modelo começando com '{modelo_parcial}':")
            for oc in ocorrencias:
                print(f"  Código: {oc.codigo}, Local: {oc.cidade.strip()}/{oc.uf}, Classificação: {oc.classificacao.strip()}")
        else:
            print(f"Nenhuma ocorrência encontrada para modelo começando com '{modelo_parcial}'.")
    except Exception as e:
        print(f"Erro ao buscar por modelo na Trie: {e}")

def busca_na_trie_modelo_paginada(db):
    clear_terminal()
    print("--- Busca por Modelo ---")
    termo = input('Digite o modelo ou prefixo: ').strip()
    if not termo: return
    
    print("Buscando...")
    try:
        resultados = db.buscar_por_modelo(termo)
        exibir_resultados_paginados(resultados, f"Modelo '{termo}'", permitir_filtro_cidade=True)
    except Exception as e:
        print(f"Erro: {e}")
        input()

def busca_trie_cidade(db, cidade_parcial="SAO PAULO"):
    try:
        ocorrencias = db.buscar_por_cidade(cidade_parcial)
        if ocorrencias:
            print(f"Ocorrências encontradas para cidade começando com '{cidade_parcial}':")
            for oc in ocorrencias:
                print(f"  Código: {oc.codigo}, Local: {oc.cidade.strip()}/{oc.uf}, Classificação: {oc.classificacao.strip()}")
        else:
            print(f"Nenhuma ocorrência encontrada para cidade começando com '{cidade_parcial}'.")
    except Exception as e:
        print(f"Erro ao buscar por cidade na Trie: {e}")

def busca_trie_cidade_paginada(db):
    clear_terminal()
    print("--- Busca por Cidade ---")
    termo = input('Digite a cidade ou prefixo: ').strip()
    if not termo: return

    print("Buscando...")
    try:
        resultados = db.buscar_por_cidade(termo)
        exibir_resultados_paginados(resultados, f"Cidade '{termo}'")
    except Exception as e:
        print(f"Erro: {e}")
        input()

def busca_trie_categoria(db, categoria_parcial="ACIDENTE"):
    try:
        ocorrencias = db.buscar_por_categoria_tipo(categoria_parcial)
        if ocorrencias:
            print(f"Ocorrências encontradas para categoria começando com '{categoria_parcial}':")
            for oc in ocorrencias:
                print(f"  Código: {oc.codigo}, Local: {oc.cidade.strip()}/{oc.uf}, Classificação: {oc.classificacao.strip()}")
        else:
            print(f"Nenhuma ocorrência encontrada para categoria começando com '{categoria_parcial}'.")
    except Exception as e:
        print(f"Erro ao buscar por categoria na Trie: {e}")

def busca_bst_uf(db, uf="SP"):
    try:
        ocorrencias = db.buscar_por_uf(uf)
        if ocorrencias:
            print(f"Ocorrências encontradas para UF '{uf}':")
            for oc in ocorrencias:
                print(f"  Código: {oc.codigo}, Local: {oc.cidade.strip()}/{oc.uf}, Classificação: {oc.classificacao.strip()}")
        else:
            print(f"Nenhuma ocorrência encontrada para UF '{uf}'.")
    except Exception as e:
        print(f"Erro ao buscar por UF na BST: {e}")

def busca_bst_status_investigacao(db, status="FINALIZADA"):
    try:
        ocorrencias = db.buscar_por_status_investigacao(status)
        if ocorrencias:
            print(f"Ocorrências encontradas para status de investigação '{status}':")
            for oc in ocorrencias:
                print(f"  Código: {oc.codigo}, Local: {oc.cidade.strip()}/{oc.uf}, Classificação: {oc.classificacao.strip()}")
        else:
            print(f"Nenhuma ocorrência encontrada para status de investigação '{status}'.")
    except Exception as e:
        print(f"Erro ao buscar por status de investigação na BST: {e}")

def busca_bst_fatalidades(db, qtd):
    try:
        ocorrencias = db.buscar_por_fatalidades(qtd)
        if ocorrencias:
            print(f"Ocorrências encontradas com {qtd} fatalidades:")
            for oc in ocorrencias:
                print(f"  Código: {oc.codigo} | Local: {oc.cidade.strip()}/{oc.uf} | Classificação: {oc.classificacao.strip()}")
        else:
            print(f"Nenhuma ocorrência encontrada com exatos {qtd} fatalidades.")
    except Exception as e:
        print(f"Erro na busca por fatalidades: {e}")

def busca_trie_categoria_paginada(db):
    clear_terminal()
    print("--- Busca por Categoria da Ocorrência ---")
    termo = input('Digite a categoria ou prefixo: ').strip()
    if not termo: return

    print("Buscando...")
    try:
        resultados = db.buscar_por_categoria_tipo(termo)
        exibir_resultados_paginados(resultados, f"Categoria '{termo}'")
    except Exception as e:
        print(f"Erro: {e}")
        input()

def busca_bst_uf_paginada(db):
    clear_terminal()
    print("--- Busca por UF (Estado) ---")
    uf = input('Digite a Sigla da UF (ex: SP, RJ, RS): ').strip().upper()
    
    if len(uf) != 2:
        print("Erro: A UF deve ter exatamente 2 letras.")
        input("Enter para voltar...")
        return

    print("Buscando...")
    try:
        resultados = db.buscar_por_uf(uf)
        exibir_resultados_paginados(resultados, f"UF '{uf}'")
    except Exception as e:
        print(f"Erro: {e}")
        input()

def busca_bst_status_paginada(db):
    clear_terminal()
    print("--- Busca por Status da Investigação ---")
    print("Exemplos: FINALIZADA, ATIVA")
    status = input('Digite o Status: ').strip().upper()
    if not status: return

    print("Buscando...")
    try:
        resultados = db.buscar_por_status_investigacao(status)
        exibir_resultados_paginados(resultados, f"Status '{status}'")
    except Exception as e:
        print(f"Erro: {e}")
        input()

def busca_bst_fatalidades_paginada(db):
    clear_terminal()
    print("--- Busca por Quantidade de Fatalidades ---")
    entrada = input('Digite o número exato de fatalidades: ').strip()
    
    if not entrada.isdigit():
        print("Erro: Digite apenas números inteiros.")
        input("Enter para voltar...")
        return
        
    qtd = int(entrada)
    print("Buscando...")
    try:
        resultados = db.buscar_por_fatalidades(qtd)
        exibir_resultados_paginados(resultados, f"{qtd} Fatalidades")
    except Exception as e:
        print(f"Erro: {e}")
        input()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')