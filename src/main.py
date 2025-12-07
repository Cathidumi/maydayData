import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from importer import importar_tudo

from teste_leitura import testar_simples
from buscas import busca_na_arvore, busca_na_trie_modelo, busca_trie_cidade, busca_trie_categoria

def main():
    try:
        importar_tudo()
    except Exception as e:
        print(f"Erro crítico na importação: {e}")
        return

    #-------------------------------
    # APENAS PARA FINS DE TESTES
    try:
        testar_simples()
    except Exception as e:
        print(f"Erro ao ler os dados: {e}")
        return
    
    """  # BUSCA NA ÁRVORE B+
    print('\n--- Teste de Busca na Árvore B+ ---\n')
    try:
        busca_na_arvore(87124)
    except Exception as e:
        print(f"Erro ao buscar na árvore B+: {e}")
        return """
    
def app():
    while True:
        print('\n--- Menu Principal ---')
        print('1. Busca por Código de Ocorrência')
        print('2. Busca por modelo de Aeronave')
        print('3. Busca por cidade')
        print('4. Busca por categoria de Ocorrência')
        print('sair. Sair do programa')
        escolha = input('Escolha uma opção: ')
        if escolha == '1':
            try:
                codigo = int(input('Digite o código da ocorrência: '))
                busca_na_arvore(codigo)
            except Exception as e:
                print(f"Erro ao buscar na árvore B+: {e}")
        elif escolha == '2':
            try:
                modelo = input('Digite o modelo da aeronave: ')
                busca_na_trie_modelo(modelo)
            except Exception as e:
                print(f"Erro ao buscar por modelo na Trie: {e}")
        elif escolha == '3':
            try:
                cidade = input('Digite a cidade da ocorrência: ')
                busca_trie_cidade(cidade)
            except Exception as e:
                print(f"Erro ao buscar por cidade na Trie: {e}")
        elif escolha == '4':
            try:
                categoria = input('Digite a categoria/tipo da ocorrência: ')
                busca_trie_categoria(categoria)
            except Exception as e:
                print(f"Erro ao buscar por categoria/tipo na Trie: {e}")
        elif escolha.lower() == 'sair':
            print('Saindo do programa.')
            break
        else:
            print('Opção inválida. Tente novamente.')

if __name__ == "__main__":
    main()
    app()