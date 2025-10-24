# 💿 Sistema de Gerenciamento de Arquivos com Lista Encadeada

Um simulador de sistema de arquivos que implementa alocação encadeada de blocos, desenvolvido em Python para fins educacionais.

## 📋 Descrição do Projeto

Este projeto simula um sistema de arquivos simples onde:

- O disco é organizado em **32 blocos** de 32 bits cada (total de 1024 bits)
- Cada bloco contém **16 bits para dados** (char) e **16 bits para ponteiro** (short int)
- Os arquivos são armazenados como listas encadeadas de blocos
- Suporte para criação, leitura e exclusão de arquivos
- Gerenciamento automático de fragmentação e espaços livres

## 🔧 Componentes Principais

### 1. **Disco (disk.py)**

- Simula o hardware de armazenamento usando arrays Python
- Organiza dados em blocos com estrutura `[dado|ponteiro]`
- Implementa operações básicas de leitura/escrita

### 2. **Sistema de Arquivos (filesystem.py)**

- Gerencia a tabela de diretório
- Implementa alocação/liberação de blocos
- Controla a lista de blocos livres
- Operações CRUD em arquivos

### 3. **Interface (main.py + ui.py)**

- Menu interativo para o usuário
- Visualização rica dos dados usando biblioteca `rich`
- Funções auxiliares para debugging e demonstração

## 📦 Instalação

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. **Clone o repositório:**

```bash
git clone https://github.com/evertonreis1/gerenciamento-arquivos.git
cd gerenciamento-arquivos
```

2. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

3. **Execute o programa:**

```bash
python main.py
```

## 🎮 Como Usar

### Menu Principal

```
Gerenciador de Arquivos (Alocação Encadeada)

1. Criar Arquivo
2. Ler Arquivo
3. Excluir Arquivo
4. Mostrar Tabela de Diretório
5. Mostrar Lista de Blocos Livres
6. Mostrar Disco Completo
7. Sair
```

### Exemplos de Uso

#### Criando um Arquivo

```
Escolha: 1
Nome do arquivo (max 4 chars): arq1
Conteúdo (palavra): hello
✅ Arquivo 'arq1' criado (Início: Bloco 0).
```

#### Lendo um Arquivo

```
Escolha: 2
Nome do arquivo para ler: arq1
📖 Leitura de 'arq1': "hello"
```

#### Visualizando o Disco

```
Escolha: 6
💿 Status Atual do Disco
┌───────┬──────┬──────────┐
│ Bloco │ Data │ Ponteiro │
├───────┼──────┼──────────┤
│     0 │ 'h'  │        1 │
│     1 │ 'e'  │        2 │
│     2 │ 'l'  │        3 │
│     3 │ 'l'  │        4 │
│     4 │ 'o'  │     NULL │
│     5 │ ''   │        6 │
│   ... │ ...  │      ... │
└───────┴──────┴──────────┘
```

## 📊 Especificações Técnicas

### Estrutura do Disco

- **Tamanho total:** 1024 bits (32 blocos × 32 bits)
- **Estrutura do bloco:** [16 bits dados | 16 bits ponteiro]
- **Capacidade máxima:** 32 caracteres (se não fragmentado)

### Limitações

- **Nome do arquivo:** Máximo 4 caracteres
- **Conteúdo:** Apenas caracteres ASCII
- **Tamanho máximo por arquivo:** Limitado pelos blocos disponíveis
- **Número de arquivos:** Limitado pela memória disponível

### Algoritmos Implementados

- **Alocação:** First-fit com lista encadeada de blocos livres
- **Fragmentação:** Suportada automaticamente
- **Desfragmentação:** Não implementada (característica do algoritmo)

## 🔍 Funcionalidades Detalhadas

### ✅ Criação de Arquivos

- Verifica disponibilidade de espaço antes da criação
- Aloca blocos sequencialmente da lista livre
- Encadeia blocos para formar o arquivo
- Atualiza tabela de diretório

### ✅ Leitura de Arquivos

- Percorre lista encadeada de blocos
- Reconstrói conteúdo original
- Exibe resultado formatado

### ✅ Exclusão de Arquivos

- Remove entrada da tabela de diretório
- Libera todos os blocos do arquivo
- Retorna blocos para lista livre

### ✅ Visualização do Sistema

- **Tabela de Diretório:** Lista todos os arquivos e seus blocos iniciais
- **Lista de Blocos Livres:** Mostra cadeia de blocos disponíveis
- **Status do Disco:** Visão completa de todos os blocos

## 🧪 Exemplos de Teste

### Teste de Fragmentação

```python
# Criar arquivos para testar fragmentação
1. Criar "arq1" com "hello" (ocupa blocos 0-4)
2. Criar "arq2" com "world" (ocupa blocos 5-9)
3. Excluir "arq1" (libera blocos 0-4)
4. Criar "arq3" com "test" (reutiliza blocos 0-3)
```

### Teste de Limite de Memória

```python
# Tentar criar arquivo maior que espaço disponível
1. Criar arquivo com 35 caracteres (falha - máximo 32)
2. Verificar mensagem: "Memória insuficiente"
```

## 🔧 Estrutura de Arquivos

```
gerenciamento-arquivos/
├── README.md              # Este arquivo
├── requirements.txt       # Dependências Python
├── main.py               # Interface principal e menu
├── filesystem.py         # Lógica do sistema de arquivos
├── disk.py              # Simulação do disco físico
└── ui.py                # Funções de visualização
```

## 📄 Licença

Este projeto é desenvolvido para fins educacionais.

## 👨‍💻 Autor

Desenvolvido como projeto acadêmico para demonstração de conceitos de Sistemas Operacionais.
