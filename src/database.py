import os
from model import Ocorrencia, Aeronave, OcorrenciaTipo, Recomendacao
from bplustree import BPlusTree # Importa a classe BPlusTree como índice primário
from indexes import Trie   # Importa a Trie como índice secundário para busca por modelo de aeronave
from indexes import IndiceInvertidoBST  # Importa a BST para índice invertido

class Database:
    def __init__(self, path_oc, path_ae, path_tipo, path_rec):
        self.file_oc = path_oc
        self.file_ae = path_ae
        self.file_tipo = path_tipo
        self.file_rec = path_rec
        
        # Carrega o índice B+ ao iniciar
        # Conforme a spec: árvores podem ser carregadas integralmente em memória 
        self.index = BPlusTree.load("data/bin/index_primary.dat")

        # Tries
        self.index_modelo = Trie.load("data/bin/index_modelo.dat") # Carrega a Trie para índice secundário de modelo
        self.index_cidade = Trie.load("data/bin/index_cidade.dat") # Carrega Trie de cidades
        self.index_categoria = Trie.load("data/bin/index_categoria.dat") # Carrega Trie de categoria

        # BST de índice invertido
        self.index_uf = IndiceInvertidoBST.load("data/bin/index_uf.dat")
        self.index_investigacao = IndiceInvertidoBST.load("data/bin/index_investigacao.dat")


    def buscar_ocorrencia_por_id(self, codigo_id):
        """Busca O(log n) usando a Árvore B+"""
        offset = self.index.search(codigo_id)
        if offset is None:
            return None
        return self.ler_ocorrencia(offset)
    
    def buscar_por_modelo(self, modelo_parcial):
        """Busca Ocorrências por prefixo do Modelo da Aeronave"""
        ids = self.index_modelo.search_prefix(modelo_parcial)
        return self._recuperar_ocorrencias_por_ids(ids)

    def buscar_por_cidade(self, cidade_parcial):
        """Busca Ocorrências por prefixo do nome da Cidade"""
        ids = self.index_cidade.search_prefix(cidade_parcial)
        return self._recuperar_ocorrencias_por_ids(ids)
    
    def buscar_por_categoria_tipo(self, categoria_parcial):
        """Busca Ocorrências por prefixo da Categoria/Tipo da Ocorrência"""
        ids = self.index_categoria.search_prefix(categoria_parcial)
        return self._recuperar_ocorrencias_por_ids(ids)
    
    def buscar_por_uf(self, uf):
        # Ex: uf = 'SP'
        """Busca Ocorrências por UF usando o índice invertido (BST)"""
        ids = self.index_uf.buscar(uf) 
        return self._recuperar_ocorrencias_por_ids(ids)
    
    def buscar_por_status_investigacao(self, status):
        # Ex: status = 'FINALIZADA' ou 'ATIVA'
        """Busca Ocorrências por Status da Investigação usando o índice invertido (BST)"""
        ids = self.index_investigacao.buscar(status) 
        return self._recuperar_ocorrencias_por_ids(ids)

    def _recuperar_ocorrencias_por_ids(self, lista_ids):
        """Método auxiliar para evitar repetição de código"""
        ocorrencias = []
        # Usar set para remover duplicatas caso o mesmo ID apareça 2x (ex: 2 aeronaves do mesmo modelo no mesmo acidente)
        for cod in set(lista_ids): 
            offset = self.index.search(cod)
            if offset is not None:
                oc = self.ler_ocorrencia(offset)
                if oc:
                    ocorrencias.append(oc)
        return ocorrencias

    def ler_ocorrencia(self, offset):
        """Lê uma ocorrência dado o offset (acesso direto)"""
        if offset < 0: return None
        with open(self.file_oc, 'rb') as f:
            f.seek(offset)
            dados = f.read(Ocorrencia.TAMANHO)
            if not dados: return None
            return Ocorrencia.from_bytes(dados)
    
    def ler_aeronaves(self, ocorrencia):
        """Percorre a lista de aeronaves"""
        lista = []
        prox = ocorrencia.pont_aeronave
        if prox == -1: return []

        with open(self.file_ae, 'rb') as f:
            while prox != -1:
                f.seek(prox)
                dados = f.read(Aeronave.TAMANHO)
                if not dados: break
                obj = Aeronave.from_bytes(dados)
                lista.append(obj)
                prox = obj.prox_aeronave
        return lista

    def ler_tipos(self, ocorrencia):
        """Percorre a lista de tipos"""
        lista = []
        prox = ocorrencia.pont_tipo
        if prox == -1: return []

        with open(self.file_tipo, 'rb') as f:
            while prox != -1:
                f.seek(prox)
                dados = f.read(OcorrenciaTipo.TAMANHO)
                if not dados: break
                obj = OcorrenciaTipo.from_bytes(dados)
                lista.append(obj)
                prox = obj.prox_tipo
        return lista

    def ler_recomendacoes(self, ocorrencia):
        """Percorre a lista de recomendações"""
        lista = []
        prox = ocorrencia.pont_recomendacao
        if prox == -1: return []

        with open(self.file_rec, 'rb') as f:
            while prox != -1:
                f.seek(prox)
                dados = f.read(Recomendacao.TAMANHO)
                if not dados: break
                obj = Recomendacao.from_bytes(dados)
                lista.append(obj)
                prox = obj.prox_rec
        return lista
    

