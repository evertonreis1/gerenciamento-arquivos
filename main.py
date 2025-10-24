from filesystem import FileSystem
import ui
from rich.console import Console
from rich.panel import Panel
import time


def print_menu():
    console = Console()
    menu_text = """
[bold cyan]Gerenciador de Arquivos (Alocação Encadeada)[/bold cyan]

1. Criar Arquivo
2. Ler Arquivo
3. Excluir Arquivo
4. Mostrar Tabela de Diretório
5. Mostrar Lista de Blocos Livres
6. Mostrar Disco Completo
7. Sair
"""
    console.print(Panel(menu_text, title="Menu Principal",
                  width=60, border_style="blue"))

    try:
        choice = console.input("[bold]Escolha uma opção (1-7): [/bold]")
        return choice
    except EOFError:
        return '7'
    except KeyboardInterrupt:
        return '7'


def main_interactive():
    fs = FileSystem()
    console = Console()

    ui.print_step("SISTEMA DE ARQUIVOS INICIADO")
    ui.print_info(f"Disco de {fs.disk.DISK_SIZE} blocos inicializado.")
    ui.print_free_list(fs)
    console.print("\n")

    while True:
        choice = print_menu()
        console.print("\n")

        if choice == '1':
            ui.print_step("1. Criar Arquivo")
            name = input("Nome do arquivo (max 4 chars): ").strip()
            content = input("Conteúdo (palavra): ").strip()

            if not name or not content:
                ui.print_error("Nome e conteúdo não podem ser vazios.")
            else:
                fs.create_file(name, content)

        elif choice == '2':
            ui.print_step("2. Ler Arquivo")
            name = input("Nome do arquivo para ler: ").strip()
            if not name:
                ui.print_error("Nome não pode ser vazio.")
            else:
                fs.read_file(name)

        elif choice == '3':
            ui.print_step("3. Excluir Arquivo")
            name = input("Nome do arquivo para excluir: ").strip()
            if not name:
                ui.print_error("Nome não pode ser vazio.")
            else:
                fs.delete_file(name)

        elif choice == '4':
            ui.print_step("4. Tabela de Diretório")
            ui.print_directory(fs)

        elif choice == '5':
            ui.print_step("5. Lista de Blocos Livres")
            ui.print_free_list(fs)

        elif choice == '6':
            ui.print_step("6. Status do Disco Completo")
            ui.print_disk_status(fs)

        elif choice == '7':
            ui.print_info("Encerrando o sistema. Até logo!")
            break

        else:
            ui.print_error("Opção inválida. Por favor, escolha de 1 a 7.")

        console.input("\n[dim]Pressione Enter para continuar...[/dim]")
        console.clear()


if __name__ == "__main__":
    try:
        main_interactive()
    except ImportError:
        print("Erro: Biblioteca 'rich' não encontrada.")
        print("Por favor, instale com: pip install rich")
    except KeyboardInterrupt:
        print("\nSimulação interrompida pelo usuário.")
