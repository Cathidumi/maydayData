import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from importer import importar_tudo

from buscas import busca_na_arvore, busca_na_trie_modelo, busca_trie_cidade, busca_trie_categoria, busca_bst_uf, busca_bst_status_investigacao, busca_bst_fatalidades
from database import Database

def main():
    try:
        importar_tudo()
    except Exception as e:
        print(f"Erro crítico na importação: {e}")
        return

def app_main():
    clear_terminal()
    print("Carregando banco de dados e índices, por favor aguarde...")

    try:
        db = Database(
            path_oc="data/bin/ocorrencias.dat",
            path_ae="data/bin/aeronaves.dat",
            path_tipo="data/bin/tipos.dat",
            path_rec="data/bin/recomendacoes.dat"
        )
    except Exception as e:
        print(f"Erro fatal ao carregar banco de dados: {e}")
        return
    
    menu_principal()

    while True:
        menu_principal()
        input_opcao = input('\nEscolha uma opção: ')
        if input_opcao == '1':
            app_busca_por_codigo(db)
            voltar_ao_menu()
        elif input_opcao == '2':
            busca_na_trie_modelo(db)
        elif input_opcao == '3':
            busca_trie_cidade(db)
        elif input_opcao == '4':
            busca_trie_categoria(db)
        elif input_opcao == '5':
            busca_bst_uf(db)
        elif input_opcao == '6':
            busca_bst_status_investigacao(db)
        elif input_opcao == '7':
            busca_bst_fatalidades(db)

        elif input_opcao == 'sair':
            print('Saindo do programa.')
            return
        else:
            print('Opção inválida. Tente novamente.')
    

    
def clear_terminal():
    # Check the operating system name
    if os.name == 'nt':
        # Command for Windows
        _ = os.system('cls')
    else:
        # Command for Linux and macOS (posix is the name for non-Windows)
        _ = os.system('clear')

def app_busca_por_codigo(db):
    clear_terminal()
    try:
        codigo = int(input('Digite o código da ocorrência: '))
        print()
        busca_na_arvore(db, codigo)
    except Exception as e:
        print(f"Erro ao buscar na árvore B+: {e}")

def menu_principal():
    clear_terminal()
    texto_inicial = 'MaydaData - Sistema de Pesquisa de Ocorrências Aéreas na Aviação Civil Brasileira'
    largura_console = os.get_terminal_size().columns # 158 na minha tela
    print(f'\n{'-'*largura_console}\n{texto_inicial.center(largura_console)}\n{"-"*largura_console}\n')
    print('Menu principal')
    print('1. Busca por Código de Ocorrência')
    print('2. Busca por modelo de Aeronave')
    print('3. Busca por cidade')
    print('4. Busca por categoria de Ocorrência')
    print('5. Busca por UF')
    print('6. Busca por Status da Investigação')
    print('7. Busca por Fatalidades')
    print('sair. Sair do programa')

def voltar_ao_menu():
    input('\nPressione Enter para voltar ao menu principal...')
    menu_principal()

if __name__ == "__main__":
    main()
    #app()
    app_main()