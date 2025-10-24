import array
import warnings

warnings.filterwarnings("ignore", message="The 'u' type code is deprecated")


class Disk:
    DISK_SIZE = 32
    NULL_POINTER = -1

    def __init__(self):
        try:
            self.data = array.array('u', ['\0'] * self.DISK_SIZE)
        except (ValueError, TypeError):
            print(
                "Erro: Tipo 'u' não suportado. Use uma versão Python com suporte a Py_UNICODE.")
            exit()

        self.pointers = array.array('h', [0] * self.DISK_SIZE)

    def initialize_free_list(self):
        for i in range(self.DISK_SIZE - 1):
            self.pointers[i] = i + 1
        self.pointers[self.DISK_SIZE - 1] = self.NULL_POINTER

    def write(self, block_index, data, pointer):
        if 0 <= block_index < self.DISK_SIZE:
            self.data[block_index] = data
            self.pointers[block_index] = pointer

    def read(self, block_index):
        if 0 <= block_index < self.DISK_SIZE:
            return self.data[block_index], self.pointers[block_index]
        return None, None

    def clear_block_data(self, block_index):
        if 0 <= block_index < self.DISK_SIZE:
            self.data[block_index] = '\0'
