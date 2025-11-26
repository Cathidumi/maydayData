# ARQUIVO CRIADO APENAS PARA FINS DE TESTE DA LEITURA DOS DADOS BINÁRIOS

from database import Database
import os

def testar_simples():
    path_oc = "data/bin/ocorrencias.dat"
    path_ae = "data/bin/aeronaves.dat"
    path_tp = "data/bin/tipos.dat"
    path_rc = "data/bin/recomendacoes.dat"

    if not os.path.exists(path_oc):
        print("Arquivos .dat não encontrados")
        return

    db = Database(path_oc, path_ae, path_tp, path_rc)

    # Lê a primeira ocorrência
    oc = db.ler_ocorrencia(0)
    
    if not oc:
        print("Nenhuma ocorrência encontrada.")
        return

    print(f"ID: {oc.codigo} | Local: {oc.cidade.strip()}/{oc.uf}")
    print(f"Classificação: {oc.classificacao.strip()}")

    aeronaves = db.ler_aeronaves(oc)
    print(f"Aeronaves ({len(aeronaves)}):")
    for a in aeronaves:
        print(f" - {a.modelo.strip()} (Fatais: {a.fatalidades})")

    tipos = db.ler_tipos(oc)
    print(f"Tipos ({len(tipos)}):")
    for t in tipos:
        print(f" - {t.tipo.strip()} ({t.taxonomia.strip()})")

    recs = db.ler_recomendacoes(oc)
    print(f"Recomendações ({len(recs)}):")
    for r in recs:
        print(f" - {r.numero.strip()}: {r.status.strip()}")

if __name__ == "__main__":
    testar_simples()