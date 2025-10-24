from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def print_step(title):
    console.rule(f"[bold cyan]{title}[/bold cyan]", style="cyan")


def print_info(message):
    console.print(f"ℹ️  [blue]Info:[/blue] {message}")


def print_success(message):
    console.print(f"✅ [bold green]Sucesso:[/bold green] {message}")


def print_error(message):
    console.print(f"❌ [bold red]Erro:[/bold red] {message}")


def print_read_file(name, content):
    console.print(
        f"📖 [bold]Leitura de '[yellow]{name}[/yellow]':[/bold] \"{content}\"")


def print_disk_status(fs):
    table = Table(title="💿 Status Atual do Disco",
                  title_style="bold magenta", padding=0)
    table.add_column("Bloco", style="dim", justify="right")
    table.add_column("Data", justify="center")
    table.add_column("Ponteiro", justify="right")

    for i in range(fs.disk.DISK_SIZE):
        data, pointer = fs.disk.read(i)

        data_repr = f"'{data}'" if data != '\0' else "[dim]''[/dim]"

        pointer_repr = f"[red]NULL[/red]" if pointer == fs.disk.NULL_POINTER else str(
            pointer)

        style = "on #333333" if data != '\0' else ""

        table.add_row(str(i), data_repr, pointer_repr, style=style)

    console.print(table)


def print_directory(fs):
    table = Table(title="🗂️  Tabela de Diretório", title_style="bold")
    table.add_column("Nome (Arquivo)", style="yellow")
    table.add_column("Bloco Inicial", style="cyan")

    if not fs.directory_table:
        table.add_row("[dim](Vazia)[/dim]", "")
    else:
        for name, start in fs.directory_table.items():
            table.add_row(name, str(start))

    console.print(table)


def print_free_list(fs):
    panel_content = f"[bold]Espaço Livre Total:[/bold] {fs.free_space_size} blocos\n"
    panel_content += f"[bold]Início da Lista (Head):[/bold] {fs.free_list_head}\n\n"

    nodes = []
    current_block = fs.free_list_head
    count_limit = 0

    while current_block != fs.disk.NULL_POINTER and count_limit <= fs.disk.DISK_SIZE:
        nodes.append(str(current_block))
        _data, next_block = fs.disk.read(current_block)
        current_block = next_block
        count_limit += 1

    if not nodes:
        panel_content += "[bold]Cadeia de Livres:[/bold] [dim](Nenhum)[/dim]"
    else:
        panel_content += "[bold]Cadeia de Livres:[/bold] " + \
            " -> ".join(nodes) + " -> [red]NULL[/red]"

    console.print(
        Panel(panel_content, title="📉 Lista de Blocos Livres", border_style="green"))
