import struct
import os

class TrieNode:
    def __init__(self):
        self.children = {}  # Dicionário: char -> TrieNode
        self.is_end_of_word = False
        self.values = []    # Lista de IDs (codigo_ocorrencia)
        
        # Atributos auxiliares para persistência (não usados na lógica em memória)
        self._my_offset = -1
        self._temp_children_offsets = {} # char -> offset

class Trie:
    def __init__(self, filename="data/bin/index_modelo.dat"):
        self.root = TrieNode()
        self.filename = filename

    # --- Lógica em Memória ---

    def insert(self, key, value):
        """
        Insere uma chave (modelo) e associa um ID (value).
        Normaliza a chave para maiúsculas e remove espaços extras.
        """
        node = self.root
        key_normalized = key.strip().upper()
        
        for char in key_normalized:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
        if value not in node.values:
            node.values.append(value)

    def search(self, key):
        """Busca exata: Retorna lista de IDs para o modelo exato."""
        node = self.root
        key_normalized = key.strip().upper()
        
        for char in key_normalized:
            if char not in node.children:
                return []
            node = node.children[char]
        
        if node.is_end_of_word:
            return node.values
        return []

    def search_prefix(self, prefix):
        """Busca por prefixo: Retorna lista de IDs de todos modelos que começam com o prefixo."""
        node = self.root
        prefix_normalized = prefix.strip().upper()
        
        # 1. Navegar até o fim do prefixo
        for char in prefix_normalized:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # 2. Coletar todos os valores a partir deste nó
        results = []
        self._collect_values(node, results)
        return results

    def _collect_values(self, node, results):
        """Método auxiliar recursivo para coletar valores da subárvore."""
        if node.is_end_of_word:
            results.extend(node.values)
        
        for char in node.children:
            self._collect_values(node.children[char], results)

    # --- Persistência (Save/Load com Struct) ---

    def save(self):
        """
        Salva a Trie em formato binário customizado.
        Formato do Nó:
        [Flag Fim(1b)] [Qtd Values(4b)] [Values...] [Qtd Filhos(4b)] [Filhos (Char 1b + Offset 4b)...]
        """
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        
        # 1. Linearizar a árvore (BFS) para calcular offsets
        all_nodes = []
        node_to_offset = {}
        
        # Header: Root Offset (4 bytes)
        current_offset = 4
        
        queue = [self.root]
        visited = set() # Segurança contra ciclos (embora Trie seja acíclica)
        visited.add(id(self.root))

        # Passada 1: Coletar nós e calcular onde cada um será escrito
        idx = 0
        while idx < len(queue):
            node = queue[idx]
            idx += 1
            all_nodes.append(node)
            
            # Calcular tamanho do nó em bytes
            # bool is_end (1) + int num_values (4)
            size = 1 + 4
            # Lista de valores (int 4 bytes cada)
            size += len(node.values) * 4
            # int num_children (4)
            size += 4
            # Lista de filhos: Para cada filho grava-se o CHAR (1 byte) e o OFFSET (4 bytes)
            size += len(node.children) * (1 + 4)
            
            node_to_offset[id(node)] = current_offset
            current_offset += size
            
            # Adicionar filhos na fila
            # Ordenar chaves para garantir determinismo na gravação
            for char in sorted(node.children.keys()):
                child = node.children[char]
                if id(child) not in visited:
                    visited.add(id(child))
                    queue.append(child)

        # 2. Escrever no disco
        with open(self.filename, 'wb') as f:
            # Header: Offset da Raiz
            root_offset = node_to_offset[id(self.root)]
            f.write(struct.pack('<i', root_offset))
            
            for node in all_nodes:
                # Dados básicos
                # '<?i' -> bool (1), int (4)
                f.write(struct.pack('<?i', node.is_end_of_word, len(node.values)))
                
                # Escrever Values (IDs)
                for val in node.values:
                    f.write(struct.pack('<i', int(val)))
                
                # Escrever Filhos
                f.write(struct.pack('<i', len(node.children)))
                
                for char in sorted(node.children.keys()):
                    child_node = node.children[char]
                    child_offset = node_to_offset[id(child_node)]
                    
                    # Char (1 byte encoded latin-1) + Offset (4 bytes)
                    b_char = char.encode('latin-1', errors='replace')[:1]
                    f.write(struct.pack('<c', b_char)) 
                    f.write(struct.pack('<i', child_offset))
        
        print(f"Índice Secundário (Trie) salvo em {self.filename} ({len(all_nodes)} nós).")

    @staticmethod
    def load(filename="data/bin/index_modelo.dat"):
        """Carrega a Trie do disco."""
        if not os.path.exists(filename):
            print("Índice secundário não encontrado. Criando nova Trie.")
            return Trie(filename=filename)

        with open(filename, 'rb') as f:
            # Ler Header
            data = f.read(4)
            if not data: return Trie(filename=filename)
            root_offset = struct.unpack('<i', data)[0]
            
            trie = Trie(filename=filename)
            offset_to_node = {}
            
            # Fila de offsets para processar
            queue_offsets = [root_offset]
            processed_offsets = set()
            
            while queue_offsets:
                curr_off = queue_offsets.pop(0)
                if curr_off in processed_offsets:
                    continue
                
                f.seek(curr_off)
                
                # Ler Cabeçalho do Nó: is_end (1) + num_values (4) -> 5 bytes
                head_data = f.read(5)
                is_end, num_values = struct.unpack('<?i', head_data)
                
                node = TrieNode()
                node.is_end_of_word = is_end
                
                # Ler Values
                if num_values > 0:
                    val_data = f.read(4 * num_values)
                    node.values = list(struct.unpack(f'<{num_values}i', val_data))
                
                # Ler Filhos
                child_count_data = f.read(4)
                num_children = struct.unpack('<i', child_count_data)[0]
                
                for _ in range(num_children):
                    # Ler Char (1) + Offset (4) -> 5 bytes
                    child_info = f.read(5)
                    b_char, child_offset = struct.unpack('<ci', child_info)
                    char = b_char.decode('latin-1')
                    
                    node._temp_children_offsets[char] = child_offset
                    
                    if child_offset not in processed_offsets:
                        queue_offsets.append(child_offset)
                
                offset_to_node[curr_off] = node
                processed_offsets.add(curr_off)
            
            # Reconstruir ponteiros
            for node in offset_to_node.values():
                for char, offset in node._temp_children_offsets.items():
                    if offset in offset_to_node:
                        node.children[char] = offset_to_node[offset]
            
            if root_offset in offset_to_node:
                trie.root = offset_to_node[root_offset]
                
            return trie


