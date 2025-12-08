import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# BUSCA NA ÁRVORE B+
def busca_na_arvore(db, codigo_teste=87125):
    try:
        ocorrencia = db.buscar_ocorrencia_por_id(codigo_teste)
        if ocorrencia:
            print(f"Ocorrência encontrada: {ocorrencia}")
            print(f"  Local: {ocorrencia.cidade.strip()}/{ocorrencia.uf}")
            print(f"  Classificação: {ocorrencia.classificacao.strip()}")
            print(f"  Total Aeronaves Envolvidas: {ocorrencia.total_aeros}")
            print(f"  Status da Investigação: {ocorrencia.status.strip()}")
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
