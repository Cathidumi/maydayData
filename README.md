# 🚁 MaydayData

**Repositório dedicado ao desenvolvimento de aplicação vinculada ao trabalho final da disciplina de Classificação e Pesquisa de Dados (CPD), ministrada no Instituto de Informática da UFRGS.**

---

![Diagrama ER do Projeto](https://github.com/user-attachments/assets/5562b9b2-dc79-40f8-8679-b987869a4214)

## 📖 Sobre o Projeto

O **MaydayData** é uma aplicação desktop (CLI) desenvolvida em Python para indexação, busca e visualização de dados sobre ocorrências aeronáuticas no Brasil. O sistema consome dados abertos do **CENIPA**, processa arquivos CSV brutos e os converte para uma estrutura de banco de dados proprietária baseada em arquivos binários.

O objetivo principal deste projeto é demonstrar a implementação manual de estruturas de dados avançadas para armazenamento e recuperação eficiente de informações, **sem a utilização de SGBDs (Sistemas Gerenciadores de Banco de Dados) prontos**.

## 🚀 Funcionalidades

- **Importação e ETL:** Leitura de CSVs (latin-1), tratamento de dados e conversão para arquivos binários (`.dat`).
- **Busca por Código (Índice Primário):** Recuperação instantânea de ocorrências completas.
- **Busca Textual por Prefixo:** Pesquisa eficiente por Modelos de Aeronave, Cidades e Categorias.
- **Filtros Avançados:** Filtragem por UF, Status da Investigação e Número de Fatalidades.
- **Interface Interativa:** Sistema de menus via terminal com **paginação de resultados** e filtros dinâmicos em memória.

## 🛠️ Tecnologias e Estruturas de Dados

Este projeto foi construído utilizando apenas bibliotecas padrão do Python, com foco total na implementação algorítmica:

* **Linguagem:** Python 3.12+
* **Armazenamento:** Arquivos binários de acesso aleatório com registros de tamanho fixo e manipulação de *offsets* (`struct`).
* **Integridade Referencial:** Listas encadeadas em disco para relacionamentos 1:N (Ocorrência -> Aeronaves/Recomendações).

### Estruturas de Indexação Implementadas:
1.  **Árvore B+:** Índice primário para busca por ID da Ocorrência.
2.  **Árvore Trie (Digital):** Índices secundários para buscas textuais (Modelo, Cidade, Categoria).
3.  **Árvore Binária de Busca (BST):** Índices invertidos para campos categóricos (UF, Status) e numéricos (Fatalidades).

## 📂 Estrutura do Projeto

```bash
maydayData/
├── data/
│   ├── raw/           # Arquivos CSV originais do CENIPA
│   └── bin/           # Arquivos binários e índices gerados (.dat)
├── src/
│   ├── main.py        # Ponto de entrada da aplicação
│   ├── database.py    # Gerenciador de I/O e persistência
│   ├── buscas.py      # Lógica de interface e paginação
│   ├── bplustree.py   # Implementação da Árvore B+
│   ├── indexes.py     # Implementações de Trie e BST
│   ├── importer.py    # Script de carga e conversão de dados
│   └── model.py       # Definição das classes e structs
└── README.md
```

## ▶️ Como Executar

Certifique-se de ter o **Python 3** instalado.

1. Clone o repositório:
   ```bash
   git clone [https://github.com/seu-usuario/maydayData.git](https://github.com/seu-usuario/maydayData.git)
   cd maydayData
   ```

2. Coloque os arquivos CSV do CENIPA na pasta `data/raw/` (caso não estejam lá).

3. Execute o programa principal:
   ```bash
   python src/main.py
   ```
   *O sistema verificará a existência dos arquivos binários e realizará a importação automaticamente na primeira execução.*

## 👨‍💻 Autores

Trabalho desenvolvido pelos acadêmicos:

* **André Gabriel** - [Github](https://github.com/AndreVitorG)
* **Cauã Miranda** - [Github](https://github.com/Cathidumi)

---
*Instituto de Informática - UFRGS | 2025/2*
