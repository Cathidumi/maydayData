import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from importer import importar_tudo
from teste_leitura import testar_simples
from teste_busca import busca_na_arvore

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
    
    # BUSCA NA ÁRVORE B+
    print('\n--- Teste de Busca na Árvore B+ ---\n')
    try:
        busca_na_arvore(87124)
    except Exception as e:
        print(f"Erro ao buscar na árvore B+: {e}")
        return

if __name__ == "__main__":
    main()