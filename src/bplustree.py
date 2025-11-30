import struct
import os

class Node:
    def __init__(self, is_leaf=False):
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []  # Nós internos (objetos Node)
        self.values = []    # Nós folha (offsets do arquivo de dados - int)
        self.next = None    # Ponteiro para próxima folha (objeto Node)
        
        # Atributos temporários usados apenas durante o load/save para reconstruir ponteiros
        self._temp_children_offsets = []
        self._temp_next_offset = -1
        self._my_file_offset = -1

class BPlusTree:
    def __init__(self, order=5, filename="data/bin/index_primary.idx"):
        self.root = Node(is_leaf=True)
        self.order = order
        self.filename = filename

    # --- MÉTODOS DE INSERÇÃO E BUSCA (Lógica de Memória - Inalterada) ---

    def insert(self, key, value):
        root = self.root
        if len(root.keys) == self.order - 1:
            new_root = Node()
            self.root = new_root
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, key, value)
        else:
            self._insert_non_full(root, key, value)

    def _insert_non_full(self, node, key, value):
        if node.is_leaf:
            idx = 0
            while idx < len(node.keys) and key > node.keys[idx]:
                idx += 1
            node.keys.insert(idx, key)
            node.values.insert(idx, value)
        else:
            idx = len(node.keys) - 1
            while idx >= 0 and key < node.keys[idx]:
                idx -= 1
            idx += 1
            child = node.children[idx]
            if len(child.keys) == self.order - 1:
                self._split_child(node, idx)
                if key > node.keys[idx]:
                    idx += 1
            self._insert_non_full(node.children[idx], key, value)

    def _split_child(self, parent, idx):
        child = parent.children[idx]
        mid = (self.order - 1) // 2
        new_node = Node(is_leaf=child.is_leaf)
        
        parent.keys.insert(idx, child.keys[mid])
        parent.children.insert(idx + 1, new_node)
        
        if child.is_leaf:
            new_node.keys = child.keys[mid:]
            new_node.values = child.values[mid:]
            child.keys = child.keys[:mid]
            child.values = child.values[:mid]
            new_node.next = child.next
            child.next = new_node
        else:
            new_node.keys = child.keys[mid+1:]
            new_node.children = child.children[mid+1:]
            child.keys = child.keys[:mid]
            child.children = child.children[:mid+1]

    def search(self, key):
        current = self.root
        while not current.is_leaf:
            idx = 0
            while idx < len(current.keys) and key >= current.keys[idx]:
                idx += 1
            current = current.children[idx]
        for i, k in enumerate(current.keys):
            if k == key:
                return current.values[i]
        return None

    # --- NOVOS MÉTODOS SAVE/LOAD COM STRUCT (Sem Pickle) ---

    # ... (Mantenha a parte inicial da classe BPlusTree e os métodos insert/search iguais)

    # --- MÉTODOS SAVE/LOAD CORRIGIDOS (Com alinhamento padrão '<') ---

    def save(self):
        """
        Salva a árvore em formato binário customizado usando struct.
        Usa '<' para garantir Little-Endian e sem padding (tamanhos exatos).
        """
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        
        # 1. Linearizar a árvore (BFS)
        all_nodes = []
        node_to_offset = {}
        
        # Header: Order(4) + RootOffset(4) = 8 bytes
        current_offset = 8 
        
        bfs_queue = [self.root]
        visited = set()
        
        # Coleta nós e calcula offsets futuros
        while bfs_queue:
            node = bfs_queue.pop(0)
            if id(node) in visited:
                continue
            visited.add(id(node))
            all_nodes.append(node)
            
            # Cálculo de tamanho exato (sem padding)
            # is_leaf (1 byte) + num_keys (4 bytes)
            size = 1 + 4 
            # keys (4 bytes cada)
            size += (len(node.keys) * 4)
            
            if node.is_leaf:
                # values (4 bytes cada) + next_leaf_offset (4 bytes)
                size += (len(node.values) * 4) + 4
            else:
                # children_offsets (4 bytes cada)
                size += (len(node.children) * 4)
            
            node_to_offset[id(node)] = current_offset
            current_offset += size
            
            if not node.is_leaf:
                for child in node.children:
                    bfs_queue.append(child)

        # 2. Escrever no disco
        with open(self.filename, 'wb') as f:
            # Header: '<ii' (Little-endian, 2 ints)
            root_offset = node_to_offset[id(self.root)]
            f.write(struct.pack('<ii', self.order, root_offset))
            
            for node in all_nodes:
                # Node Header: '<?i' (Little-endian, Bool + Int) -> Exatos 5 bytes
                f.write(struct.pack('<?i', node.is_leaf, len(node.keys)))
                
                # Keys
                for k in node.keys:
                    f.write(struct.pack('<i', int(k)))
                
                if node.is_leaf:
                    # Values
                    for v in node.values:
                        f.write(struct.pack('<i', int(v)))
                    
                    # Next Leaf Pointer
                    if node.next and id(node.next) in node_to_offset:
                        next_off = node_to_offset[id(node.next)]
                        f.write(struct.pack('<i', next_off))
                    else:
                        f.write(struct.pack('<i', -1))
                else:
                    # Children Pointers
                    for child in node.children:
                        child_off = node_to_offset[id(child)]
                        f.write(struct.pack('<i', child_off))

        print(f"Índice B+ salvo com STRUCT em {self.filename} ({len(all_nodes)} nós).")

    @staticmethod
    def load(filename="data/bin/index_primary.idx"):
        """Carrega a árvore reconstruindo os ponteiros a partir dos offsets."""
        if not os.path.exists(filename):
            print("Arquivo de índice não encontrado. Criando nova árvore.")
            return BPlusTree(filename=filename)

        with open(filename, 'rb') as f:
            # Ler Header (8 bytes)
            data = f.read(8)
            if not data: return BPlusTree(filename=filename)
            order, root_offset = struct.unpack('<ii', data)
            
            tree = BPlusTree(order=order, filename=filename)
            offset_to_node = {}
            
            queue_offsets = [root_offset]
            processed_offsets = set()
            
            while queue_offsets:
                curr_off = queue_offsets.pop(0)
                if curr_off in processed_offsets:
                    continue
                
                f.seek(curr_off)
                
                # Ler is_leaf + num_keys (5 bytes exatos graças ao '<')
                head_data = f.read(5)
                is_leaf, num_keys = struct.unpack('<?i', head_data)
                
                node = Node(is_leaf=is_leaf)
                
                # Ler Keys
                keys_data = f.read(4 * num_keys)
                node.keys = list(struct.unpack(f'<{num_keys}i', keys_data))
                
                if is_leaf:
                    # Ler Values
                    vals_data = f.read(4 * num_keys)
                    node.values = list(struct.unpack(f'<{num_keys}i', vals_data))
                    
                    # Ler Next Ptr
                    next_data = f.read(4)
                    node._temp_next_offset = struct.unpack('<i', next_data)[0]
                else:
                    # Ler Children Offsets
                    num_children = num_keys + 1
                    child_data = f.read(4 * num_children)
                    children_offsets = list(struct.unpack(f'<{num_children}i', child_data))
                    node._temp_children_offsets = children_offsets
                    
                    for child_off in children_offsets:
                        if child_off not in processed_offsets:
                            queue_offsets.append(child_off)
                
                offset_to_node[curr_off] = node
                processed_offsets.add(curr_off)

            # Reconstruir Ponteiros de Objeto
            for node in offset_to_node.values():
                if node.is_leaf:
                    if node._temp_next_offset != -1:
                        node.next = offset_to_node.get(node._temp_next_offset)
                else:
                    node.children = []
                    for child_off in node._temp_children_offsets:
                        child_node = offset_to_node.get(child_off)
                        if child_node:
                            node.children.append(child_node)

            if root_offset in offset_to_node:
                tree.root = offset_to_node[root_offset]
            
            return tree