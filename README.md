# Simulação de Ambiente Distribuído com Proof of Work (PoW)

## Descrição

Este projeto simula um abiente **_distribuído em consenso_** utilizando o **_algoritmo de Proof of Work (PoW)_**. O sistema implementa múltiploes nós que colaboram para minerar blocos e formar uma blockchain, enquanto um coordenador central valida os blocos. A simulação inclui falhas e recuperação de nós, bem como troca de mensagens para garantir a integridade e o consenso da rede

### Algoritmo Implementado

- Proof of Work (PoW)
    - Cada nó tenta encontrar um nonce que, combinado com os dados do bloco e o hash do bloco anterior, resulta em um hash válido (inicia com um número específico de zeros definido pela variável "Difficulty")
    - Os blocos minerados são enviados para um nó coordenador que valida sua integridade antes de adicioná-los à blockchain

## Instruções para Configuração e Execução

### Pré-requisitos
- Python 3.6 ou superior
- Biblioteca **_hashlib_** (já incluída na instalação padrão do Python)
- Sistema operacional com suporte a threads

### Passo a Passo

1. __Clone o repositório__

    ```
    git clone https://github.com/seuusuario/projeto-blockchain.git
    cd projeto-blockchain
    ```

2. __Execute o script__

    ```
    python simulador_PoW.py
    ```

3. __Simular encerramento__

    - Use ctrl+c para interromper o programa
    - O programa finalizará todas as threads e exibirá os blocos minerados na blockchain

### Estrutura do projeto

    ```
    projeto-blockchain/
    ├── simulador_PoW.py       # Script principal com a implementação
    ├── README.md     # Documentação do projeto
    ```

## Fases do Algoritmo

1. __Inicialização__

    - Múltiplos nós são criados e iniciados como threads independentes
    - Um nó coordenador é criado para gerenciar a validação de blocos e a construção da blockchain

2. __Mineração de blocos (Proof of Work)__

    - Cada nó realiza os seguintes passos:
        1. Obtém o hash do bloco anterior (ou um hash inicial para o bloco gênesis).
        2. Incrementa um nonce até encontrar um hash válido
        3. Envia o bloco minerado para o coordenador por meio de uma fila de mensagens

3. __Validação pelo Coordenador__

    - O Coordenador verifica se:
        - O hash do bloco é válido (Começa com o número correto de zeros)
        - O bloco tem o hash do bloco anterior na blockchain
    - Blocos válidos são adicionados à blockchain; blocos inválidos são rejeitados

4 __Simulação de Falhas e Recuperação__

    - Nós falham aleatoriamente durante a execução
    - Nós inativos permanecem fora do processo de mineração até serem "recuperados" após um intervalo de tempo aleatório

## Simulação de Falhas e Respostas do Sistema

### Falhas simuladas

1. __Falha de nó__

    - Um nó pode falhar aleatoriamente (Simulado pela função Simulate_failures):
    ```
    def simulate_failures(nodes):
    global RUNNING
    while RUNNING:
        time.sleep(random.randint(10, 20))
        node = random.choice(nodes)
        if node.active:
            node.fail()
    ```
    - O nó interrompe sua mineração e não aprticipa da rede até se recuperar

2. __Falha na Validação__

    - O coordenador rejeita blocos se
        - O prev_hash não correponder ao hash do último bloco na blockchain
        - O bloco não cumprir os critérios do Proof of Work

### Respostas do Sistema

- Quando um nó falha:
    - Ele entra em estado de recuperação e retoma a mineração após um intervalo aleatório
    - Logs detalham o momento da falha e da recuperação
- Quando um bloco inválido é enviado
    - O coordenador rejeita o bloco e registra um log com o motivo

## Exemplo de Execução

### Logs de mineração

```
Node-1 mined a block: 0000a12bcd34...
Block added to blockchain: 0000a12bcd34...
Node-3 mined a block: 0000b23cde45...
Block added to blockchain: 0000b23cde45...
```

### Logs de falhas

```
Node-2 has failed!
Node-2 has recovered and resumed mining!
```

### Blockchain Final

Após o término do programa, a blockchain será exibida:

```
Shutting down...

Blockchain Final:
Bloco 1: {'node': 2, 'nonce': 124, 'hash': '0000a1b2c3d4...', 'prev_hash': '0'*64}
Bloco 2: {'node': 4, 'nonce': 432, 'hash': '0000e5f6g7h8...', 'prev_hash': '0000a1b2c3d4...'}
Bloco 3: {'node': 1, 'nonce': 789, 'hash': '0000i9j0k1l2...', 'prev_hash': '0000e5f6g7h8...'}

Program terminated.

```

## Autores

**__Eric Rodrigues Abib - 21000481__**
**__Felipe Mafissioni - 22001008__**
**__Lucas Perim - 22001501__**
**__Murilo Apolinario - 22002255__**


