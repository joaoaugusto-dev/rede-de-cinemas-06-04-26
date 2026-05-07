from src.database.database_manager import DatabaseManager
from src.repositories.filme_repository import FilmeRepository
from src.repositories.cinema_repository import CinemaRepository
from src.repositories.sala_repository import SalaRepository
from src.repositories.sessao_repository import SessaoRepository
from src.services.filme_service import FilmeService
from src.services.sessao_service import SessaoService
from src.controllers.sessao_controller import SessaoController
from src.views.cli_view import CLIView

def main():
    # Inicialização das camadas
    db_manager = DatabaseManager("cinema.db")
    
    # Repositories
    filme_repo = FilmeRepository(db_manager)
    cinema_repo = CinemaRepository(db_manager)
    sala_repo = SalaRepository(db_manager)
    sessao_repo = SessaoRepository(db_manager)
    
    # Services
    filme_service = FilmeService(filme_repo)
    sessao_service = SessaoService(sessao_repo, filme_repo, sala_repo)
    
    # Controllers
    sessao_controller = SessaoController(sessao_service)
    
    # View
    view = CLIView(sessao_controller, filme_service, cinema_repo, sala_repo)
    
    # Execução
    view.show_splash()
    view.main_menu()

if __name__ == "__main__":
    main()
