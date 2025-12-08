import os
import csv
from model import Ocorrencia, Aeronave, OcorrenciaTipo, Recomendacao
from bplustree import BPlusTree # importa a implementação da Árvore B+
from indexes import Trie # importa a implementação da Trie
from indexes import IndiceInvertidoBST

def importar_tudo():
    # Pastas e Caminhos
    os.makedirs("data/bin", exist_ok=True)
    f_oc = "data/bin/ocorrencias.dat"
    f_ae = "data/bin/aeronaves.dat"
    f_tp = "data/bin/tipos.dat"
    f_rc = "data/bin/recomendacoes.dat"
    
    # Inicializa a Árvore B+
    index_tree = BPlusTree(order=5)
    # Inicializa a Trie para busca por modelo (Índice Secundário)
    index_modelo_trie = Trie("data/bin/index_modelo.dat")
    #Index Secundário (Trie) para cidades
    index_cidade = Trie("data/bin/index_cidade.dat")
    #Index Secundário (Trie) para ocorrencia_categoria_tipo
    index_categoria = Trie("data/bin/index_categoria.dat")
    # Inicializa BST para índice invertido para UF
    index_uf = IndiceInvertidoBST("data/bin/index_uf.dat", key_size=2)

    # Abre todos em modo w+b (limpa e abre binario)
    arq_oc = open(f_oc, "w+b")
    arq_ae = open(f_ae, "w+b")
    arq_tp = open(f_tp, "w+b")
    arq_rc = open(f_rc, "w+b")
    
    # Mantemos este dicionário APENAS para resolver as chaves estrangeiras 
    # (Aeronaves/Tipos) rapidamente durante a importação, sem precisar fazer I/O na árvore.
    indice_id_offset_temp = {} 

    # --- PASSO 1: OCORRÊNCIAS ---
    print("--- 1. Importando Ocorrências ---")
    try:
        with open("data/raw/ocorrencia.csv", "r", encoding='latin-1') as f:
            leitor = csv.DictReader(f, delimiter=';')
            for row in leitor:
                try:
                    cod = int(row['codigo_ocorrencia'])
                    cidade = row['ocorrencia_cidade'] # <--- PEGANDO A CIDADE
                    
                    oc = Ocorrencia(
                        codigo=cod,
                        uf=row['ocorrencia_uf'],
                        cidade=row['ocorrencia_cidade'],
                        classificacao=row['ocorrencia_classificacao'],
                        status=row['investigacao_status'],
                        total_aeros=row['total_aeronaves_envolvidas']
                    )
                    
                    offset = arq_oc.tell()
                    arq_oc.write(oc.to_bytes())
                    
                    # Atualiza índice em memória (temp) e Árvore B+
                    indice_id_offset_temp[cod] = offset
                    index_tree.insert(cod, offset) # <--- INSERIR NA ÁRVORE
                    # Inserir na Trie de cidades (Índice Secundário)
                    index_cidade.insert(cidade, cod)
                    # Inserir na BST de UF (Índice Invertido)
                    index_uf.adicionar(row['ocorrencia_uf'], cod)
                    
                except ValueError: continue
    except FileNotFoundError: print("Arquivo ocorrencia.csv não encontrado.")

    # --- PASSO 2: AERONAVES ---
    print("--- 2. Importando Aeronaves ---")
    try:
        with open("data/raw/aeronave.csv", "r", encoding='latin-1') as f:
            leitor = csv.DictReader(f, delimiter=';')
            for row in leitor:
                try:
                    # CENIPA usa codigo_ocorrencia2 na tabela aeronave
                    cod_pai = int(row.get('codigo_ocorrencia2', row.get('codigo_ocorrencia')))
                    
                    if cod_pai in indice_id_offset_temp:
                        off_pai = indice_id_offset_temp[cod_pai]
                        modelo_aeronave = row['aeronave_modelo'] # <--- PEGANDO O MODELO
                        
                        # Ler Pai
                        arq_oc.seek(off_pai)
                        pai = Ocorrencia.from_bytes(arq_oc.read(Ocorrencia.TAMANHO))
                        
                        # Criar Filho (aponta para onde o pai apontava)
                        filho = Aeronave(
                            modelo=row['aeronave_modelo'],
                            origem=row['aeronave_voo_origem'],
                            destino=row['aeronave_voo_destino'],
                            fatalidades=row['aeronave_fatalidades_total'],
                            prox_aeronave=pai.pont_aeronave
                        )
                        
                        # Gravar Filho
                        off_filho = arq_ae.tell()
                        arq_ae.write(filho.to_bytes())
                        
                        # Atualizar Pai
                        pai.pont_aeronave = off_filho
                        arq_oc.seek(off_pai)
                        arq_oc.write(pai.to_bytes())

                        # Inserir no Índice Secundário (Trie) # <--- AQUI!
                        # A chave é o modelo, o valor é o código da ocorrência.
                        index_modelo_trie.insert(modelo_aeronave, cod_pai)
                        
                        # Resetar cursor do filho
                        arq_ae.seek(0, os.SEEK_END)
                except ValueError: continue
    except FileNotFoundError: print("aeronave.csv falta.")

    # --- PASSO 3: TIPOS ---
    print("--- 3. Importando Tipos ---")
    try:
        with open("data/raw/ocorrencia_tipo.csv", "r", encoding='latin-1') as f:
            leitor = csv.DictReader(f, delimiter=';')
            for row in leitor:
                try:
                    # CENIPA usa codigo_ocorrencia1
                    cod_pai = int(row.get('codigo_ocorrencia1', row.get('codigo_ocorrencia')))
                    
                    if cod_pai in indice_id_offset_temp:
                        off_pai = indice_id_offset_temp[cod_pai]
                        categoria_tipo = row['ocorrencia_tipo_categoria'] # <--- PEGANDO A CATEGORIA DA OCORRÊNCIA
                        
                        arq_oc.seek(off_pai)
                        pai = Ocorrencia.from_bytes(arq_oc.read(Ocorrencia.TAMANHO))
                        
                        filho = OcorrenciaTipo(
                            tipo=row['ocorrencia_tipo'],
                            categoria=row['ocorrencia_tipo_categoria'],
                            taxonomia=row['taxonomia_tipo_icao'],
                            prox_tipo=pai.pont_tipo
                        )
                        
                        off_filho = arq_tp.tell()
                        arq_tp.write(filho.to_bytes())
                        
                        pai.pont_tipo = off_filho
                        arq_oc.seek(off_pai)
                        arq_oc.write(pai.to_bytes())

                        # Inserir no Índice Secundário (Trie)
                        # A chave é o modelo, o valor é o código da ocorrência.
                        index_categoria.insert(categoria_tipo, cod_pai)
                        
                        arq_tp.seek(0, os.SEEK_END)
                except ValueError: continue
    except FileNotFoundError: print("ocorrencia_tipo.csv falta.")

    # --- PASSO 4: RECOMENDAÇÕES ---
    print("--- 4. Importando Recomendações ---")
    try:
        with open("data/raw/recomendacao.csv", "r", encoding='latin-1') as f:
            leitor = csv.DictReader(f, delimiter=';')
            for row in leitor:
                try:
                    # CENIPA usa codigo_ocorrencia4
                    cod_pai = int(row.get('codigo_ocorrencia4', row.get('codigo_ocorrencia')))
                    
                    if cod_pai in indice_id_offset_temp:
                        off_pai = indice_id_offset_temp[cod_pai]
                        
                        arq_oc.seek(off_pai)
                        pai = Ocorrencia.from_bytes(arq_oc.read(Ocorrencia.TAMANHO))
                        
                        filho = Recomendacao(
                            numero=row['recomendacao_numero'],
                            status=row['recomendacao_status'],
                            conteudo=row['recomendacao_conteudo'],
                            prox_rec=pai.pont_recomendacao
                        )
                        
                        off_filho = arq_rc.tell()
                        arq_rc.write(filho.to_bytes())
                        
                        pai.pont_recomendacao = off_filho
                        arq_oc.seek(off_pai)
                        arq_oc.write(pai.to_bytes())
                        
                        arq_rc.seek(0, os.SEEK_END)
                except ValueError: continue
    except FileNotFoundError: print("recomendacao.csv falta (opcional).")

    # Salvar a Árvore B+ no final
    index_tree.save() # <--- SALVAR NO DISCO
    
    # Salvar a Trie no final
    index_modelo_trie.save()
    index_cidade.save() # <--- SALVAR TRIE DE CIDADES
    index_categoria.save() # <--- SALVAR TRIE DE CATEGORIA
    
    index_uf.save()  # Salvar BST de UF

    # Fechar tudo
    arq_oc.close()
    arq_ae.close()
    arq_tp.close()
    arq_rc.close()
    print("Importação Completa! Arquivos Binários, Índice B+ Gerados e Índices Trie Gerados.")

if __name__ == "__main__":
    importar_tudo()
