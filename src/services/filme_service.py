from src.models.entities import Filme
from src.repositories.filme_repository import FilmeRepository

class FilmeService:
    def __init__(self, filme_repo: FilmeRepository):
        self.filme_repo = filme_repo

    def cadastrar_filme(self, titulo, duracao, sinopse, elenco, diretor, genero):
        filme = Filme(None, titulo, duracao, sinopse, elenco, diretor, genero)
        return self.filme_repo.save(filme)

    def listar_filmes(self):
        return self.filme_repo.get_all()
