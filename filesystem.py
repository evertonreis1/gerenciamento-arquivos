from disk import Disk
import ui # Usaremos o UI para imprimir mensagens de status

class FileSystem:
    """
    Implementa a lógica de gerenciamento de arquivos, diretório e lista livre.
    """
    def __init__(self):
        self.disk = Disk()
        
        # Tabela de diretório (Nome -> Bloco Inicial) [cite: 13]
        self.directory_table = {}
        
        # Gerenciamento da memória livre
        self.free_list_head = 0  # Aponta para a primeira posição livre [cite: 14]
        self.free_space_size = self.disk.DISK_SIZE  # Guarda o tamanho da memória livre [cite: 15]
        
        # Inicializa o disco com a lista livre encadeada [cite: 32]
        self.disk.initialize_free_list()

    def _allocate_block(self):
        """
        Aloca um bloco da lista de livres.
        Retorna o índice do bloco alocado ou NULL_POINTER se não houver espaço.
        """
        if self.free_list_head == self.disk.NULL_POINTER:
            return self.disk.NULL_POINTER
        
        allocated_block_index = self.free_list_head
        
        # Lê o ponteiro do bloco que estamos alocando (que aponta para o próximo livre)
        _data, next_free_block = self.disk.read(allocated_block_index)
        
        # Atualiza o início da lista livre
        self.free_list_head = next_free_block
        self.free_space_size -= 1
        
        # Limpa o ponteiro do bloco alocado
        self.disk.write(allocated_block_index, '\0', self.disk.NULL_POINTER)
        
        return allocated_block_index

    def _free_block(self, block_index):
        """
        Libera um bloco e o retorna ao início da lista de livres.
        """
        self.disk.clear_block_data(block_index)
        
        # Coloca o bloco liberado no início da lista livre
        self.disk.write(block_index, '\0', self.free_list_head)
        self.free_list_head = block_index
        self.free_space_size += 1

    def create_file(self, name, content):
        """
        Cria um novo "arquivo" (palavra) no disco.
        """
        ui.print_info(f"Tentando criar '{name}' (Tamanho: {len(content)})")
        
        # Nome curto de 4 caracteres, no máximo [cite: 9]
        if len(name) > 4:
            ui.print_error(f"Nome '{name}' excede 4 caracteres.")
            return

        if name in self.directory_table:
            ui.print_error(f"Arquivo '{name}' já existe.")
            return

        # Verifica se o espaço livre total é suficiente [cite: 19, 23]
        if len(content) > self.free_space_size:
            ui.print_error(f"Memória insuficiente. (Req: {len(content)}, Disp: {self.free_space_size})")
            return
        
        if len(content) == 0:
            ui.print_error("Conteúdo do arquivo não pode ser vazio.")
            return

        prev_block = self.disk.NULL_POINTER
        first_block = self.disk.NULL_POINTER
        
        # Aloca um bloco para cada caractere
        for char in content:
            current_block = self._allocate_block()
            
            # Escreve o caractere no bloco [cite: 12]
            self.disk.write(current_block, char, self.disk.NULL_POINTER)
            
            if first_block == self.disk.NULL_POINTER:
                first_block = current_block
            
            if prev_block != self.disk.NULL_POINTER:
                # Encadeia o bloco anterior a este [cite: 12]
                _data, _ptr = self.disk.read(prev_block)
                self.disk.write(prev_block, _data, current_block)
            
            prev_block = current_block
        
        # Adiciona a entrada na tabela de diretório [cite: 13]
        self.directory_table[name] = first_block
        ui.print_success(f"Arquivo '{name}' criado (Início: Bloco {first_block}).")

    def read_file(self, name):
        """
        Lê o conteúdo de um arquivo do disco e o retorna[cite: 20].
        """
        if name not in self.directory_table:
            ui.print_error(f"Arquivo '{name}' não encontrado.")
            return None

        file_content = []
        current_block = self.directory_table[name]
        
        # Percorre a lista encadeada do arquivo [cite: 11]
        while current_block != self.disk.NULL_POINTER:
            data, next_block = self.disk.read(current_block)
            if data is None: break # Proteção
            
            file_content.append(data)
            current_block = next_block
        
        content_str = ''.join(file_content)
        ui.print_read_file(name, content_str)
        return content_str

    def delete_file(self, name):
        """
        Exclui um arquivo, liberando seus blocos.
        """
        ui.print_info(f"Tentando excluir '{name}'")
        if name not in self.directory_table:
            ui.print_error(f"Arquivo '{name}' não encontrado.")
            return
        
        current_block = self.directory_table[name]
        del self.directory_table[name]
        
        # Percorre a lista encadeada do arquivo e libera cada bloco
        while current_block != self.disk.NULL_POINTER:
            _data, next_block = self.disk.read(current_block)
            self._free_block(current_block)
            current_block = next_block
            
        ui.print_success(f"Arquivo '{name}' excluído.")