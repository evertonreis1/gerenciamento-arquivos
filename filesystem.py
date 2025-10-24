from disk import Disk
import ui


class FileSystem:
    def __init__(self):
        self.disk = Disk()

        self.directory_table = {}

        self.free_list_head = 0
        self.free_space_size = self.disk.DISK_SIZE

        self.disk.initialize_free_list()

    def _allocate_block(self):
        if self.free_list_head == self.disk.NULL_POINTER:
            return self.disk.NULL_POINTER

        allocated_block_index = self.free_list_head

        _data, next_free_block = self.disk.read(allocated_block_index)

        self.free_list_head = next_free_block
        self.free_space_size -= 1

        self.disk.write(allocated_block_index, '\0', self.disk.NULL_POINTER)

        return allocated_block_index

    def _free_block(self, block_index):
        self.disk.clear_block_data(block_index)

        self.disk.write(block_index, '\0', self.free_list_head)
        self.free_list_head = block_index
        self.free_space_size += 1

    def create_file(self, name, content):
        ui.print_info(f"Tentando criar '{name}' (Tamanho: {len(content)})")

        if len(name) > 4:
            ui.print_error(f"Nome '{name}' excede 4 caracteres.")
            return

        if name in self.directory_table:
            ui.print_error(f"Arquivo '{name}' já existe.")
            return

        if len(content) > self.free_space_size:
            ui.print_error(
                f"Memória insuficiente. (Req: {len(content)}, Disp: {self.free_space_size})")
            return

        if len(content) == 0:
            ui.print_error("Conteúdo do arquivo não pode ser vazio.")
            return

        prev_block = self.disk.NULL_POINTER
        first_block = self.disk.NULL_POINTER

        for char in content:
            current_block = self._allocate_block()

            self.disk.write(current_block, char, self.disk.NULL_POINTER)

            if first_block == self.disk.NULL_POINTER:
                first_block = current_block

            if prev_block != self.disk.NULL_POINTER:
                _data, _ptr = self.disk.read(prev_block)
                self.disk.write(prev_block, _data, current_block)

            prev_block = current_block

        self.directory_table[name] = first_block
        ui.print_success(
            f"Arquivo '{name}' criado (Início: Bloco {first_block}).")

    def read_file(self, name):
        if name not in self.directory_table:
            ui.print_error(f"Arquivo '{name}' não encontrado.")
            return None

        file_content = []
        current_block = self.directory_table[name]

        while current_block != self.disk.NULL_POINTER:
            data, next_block = self.disk.read(current_block)
            if data is None:
                break

            file_content.append(data)
            current_block = next_block

        content_str = ''.join(file_content)
        ui.print_read_file(name, content_str)
        return content_str

    def delete_file(self, name):
        ui.print_info(f"Tentando excluir '{name}'")
        if name not in self.directory_table:
            ui.print_error(f"Arquivo '{name}' não encontrado.")
            return

        current_block = self.directory_table[name]
        del self.directory_table[name]

        while current_block != self.disk.NULL_POINTER:
            _data, next_block = self.disk.read(current_block)
            self._free_block(current_block)
            current_block = next_block

        ui.print_success(f"Arquivo '{name}' excluído.")
