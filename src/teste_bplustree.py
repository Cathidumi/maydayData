import os
import sys

# Adiciona o diretório 'src' ao PATH para garantir que os módulos sejam encontrados
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from bplustree import BPlusTree
except ImportError:
    print("ERRO: O arquivo bplustree.py não foi encontrado no diretório src.")
    sys.exit(1)


def testar_arvore():
    """
    Testa a funcionalidade básica de inserção, salvamento, carregamento e busca
    da Árvore B+.
    """
    ARQUIVO_INDICE = "data/bin/test_index.idx"
    
    print("-" * 30)
    print("INICIANDO TESTE DA ÁRVORE B+")
    print("-" * 30)

    # 1. Teste de Inserção
    print("1. Criando e populando a Árvore B+ em memória...")
    
    # Cria uma nova instância da BPlusTree para os testes
    # (Usaremos um nome de arquivo de teste para não interferir no índice principal)
    tree_insert = BPlusTree(order=5, filename=ARQUIVO_INDICE)
    
    # Simula a inserção de códigos de ocorrência (chaves) e seus offsets (valores)
    dados_teste = [
        (80000, 0),    # Código 80000, Offset 0
        (80005, 130),  # Código 80005, Offset 130
        (80002, 260),  # Código 80002, Offset 260
        (80010, 390),  # Código 80010, Offset 390
        (80001, 520),  # Código 80001, Offset 520
        (80003, 650),  # Código 80003, Offset 650
        (80004, 780),  # Código 80004, Offset 780
    ]

    for key, offset in dados_teste:
        tree_insert.insert(key, offset)
    
    print(f"   -> {len(dados_teste)} registros inseridos.")

    # 2. Teste de Persistência (Save)
    print("\n2. Salvando a Árvore B+ no disco...")
    try:
        # A BPlusTree.save() já deve ter a lógica para aumentar o limite de recursão.
        tree_insert.save()
        print(f"   -> Arquivo de índice salvo em: {ARQUIVO_INDICE}")
    except Exception as e:
        print(f"   -> ERRO FATAL ao salvar o índice: {e}")
        return

    # 3. Teste de Recuperação (Load)
    print("\n3. Carregando a Árvore B+ do disco...")
    tree_loaded = BPlusTree.load(filename=ARQUIVO_INDICE)
    print("   -> Árvore carregada com sucesso na memória.")

    # 4. Teste de Busca (Search)
    print("\n4. Testando a busca (Search):")
    
    # Busca por chave existente
    key_existente = 80002
    offset_encontrado = tree_loaded.search(key_existente)
    print(f"   -> Busca pelo Código {key_existente}: Offset = {offset_encontrado} (Esperado: 260)")

    key_existente_2 = 80001
    offset_encontrado_2 = tree_loaded.search(key_existente_2)
    print(f"   -> Busca pelo Código {key_existente_2}: Offset = {offset_encontrado_2} (Esperado: 520)")

    # Busca por chave inexistente
    key_inexistente = 99999
    offset_nao_encontrado = tree_loaded.search(key_inexistente)
    print(f"   -> Busca pelo Código {key_inexistente}: Offset = {offset_nao_encontrado} (Esperado: None)")
    
    # Verificação de resultados
    if offset_encontrado == 260 and offset_nao_encontrado is None:
        print("\n✅ TESTE DE BUSCA CONCLUÍDO COM SUCESSO!")
    else:
        print("\n❌ TESTE DE BUSCA FALHOU! Verifique o método search.")
        
    # Limpeza do arquivo de teste
    if os.path.exists(ARQUIVO_INDICE):
        os.remove(ARQUIVO_INDICE)
        print(f"\nArquivo de teste {ARQUIVO_INDICE} removido.")

if __name__ == "__main__":
    testar_arvore()