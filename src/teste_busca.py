import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Database

# BUSCA NA ÁRVORE B+
def busca_na_arvore(codigo_teste=87125):
    try:
        db = Database(
            path_oc="data/bin/ocorrencias.dat",
            path_ae="data/bin/aeronaves.dat",
            path_tipo="data/bin/tipos.dat",
            path_rec="data/bin/recomendacoes.dat"
        )
        
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

if __name__ == "__main__":
    busca_na_arvore()