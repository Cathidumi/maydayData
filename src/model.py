import struct

class Ocorrencia:
    # Formato expandido:
    # i   = codigo (4 bytes)
    # 2s  = uf (2 bytes)
    # 50s = cidade (50 bytes)
    # 30s = classificacao (30 bytes)
    # 20s = status investigacao (20 bytes)
    # i   = total aeronaves (4 bytes)
    # i   = pont_aeronave (4 bytes)
    # i   = pont_tipo (4 bytes) - NOVO
    # i   = pont_recomendacao (4 bytes) - NOVO
    FORMATO = 'i 2s 50s 30s 20s i i i i'
    TAMANHO = struct.calcsize(FORMATO)

    def __init__(self, codigo, uf, cidade, classificacao, status, total_aeros, 
                 pont_aeronave=-1, pont_tipo=-1, pont_recomendacao=-1):
        self.codigo = int(codigo)
        self.uf = str(uf)
        self.cidade = str(cidade)
        self.classificacao = str(classificacao)
        self.status = str(status)
        self.total_aeros = int(total_aeros or 0)
        self.pont_aeronave = pont_aeronave
        self.pont_tipo = pont_tipo
        self.pont_recomendacao = pont_recomendacao

    def to_bytes(self):
        return struct.pack(self.FORMATO,
            self.codigo,
            self.uf.encode('latin-1')[:2],
            self.cidade.encode('latin-1')[:50].ljust(50, b'\0'),
            self.classificacao.encode('latin-1')[:30].ljust(30, b'\0'),
            self.status.encode('latin-1')[:20].ljust(20, b'\0'),
            self.total_aeros,
            self.pont_aeronave,
            self.pont_tipo,
            self.pont_recomendacao
        )

    @classmethod
    def from_bytes(cls, dados_bytes):
        t = struct.unpack(cls.FORMATO, dados_bytes)
        return cls(
            codigo=t[0],
            uf=t[1].decode('latin-1', errors='replace'),
            cidade=t[2].decode('latin-1', errors='replace').rstrip('\x00'),
            classificacao=t[3].decode('latin-1', errors='replace').rstrip('\x00'),
            status=t[4].decode('latin-1', errors='replace').rstrip('\x00'),
            total_aeros=t[5],
            pont_aeronave=t[6],
            pont_tipo=t[7],
            pont_recomendacao=t[8]
        )

class Aeronave:
    # Campos: modelo, origem, destino, fatalidades + ponteiro prox
    # 4s para ICAO
    FORMATO = '30s 4s 4s i i' 
    TAMANHO = struct.calcsize(FORMATO)

    def __init__(self, modelo, origem, destino, fatalidades, prox_aeronave=-1):
        self.modelo = str(modelo)
        self.origem = str(origem)
        self.destino = str(destino)
        self.fatalidades = int(fatalidades or 0)
        self.prox_aeronave = prox_aeronave

    def to_bytes(self):
        return struct.pack(self.FORMATO,
            self.modelo.encode('latin-1')[:30].ljust(30, b'\0'),
            self.origem.encode('latin-1')[:4].ljust(4, b'\0'),
            self.destino.encode('latin-1')[:4].ljust(4, b'\0'),
            self.fatalidades,
            self.prox_aeronave
        )

    @classmethod
    def from_bytes(cls, dados_bytes):
        t = struct.unpack(cls.FORMATO, dados_bytes)
        return cls(
            modelo=t[0].decode('latin-1', errors='replace').rstrip('\x00'),
            origem=t[1].decode('latin-1', errors='replace').rstrip('\x00'),
            destino=t[2].decode('latin-1', errors='replace').rstrip('\x00'),
            fatalidades=t[3],
            prox_aeronave=t[4]
        )

class OcorrenciaTipo:
    # Campos: tipo, categoria, taxonomia + ponteiro prox
    FORMATO = '40s 20s 20s i'
    TAMANHO = struct.calcsize(FORMATO)

    def __init__(self, tipo, categoria, taxonomia, prox_tipo=-1):
        self.tipo = str(tipo)
        self.categoria = str(categoria)
        self.taxonomia = str(taxonomia)
        self.prox_tipo = prox_tipo

    def to_bytes(self):
        return struct.pack(self.FORMATO,
            self.tipo.encode('latin-1')[:40].ljust(40, b'\0'),
            self.categoria.encode('latin-1')[:20].ljust(20, b'\0'),
            self.taxonomia.encode('latin-1')[:20].ljust(20, b'\0'),
            self.prox_tipo
        )

    @classmethod
    def from_bytes(cls, dados_bytes):
        t = struct.unpack(cls.FORMATO, dados_bytes)
        return cls(
            tipo=t[0].decode('latin-1', errors='replace').rstrip('\x00'),
            categoria=t[1].decode('latin-1', errors='replace').rstrip('\x00'),
            taxonomia=t[2].decode('latin-1', errors='replace').rstrip('\x00'),
            prox_tipo=t[3]
        )

class Recomendacao:
    # Campos: numero, status, conteudo + ponteiro prox
    # Conteudo reservado 300 bytes (se for maior, corta)
    FORMATO = '20s 15s 300s i'
    TAMANHO = struct.calcsize(FORMATO)

    def __init__(self, numero, status, conteudo, prox_rec=-1):
        self.numero = str(numero)
        self.status = str(status)
        self.conteudo = str(conteudo)
        self.prox_rec = prox_rec

    def to_bytes(self):
        return struct.pack(self.FORMATO,
            self.numero.encode('latin-1')[:20].ljust(20, b'\0'),
            self.status.encode('latin-1')[:15].ljust(15, b'\0'),
            self.conteudo.encode('latin-1')[:300].ljust(300, b'\0'),
            self.prox_rec
        )

    @classmethod
    def from_bytes(cls, dados_bytes):
        t = struct.unpack(cls.FORMATO, dados_bytes)
        return cls(
            numero=t[0].decode('latin-1', errors='replace').rstrip('\x00'),
            status=t[1].decode('latin-1', errors='replace').rstrip('\x00'),
            conteudo=t[2].decode('latin-1', errors='replace').rstrip('\x00'),
            prox_rec=t[3]
        )