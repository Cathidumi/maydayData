import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from importer import importar_tudo

from teste_leitura import testar_simples
from buscas import busca_na_arvore, busca_na_trie_modelo, busca_na_trie_modelo_paginada, busca_trie_cidade, busca_trie_cidade_paginada, busca_trie_categoria, busca_bst_uf, busca_bst_status_investigacao, busca_bst_fatalidades
from database import Database

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
    
def app():
    try:
        db = Database(
            path_oc="data/bin/ocorrencias.dat",
            path_ae="data/bin/aeronaves.dat",
            path_tipo="data/bin/tipos.dat",
            path_rec="data/bin/recomendacoes.dat"
        )
        print("Índices carregados com sucesso!")
    except Exception as e:
        print(f"Erro fatal ao carregar banco de dados: {e}")
        return

    while True:
        print('\n--- Menu Principal ---')
        print('1. Busca por Código de Ocorrência')
        print('2. Busca por modelo de Aeronave')
        print('3. Busca por cidade')
        print('4. Busca por categoria de Ocorrência')
        print('5. Busca por UF')
        print('6. Busca por Status da Investigação')
        print('7. Busca por Fatalidades')
        print('sair. Sair do programa')
        escolha = input('Escolha uma opção: ')
        if escolha == '1':
            try:
                codigo = int(input('Digite o código da ocorrência: '))
                busca_na_arvore(db, codigo)
            except Exception as e:
                print(f"Erro ao buscar na árvore B+: {e}")
        elif escolha == '2':
            try:
                modelo = input('Digite o modelo da aeronave: ')
                busca_na_trie_modelo(db, modelo)
            except Exception as e:
                print(f"Erro ao buscar por modelo na Trie: {e}")
        elif escolha == '3':
            try:
                cidade = input('Digite a cidade da ocorrência: ')
                busca_trie_cidade(db, cidade)
            except Exception as e:
                print(f"Erro ao buscar por cidade na Trie: {e}")
        elif escolha == '4':
            try:
                categoria = input('Digite a categoria da ocorrência: ')
                busca_trie_categoria(db, categoria)
            except Exception as e:
                print(f"Erro ao buscar por categoria/tipo na Trie: {e}")
        elif escolha == '5':
            try:
                uf = input('Digite a UF da ocorrência (ex: SP): ')
                busca_bst_uf(db, uf)
            except Exception as e:
                print(f"Erro ao buscar por UF na BST: {e}")
        elif escolha == '6':
            try:
                status = input('Digite o Status da Investigação (ex: FINALIZADA, ATIVA): ')
                busca_bst_status_investigacao(db, status)
            except Exception as e:
                print(f"Erro ao buscar por Status da Investigação na BST: {e}")
        elif escolha == '7':
            try:
                qtd = int(input('Digite a quantidade de fatalidades: '))
                busca_bst_fatalidades(db, qtd)
            except Exception as e:
                print(f"Erro ao buscar por Fatalidades: {e}")
        elif escolha.lower() == 'sair':
            print('Saindo do programa.')
            break
        else:
            print('Opção inválida. Tente novamente.')

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
        #print("Índices carregados com sucesso!")
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
            busca_na_trie_modelo_paginada(db)
        elif input_opcao == '3':
            busca_trie_cidade_paginada(db)

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
    print(f'Menu principal')
    print(f'1. Busca por Código de Ocorrência')
    print(f'2. Busca por modelo de Aeronave')
    print(f'3. Busca por cidade')
    print(f'sair. Sair do programa')

def voltar_ao_menu():
    input('\nPressione Enter para voltar ao menu principal...')
    menu_principal()

if __name__ == "__main__":
    main()
    #app()
    app_main()