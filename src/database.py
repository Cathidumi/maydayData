import os
from model import Ocorrencia, Aeronave, OcorrenciaTipo, Recomendacao
from bplustree import BPlusTree # <--- IMPORTAR

class Database:
    def __init__(self, path_oc, path_ae, path_tipo, path_rec):
        self.file_oc = path_oc
        self.file_ae = path_ae
        self.file_tipo = path_tipo
        self.file_rec = path_rec
        
        # Carrega o índice B+ ao iniciar
        # Conforme a spec: árvores podem ser carregadas integralmente em memória 
        self.index = BPlusTree.load("data/bin/index_primary.idx")

    def buscar_ocorrencia_por_id(self, codigo_id):
        """Busca O(log n) usando a Árvore B+"""
        offset = self.index.search(codigo_id)
        if offset is None:
            return None
        return self.ler_ocorrencia(offset)

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