class No:
    """
    Nó genérico da Árvore Binária de Busca (BST).
    """
    def __init__(self, key):
        self.key = key          # Chave de busca (ex: "SP", "ACIDENTE")
        self.ids = []           # Lista de IDs (Inteiros)
        self.left = None        # Filho à esquerda
        self.right = None       # Filho à direita

class IndiceInvertidoBST:
    def __init__(self, filename, key_size=30):
        """
        :param filename: Caminho do arquivo para salvar/carregar.
        :param key_size: Tamanho fixo da chave em bytes para persistência. 
                         Defina conforme o campo (ex: UF=2, Status=20).
        """
        self.root = None
        self.filename = filename
        self.key_size = key_size 

    # --- Lógica em Memória (BST) ---

    def adicionar(self, chave_raw, _id):
        """
        Insere ou atualiza um nó na BST.
        Normaliza a chave (upper, strip) e trunca pelo key_size.
        """
        if not chave_raw: return
        
        # Normalização genérica: Maiúsculas, remove espaços e corta no tamanho máximo
        key = str(chave_raw).strip().upper()[:self.key_size]
        
        if self.root is None:
            self.root = No(key)
            self.root.ids.append(_id)
        else:
            self._inserir_recursivo(self.root, key, _id)

    def _inserir_recursivo(self, node, key, _id):
        if key == node.key:
            # Encontrou: adiciona ID à lista existente (se não duplicado)
            if _id not in node.ids:
                node.ids.append(_id)
        elif key < node.key:
            if node.left is None:
                node.left = No(key)
                node.left.ids.append(_id)
            else:
                self._inserir_recursivo(node.left, key, _id)
        else: # key > node.key
            if node.right is None:
                node.right = No(key)
                node.right.ids.append(_id)
            else:
                self._inserir_recursivo(node.right, key, _id)

    def buscar(self, termo):
        """Busca na BST em memória."""
        if not termo: return []
        key = str(termo).strip().upper()[:self.key_size]
        return self._buscar_recursivo(self.root, key)

    def _buscar_recursivo(self, node, key):
        if node is None:
            return []
        if key == node.key:
            return node.ids
        elif key < node.key:
            return self._buscar_recursivo(node.left, key)
        else:
            return self._buscar_recursivo(node.right, key)

    # --- Persistência (Arquivo Invertido Genérico) ---

    def save(self):
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        
        nos_ordenados = []
        self._in_order(self.root, nos_ordenados)
        qtd_termos = len(nos_ordenados)
        
        with open(self.filename, 'wb') as f:
            # HEADER: Use '<' para garantir tamanho padrão (8 bytes)
            f.write(struct.pack('<i i', qtd_termos, self.key_size))
            
            # Formatação COM '<' para evitar padding
            # Ex para UF: '<2s i i' (Total exato de 10 bytes)
            fmt = f'<{self.key_size}s i i'
            entry_size = struct.calcsize(fmt) # Calcula tamanho exato da struct
            
            offset_atual = 8 + (qtd_termos * entry_size)
            
            # ESCREVER DIRETÓRIO
            for node in nos_ordenados:
                qtd_ids = len(node.ids)
                b_key = node.key.encode('latin-1', errors='replace')[:self.key_size]
                b_key = b_key.ljust(self.key_size, b'\0')
                
                # Note o '<' no início do formato
                f.write(struct.pack(fmt, b_key, offset_atual, qtd_ids))
                
                offset_atual += (qtd_ids * 4) 
            
            # ESCREVER LISTAS DE POSTAGEM
            for node in nos_ordenados:
                for _id in node.ids:
                    f.write(struct.pack('<i', int(_id)))
                    
        print(f"Índice salvo em {self.filename} (Termos={qtd_termos})")

    def _in_order(self, node, lista):
        if node:
            self._in_order(node.left, lista)
            lista.append(node)
            self._in_order(node.right, lista)

    @staticmethod
    def load(filename):
        instance = IndiceInvertidoBST(filename)
        if not os.path.exists(filename):
            print(f"Índice {filename} não encontrado. Criando novo.")
            return instance

        with open(filename, 'rb') as f:
            data = f.read(8)
            if not data: return instance
            qtd_termos, loaded_key_size = struct.unpack('<i i', data)
            
            instance.key_size = loaded_key_size
            
            # Formatação COM '<'
            fmt = f'<{instance.key_size}s i i'
            entry_size = struct.calcsize(fmt) # Garante que leremos o tamanho correto
            
            dir_bytes = f.read(qtd_termos * entry_size)
            
            diretorio = []
            for i in range(qtd_termos):
                inicio = i * entry_size
                chunk = dir_bytes[inicio : inicio + entry_size]
                
                # Agora o chunk terá o tamanho exato que o unpack espera
                b_key, offset, qtd = struct.unpack(fmt, chunk)
                
                key_str = b_key.decode('latin-1').strip('\x00')
                diretorio.append((key_str, offset, qtd))
            
            for key, offset, qtd in diretorio:
                f.seek(offset)
                raw_ids = f.read(qtd * 4)
                if len(raw_ids) < qtd * 4: continue
                lista_ids = struct.unpack(f'<{qtd}i', raw_ids)
                for _id in lista_ids:
                    instance.adicionar(key, _id)
                    
        return instance