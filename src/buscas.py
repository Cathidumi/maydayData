import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# BUSCA NA ÁRVORE B+
def busca_na_arvore(db, codigo_teste=87125):
    try:
        ocorrencia = db.buscar_ocorrencia_por_id(codigo_teste)
        if ocorrencia:
            aeronave = db.ler_aeronaves(ocorrencia)
            tipos = db.ler_tipos(ocorrencia)
            recomendacoes = db.ler_recomendacoes(ocorrencia)
            #print(f"Ocorrência encontrada: {ocorrencia}")
            print('-' * 141)
            print(f'|{'Ocorrência':^34}|{'Aeronaves':^34}|{ 'Tipos':^34}|{ 'Recomendações':^34}|')
            print('-' * 141)
            print(f"| Código: {ocorrencia.codigo:<24} |")
            print(f"| Local: {ocorrencia.cidade.strip()}/{ocorrencia.uf} |")
            print(f"| Classificação: {ocorrencia.classificacao.strip():<17} |")
            print(f"| Aeronaves Envolvidas: {ocorrencia.total_aeros:<10} |")
            print(f"| Investigação: {ocorrencia.status.strip():<18} |")
            print('-' * 141)

        else:
            print(f"Ocorrência com código {codigo_teste} não encontrada.")
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
    print("--- Busca por Modelo de Aeronave ---")
    print("Digite o modelo ou prefixo")
    modelo_input = input('>> ').strip()
    
    if not modelo_input:
        return

    print(f"\nBuscando registros para '{modelo_input}' no índice...")
    
    try:
        # 1. Busca Primária (Índice Trie no Disco)
        resultados_totais = db.buscar_por_modelo(modelo_input)
    except Exception as e:
        print(f"Erro na busca: {e}")
        return
    
    if not resultados_totais:
        print("Nenhum registro encontrado.")
        input("Pressione Enter para voltar...")
        return

    # 2. Loop de Navegação (Paginação e Filtros)
    lista_atual = resultados_totais # Começa exibindo tudo
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
        print(f"Modelo Buscado: {modelo_input.upper()}")
        if filtro_ativo:
            print(f"Filtro Secundário (Cidade): {filtro_ativo}")
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

        # Opções
        opcoes = []
        if fim < total: opcoes.append("[Enter] Próx. Pág")
        if pagina_atual > 0: opcoes.append("[A]nterior")
        
        if not filtro_ativo:
            opcoes.append("[F]iltrar por Cidade")
        else:
            opcoes.append("[L]impar Filtro")
            
        opcoes.append("[S]air")
        
        print("\nComandos: " + "  ".join(opcoes))
        comando = input(">> ").strip().lower()

        # Lógica de Controle
        if comando == 's':
            break
        
        elif comando == '' and fim < total:
            pagina_atual += 1
            
        elif comando == 'a' and pagina_atual > 0:
            pagina_atual -= 1
            
        elif comando == 'f' and not filtro_ativo:
            print("\nDigite o nome (ou parte) da cidade para filtrar nesta lista:")
            cidade_filtro = input("Filtro Cidade: ").strip().upper()
            
            if cidade_filtro:
                nova_lista = [
                    oc for oc in resultados_totais 
                    if oc.cidade.strip().startswith(cidade_filtro)
                ]
                
                if not nova_lista:
                    print(f"Nenhum resultado encontrado na cidade '{cidade_filtro}'.")
                    input("Enter para continuar...")
                else:
                    lista_atual = nova_lista
                    filtro_ativo = cidade_filtro
                    pagina_atual = 0
        elif comando == 'l' and filtro_ativo:
            lista_atual = resultados_totais
            filtro_ativo = None
            pagina_atual = 0

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

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')