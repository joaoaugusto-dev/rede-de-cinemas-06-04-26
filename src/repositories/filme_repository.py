from src.repositories.base_repository import BaseRepository
from src.models.entities import Filme

class FilmeRepository(BaseRepository):
    def save(self, filme: Filme):
        query = '''
            INSERT INTO filmes (titulo, duracao, sinopse, elenco, diretor, genero, em_cartaz)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        params = (filme.titulo, filme.duracao, filme.sinopse, filme.elenco, filme.diretor, filme.genero, 1 if filme.em_cartaz else 0)
        cursor = self.execute(query, params)
        filme.id = cursor.lastrowid
        return filme

    def get_all(self):
        query = "SELECT * FROM filmes"
        rows = self.fetch_all(query)
        return [Filme(id=r[0], titulo=r[1], duracao=r[2], sinopse=r[3], elenco=r[4], diretor=r[5], genero=r[6], em_cartaz=bool(r[7])) for r in rows]

    def get_by_id(self, filme_id):
        query = "SELECT * FROM filmes WHERE id = ?"
        row = self.fetch_one(query, (filme_id,))
        if row:
            return Filme(id=row[0], titulo=row[1], duracao=row[2], sinopse=row[3], elenco=row[4], diretor=row[5], genero=row[6], em_cartaz=bool(row[7]))
        return None
