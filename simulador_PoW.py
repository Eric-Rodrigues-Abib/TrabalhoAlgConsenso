import hashlib
import threading
import time
import random
from queue import Queue

# Configuração inicial
DIFFICULTY = 4  # Número de zeros no início do hash
NUM_NODES = 5
BLOCKCHAIN = []  # Lista para armazenar os blocos
RUNNING = True  # Controle para encerrar o programa

class Node(threading.Thread):
    def __init__(self, node_id, message_queue):
        super().__init__()
        self.node_id = node_id
        self.message_queue = message_queue
        self.active = True
        self.recovering = False

    def run(self):
        global RUNNING
        while RUNNING:
            if not self.active:
                time.sleep(random.randint(5, 10))  # Simula recuperação
                self.recover()
            else:
                self.mine_block()

    def mine_block(self):
        if BLOCKCHAIN:
            prev_hash = BLOCKCHAIN[-1]['hash']
        else:
            prev_hash = "0" * 64  # Gênesis

        nonce = 0
        while self.active and RUNNING:
            block_data = f"Node-{self.node_id}-{nonce}-{prev_hash}"
            block_hash = hashlib.sha256(block_data.encode()).hexdigest()
            if block_hash.startswith("0" * DIFFICULTY):
                # Envia o bloco para validação
                block = {"node": self.node_id, "nonce": nonce, "hash": block_hash, "prev_hash": prev_hash}
                self.message_queue.put(block)
                print(f"Node-{self.node_id} mined a block: {block_hash}")
                break
            nonce += 1

    def fail(self):
        self.active = False
        self.recovering = True
        print(f"Node-{self.node_id} has failed!")

    def recover(self):
        self.active = True
        self.recovering = False
        print(f"Node-{self.node_id} has recovered and resumed mining!")

def coordinator(message_queue):
    global RUNNING, BLOCKCHAIN
    while RUNNING:
        try:
            block = message_queue.get(timeout=1)  # Timeout para evitar bloqueio
            if not BLOCKCHAIN or block['prev_hash'] == BLOCKCHAIN[-1]['hash']:
                BLOCKCHAIN.append(block)
                print(f"Block added to blockchain: {block['hash']}")
            else:
                print(f"Invalid block rejected from Node-{block['node']}")
        except:
            continue  # Se não houver mensagens na fila, continua

def simulate_failures(nodes):
    global RUNNING
    while RUNNING:
        time.sleep(random.randint(10, 20))
        node = random.choice(nodes)
        if node.active:
            node.fail()

# Inicializa os nós e o coordenador
message_queue = Queue()
nodes = [Node(node_id, message_queue) for node_id in range(NUM_NODES)]
coordinator_thread = threading.Thread(target=coordinator, args=(message_queue,))

# Inicia a simulação
for node in nodes:
    node.start()
coordinator_thread.start()

failure_thread = threading.Thread(target=simulate_failures, args=(nodes,))
failure_thread.start()

# Controla o encerramento do programa
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down...")
    RUNNING = False

# Aguarda as threads finalizarem
for node in nodes:
    node.join()
coordinator_thread.join()
failure_thread.join()

print("\nBlockchain Final:")
for i, block in enumerate(BLOCKCHAIN):
    print(f"Bloco {i + 1}: {block}")

print("Program terminated.")
