import array
import warnings

# Ignora o aviso de depreciação do tipo 'u' (char)
warnings.filterwarnings("ignore", message="The 'u' type code is deprecated")

class Disk:
    """
    Simula o disco físico de baixo nível.
    
    Organizado em 32 blocos.
    Cada bloco tem 16 bits para dados (char) e 16 bits para ponteiro (short int).
    """
    DISK_SIZE = 32
    NULL_POINTER = -1

    def __init__(self):
        """
        Inicializa os arrays (vetores) que representam o disco.
        """
        # Array para os dados (1 caractere por bloco)
        try:
            # 'u' -> Py_UNICODE (representa o 'char' de 16 bits)
            self.data = array.array('u', ['\0'] * self.DISK_SIZE)
        except (ValueError, TypeError):
            print("Erro: Tipo 'u' não suportado. Use uma versão Python com suporte a Py_UNICODE.")
            exit()
            
        # Array para os ponteiros (o próximo bloco da lista)
        # 'h' -> signed short int (representa o 'short int' de 16 bits)
        self.pointers = array.array('h', [0] * self.DISK_SIZE)
        
    def initialize_free_list(self):
        """
        Configura a lista encadeada inicial de blocos livres.
        O disco começa com blocos 0 -> 1 -> 2 -> ... -> 31 -> NULL.
        """
        for i in range(self.DISK_SIZE - 1):
            self.pointers[i] = i + 1
        self.pointers[self.DISK_SIZE - 1] = self.NULL_POINTER
        
    def write(self, block_index, data, pointer):
        """Escreve um caractere e um ponteiro em um bloco."""
        if 0 <= block_index < self.DISK_SIZE:
            self.data[block_index] = data
            self.pointers[block_index] = pointer
        
    def read(self, block_index):
        """Lê o par (dado, ponteiro) de um bloco."""
        if 0 <= block_index < self.DISK_SIZE:
            return self.data[block_index], self.pointers[block_index]
        return None, None
        
    def clear_block_data(self, block_index):
        """Limpa apenas o dado de um bloco, preservando o ponteiro (para a lista livre)."""
        if 0 <= block_index < self.DISK_SIZE:
            self.data[block_index] = '\0'