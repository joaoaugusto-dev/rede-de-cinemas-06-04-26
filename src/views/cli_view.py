from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
import time
import os

class PortugueseIntPrompt(IntPrompt):
    validate_error_message = "[bold red]Por favor, insira um número válido.[/bold red]"

class CLIView:
    def __init__(self, sessao_controller, filme_service, cinema_repo, sala_repo):
        self.console = Console()
        self.sessao_controller = sessao_controller
        self.filme_service = filme_service
        self.cinema_repo = cinema_repo
        self.sala_repo = sala_repo

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_splash(self):
        self.clear()
        self.console.print(Panel.fit(
            "[bold cyan]🎬 REDE DE CINEMAS - SISTEMA DE GESTÃO 🍿[/bold cyan]\n"
            "[italic]Engenharia de Software - 2026[/italic]",
            border_style="bright_blue"
        ))
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Carregando módulos...", total=None)
            time.sleep(1)
            progress.add_task(description="Conectando ao banco de dados...", total=None)
            time.sleep(0.5)

    def _ask_mandatory(self, message, default=None):
        while True:
            res = Prompt.ask(message, default=default)
            if res and res.strip():
                return res.strip()
            rprint("[bold red]Este campo é obrigatório e não pode conter apenas espaços.[/bold red]")

    def _ask_int(self, message, default=None):
        return PortugueseIntPrompt.ask(message, default=default)

    def main_menu(self):
        while True:
            self.clear()
            rprint(Panel("[bold yellow]Menu Principal[/bold yellow]", expand=False))
            rprint("[1] 🎥 Gerenciar Filmes")
            rprint("[2] 🏛️ Gerenciar Unidades (Cinemas/Salas)")
            rprint("[3] 🕒 Agendar Sessão")
            rprint("[4] 👥 Registrar Público")
            rprint("[5] 📊 Relatórios")
            rprint("[6] 📅 Consultar Programação")
            rprint("[7] 🔍 Detalhes de Filmes")
            rprint("[0] ❌ Sair")
            
            choice = Prompt.ask("\nSelecione uma opção", choices=["1", "2", "3", "4", "5", "6", "7", "0"])
            
            if choice == "1":
                self.gerenciar_filmes()
            elif choice == "2":
                self.gerenciar_unidades()
            elif choice == "3":
                self.agendar_sessao_flow()
            elif choice == "4":
                self.registrar_publico_flow()
            elif choice == "5":
                self.exibir_relatorios()
            elif choice == "6":
                self.consultar_programacao()
            elif choice == "7":
                self.consultar_detalhes_filme()
            elif choice == "0":
                rprint("[bold red]Saindo... Até logo![/bold red]")
                break

    def gerenciar_filmes(self):
        self.clear()
        rprint(Panel("[bold green]Listagem de Filmes[/bold green]"))
        
        filmes = self.filme_service.listar_filmes()
        if not filmes:
            rprint("[yellow]Nenhum filme cadastrado.[/yellow]")
        else:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("ID", style="dim", width=4)
            table.add_column("Título")
            table.add_column("Duração", justify="right")
            table.add_column("Gênero")
            table.add_column("Em Cartaz", justify="center")
            
            for f in filmes:
                table.add_row(
                    str(f.id), 
                    f.titulo, 
                    f"{f.duracao} min", 
                    f.genero, 
                    "[green]Sim[/green]" if f.em_cartaz else "[red]Não[/red]"
                )
            self.console.print(table)
            
        rprint("\n[A] Adicionar Filme | [M] Voltar")
        choice = Prompt.ask("Opção", choices=["A", "M"], default="M").upper()
        
        if choice == "A":
            titulo = self._ask_mandatory("Título do Filme")
            duracao = self._ask_int("Duração (minutos)")
            sinopse = Prompt.ask("Sinopse", default="").strip()
            elenco = Prompt.ask("Elenco", default="").strip()
            diretor = Prompt.ask("Diretor", default="").strip()
            genero = Prompt.ask("Gênero", default="").strip()
            
            self.filme_service.cadastrar_filme(titulo, duracao, sinopse, elenco, diretor, genero)
            rprint("[bold green]Filme cadastrado com sucesso![/bold green]")
            time.sleep(1.5)

    def gerenciar_unidades(self):
        self.clear()
        rprint(Panel("[bold blue]Gestão de Unidades e Salas[/bold blue]"))
        
        cinemas = self.cinema_repo.get_all()
        if not cinemas:
            rprint("[yellow]Nenhum cinema cadastrado.[/yellow]")
            if Prompt.ask("Deseja cadastrar um cinema agora?", choices=["S", "N"], default="S").upper() == "S":
                nome = self._ask_mandatory("Nome do Cinema")
                endereco = self._ask_mandatory("Endereço")
                cap = self._ask_int("Capacidade Total")
                self.cinema_repo.save(Cinema(None, nome, endereco, cap))
                rprint("[green]Cinema cadastrado![/green]")
                time.sleep(1)
            return

        table = Table(title="Cinemas Disponíveis")
        table.add_column("ID", style="dim")
        table.add_column("Nome")
        table.add_column("Endereço")
        ids_validos = []
        for c in cinemas:
            table.add_row(str(c.id), c.nome, c.endereco)
            ids_validos.append(c.id)
        self.console.print(table)
        
        rprint("\n[S] Adicionar Sala | [M] Voltar")
        choice = Prompt.ask("Opção", choices=["S", "M"], default="M").upper()
        
        if choice == "S":
            cinema_id = self._ask_int("ID do Cinema")
            if cinema_id not in ids_validos:
                rprint("[bold red]ID do Cinema inválido![/bold red]")
                time.sleep(1.5)
                return
                
            nome_sala = self._ask_mandatory("Nome/Número da Sala")
            cap_sala = self._ask_int("Capacidade da Sala")
            from src.models.entities import Sala
            self.sala_repo.save(Sala(None, cinema_id, nome_sala, cap_sala))
            rprint("[green]Sala adicionada![/green]")
            time.sleep(1)

    def agendar_sessao_flow(self):
        self.clear()
        rprint(Panel("[bold yellow]Agendamento de Sessão[/bold yellow]"))
        
        filmes = self.filme_service.listar_filmes()
        cinemas = self.cinema_repo.get_all()
        
        if not filmes or not cinemas:
            rprint("[red]Erro: É necessário ter filmes e cinemas cadastrados primeiro.[/red]")
            time.sleep(2)
            return
            
        rprint("[cyan]Filmes em Cartaz:[/cyan]")
        ids_filmes = []
        for f in filmes: 
            rprint(f"[{f.id}] {f.titulo}")
            ids_filmes.append(f.id)
            
        filme_id = self._ask_int("\nSelecione o ID do Filme")
        if filme_id not in ids_filmes:
            rprint("[bold red]Filme não encontrado![/bold red]")
            time.sleep(1.5)
            return
        
        rprint("\n[cyan]Cinemas:[/cyan]")
        ids_cinemas = []
        for c in cinemas: 
            rprint(f"[{c.id}] {c.nome}")
            ids_cinemas.append(c.id)
            
        cinema_id = self._ask_int("Selecione o ID do Cinema")
        if cinema_id not in ids_cinemas:
            rprint("[bold red]Cinema não encontrado![/bold red]")
            time.sleep(1.5)
            return
        
        salas = self.sala_repo.get_by_cinema(cinema_id)
        if not salas:
            rprint("[red]Este cinema não possui salas cadastradas.[/red]")
            time.sleep(2)
            return
            
        rprint("\n[cyan]Salas:[/cyan]")
        ids_salas = []
        for s in salas: 
            rprint(f"[{s.id}] {s.nome} (Capacidade: {s.capacidade})")
            ids_salas.append(s.id)
            
        sala_id = self._ask_int("Selecione o ID da Sala")
        if sala_id not in ids_salas:
            rprint("[bold red]Sala não encontrada![/bold red]")
            time.sleep(1.5)
            return
        
        data_str = Prompt.ask("Data e Hora (Formato: YYYY-MM-DD HH:MM)", default=datetime.now().strftime("%Y-%m-%d %H:%M")).strip()
        # Ajustar formato para ISO
        try:
            iso_data = datetime.strptime(data_str, "%Y-%m-%d %H:%M").isoformat()
            result = self.sessao_controller.agendar_sessao(sala_id, filme_id, iso_data)
            
            if result["status"] == "sucesso":
                rprint(f"[bold green]{result['message']}[/bold green]")
                s = result["data"]
                rprint(f"Término estimado: [bold]{s.data_hora_fim.strftime('%H:%M')}[/bold] (incluindo trailers)")
            else:
                rprint(f"[bold red]ERRO: {result['message']}[/bold red]")
        except Exception:
            rprint("[red]Formato de data inválido! Use YYYY-MM-DD HH:MM[/red]")
            
        Prompt.ask("\nPressione Enter para continuar")

    def registrar_publico_flow(self):
        self.clear()
        rprint(Panel("[bold magenta]Registro de Público[/bold magenta]"))
        
        sessoes = self.sessao_controller.sessao_service.sessao_repo.get_all()
        if not sessoes:
            rprint("[yellow]Nenhuma sessão agendada.[/yellow]")
            time.sleep(2)
            return
            
        table = Table(title="Sessões Realizadas/Agendadas")
        table.add_column("ID", style="dim")
        table.add_column("Filme")
        table.add_column("Horário")
        table.add_column("Público")
        
        ids_sessoes = []
        for s in sessoes:
            filme = self.filme_service.filme_repo.get_by_id(s.filme_id)
            table.add_row(
                str(s.id), 
                filme.titulo if filme else "Desconhecido", 
                s.data_hora_inicio.strftime("%d/%m %H:%M"),
                str(s.publico_registrado)
            )
            ids_sessoes.append(s.id)
        self.console.print(table)
        
        sessao_id = self._ask_int("\nID da Sessão para registrar público")
        if sessao_id not in ids_sessoes:
            rprint("[bold red]Sessão não encontrada![/bold red]")
            time.sleep(1.5)
            return
            
        publico = self._ask_int("Quantidade de público presente")
        
        result = self.sessao_controller.registrar_publico(sessao_id, publico)
        if result["status"] == "sucesso":
            rprint("[bold green]Sucesso![/bold green]")
        else:
            rprint(f"[bold red]Erro: {result['message']}[/bold red]")
        
        time.sleep(2)

    def exibir_relatorios(self):
        self.clear()
        rprint(Panel("[bold yellow]📊 Relatórios Analíticos[/bold yellow]"))
        
        sessoes = self.sessao_controller.sessao_service.sessao_repo.get_all()
        
        total_publico = sum(s.publico_registrado for s in sessoes)
        
        rprint(f"\n[bold]Total de Público na Rede:[/bold] [green]{total_publico}[/green] pessoas")
        
        # Agrupar por filme (simplificado)
        publico_por_filme = {}
        for s in sessoes:
            filme = self.filme_service.filme_repo.get_by_id(s.filme_id)
            nome = filme.titulo if filme else "Outros"
            publico_por_filme[nome] = publico_por_filme.get(nome, 0) + s.publico_registrado
            
        table = Table(title="Público por Filme")
        table.add_column("Filme")
        table.add_column("Total Público", justify="right")
        
        for nome, total in publico_por_filme.items():
            table.add_row(nome, str(total))
            
        self.console.print(table)
        Prompt.ask("\nPressione Enter para voltar")

    def consultar_programacao(self):
        self.clear()
        rprint(Panel("[bold cyan]📅 Programação de Sessões[/bold cyan]"))
        
        cinemas = self.cinema_repo.get_all()
        if not cinemas:
            rprint("[yellow]Nenhum cinema cadastrado.[/yellow]")
            time.sleep(1.5)
            return

        rprint("Escolha o cinema para ver a programação:")
        for c in cinemas: rprint(f"[{c.id}] {c.nome}")
        rprint("[0] Ver todas as sessões")
        
        cinema_id = self._ask_int("\nSelecione o ID")
        
        sessoes = self.sessao_controller.sessao_service.sessao_repo.get_all()
        
        table = Table(title=f"Programação")
        table.add_column("Cinema/Sala", style="dim")
        table.add_column("Filme", style="bold")
        table.add_column("Início", justify="center")
        table.add_column("Término", justify="center")
        
        found = False
        for s in sessoes:
            sala = self.sala_repo.get_by_id(s.sala_id)
            cinema = self.cinema_repo.get_by_id(sala.cinema_id)
            
            if cinema_id != 0 and cinema.id != cinema_id:
                continue
                
            filme = self.filme_service.filme_repo.get_by_id(s.filme_id)
            table.add_row(
                f"{cinema.nome}\n{sala.nome}",
                filme.titulo,
                s.data_hora_inicio.strftime("%d/%m %H:%M"),
                s.data_hora_fim.strftime("%H:%M")
            )
            found = True
            
        if not found:
            rprint("[yellow]Nenhuma sessão encontrada para os critérios selecionados.[/yellow]")
        else:
            self.console.print(table)
            
        Prompt.ask("\nPressione Enter para voltar")

    def consultar_detalhes_filme(self):
        self.clear()
        rprint(Panel("[bold magenta]🔍 Detalhes de Filmes[/bold magenta]"))
        
        filmes = self.filme_service.listar_filmes()
        if not filmes:
            rprint("[yellow]Nenhum filme cadastrado.[/yellow]")
            time.sleep(1.5)
            return
            
        for f in filmes: rprint(f"[{f.id}] {f.titulo}")
        
        filme_id = self._ask_int("\nSelecione o ID do filme para ver detalhes")
        
        filme = self.filme_service.filme_repo.get_by_id(filme_id)
        if not filme:
            rprint("[bold red]Filme não encontrado![/bold red]")
        else:
            self.clear()
            detail_panel = Panel(
                f"[bold cyan]Título:[/bold cyan] {filme.titulo}\n"
                f"[bold cyan]Gênero:[/bold cyan] {filme.genero} | [bold cyan]Duração:[/bold cyan] {filme.duracao} min\n"
                f"[bold cyan]Diretor:[/bold cyan] {filme.diretor}\n"
                f"[bold cyan]Elenco:[/bold cyan] {filme.elenco}\n\n"
                f"[bold cyan]Sinopse:[/bold cyan]\n{filme.sinopse}",
                title=f"Ficha Técnica - ID {filme.id}",
                border_style="magenta"
            )
            self.console.print(detail_panel)
            
        Prompt.ask("\nPressione Enter para voltar")

from src.models.entities import Cinema, Sala, Filme, Sessao
from datetime import datetime
