from filesystem import FileSystem
import ui
import time

def run_demo():
    """
    Executa a sequência de demonstração exata descrita no documento PDF.
    """
    fs = FileSystem()
    
    ui.print_step("ESTADO INICIAL (DISCO VAZIO)")
    ui.print_directory(fs)
    ui.print_free_list(fs)
    time.sleep(2)

    # 1. Adicionar "arquivos" 1, 2 e 3
    ui.print_step("1. Adicionando 3 arquivos")
    fs.create_file("f1", "Pernambuco") # 10 blocos
    fs.create_file("f2", "Sao Paulo")  # 9 blocos
    fs.create_file("f3", "Alagoas")    # 7 blocos
    
    print("\n")
    ui.print_disk_status(fs)
    ui.print_directory(fs)
    ui.print_free_list(fs)
    time.sleep(2)

    # 2. Tentar adicionar "Santa Catarina" (deve falhar)
    # (Req: 14 blocos, Disp: 32 - (10+9+7) = 6 blocos)
    ui.print_step("2. Tentando adicionar 'Santa Catarina' (14 blocos) - Deve falhar")
    # [cite_start]Esta é a linha que foi corrigida (removido o [cite: 30])
    fs.create_file("f4", "Santa Catarina")
    time.sleep(2)

    # 3. Ler arquivos existentes
    ui.print_step("3. Lendo arquivos existentes")
    fs.read_file("f1")
    fs.read_file("f2")
    fs.read_file("f3")
    time.sleep(2)

    # 4. Excluir o "arquivo" Sao Paulo
    ui.print_step("4. Excluindo 'Sao Paulo' (f2) - Libera 9 blocos")
    fs.delete_file("f2") # Libera 9 blocos
    
    # Espaço livre agora: 6 (anteriores) + 9 (liberados) = 15 blocos.
    # A lista livre agora está fragmentada.
    
    print("\n")
    ui.print_disk_status(fs)
    ui.print_directory(fs)
    ui.print_free_list(fs)
    time.sleep(2)

    # 5. Adicionar "arquivo" Santa Catarina (agora deve funcionar)
    # (Req: 14 blocos, Disp: 15 blocos)
    ui.print_step("5. Tentando adicionar 'Santa Catarina' (14 blocos) novamente")
    fs.create_file("f4", "Santa Catarina")
    
    print("\n")
    ui.print_disk_status(fs)
    ui.print_directory(fs)
    ui.print_free_list(fs)
    time.sleep(2)
    
    ui.print_step("6. Lendo arquivos finais para confirmar")
    fs.read_file("f1")
    fs.read_file("f3")
    fs.read_file("f4") # Confirma a leitura do arquivo fragmentado
    
    ui.print_step("DEMONSTRAÇÃO CONCLUÍDA")


if __name__ == "__main__":
    try:
        run_demo()
    except ImportError:
        ui.print_error("Biblioteca 'rich' não encontrada.")
        ui.print_info("Por favor, instale as dependências com: pip install -r requirements.txt")
    except KeyboardInterrupt:
        ui.print_info("\nSimulação interrompida pelo usuário.")