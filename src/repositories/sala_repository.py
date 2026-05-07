from src.repositories.base_repository import BaseRepository
from src.models.entities import Sala

class SalaRepository(BaseRepository):
    def save(self, sala: Sala):
        query = "INSERT INTO salas (cinema_id, nome, capacidade) VALUES (?, ?, ?)"
        cursor = self.execute(query, (sala.cinema_id, sala.nome, sala.capacidade))
        sala.id = cursor.lastrowid
        return sala

    def get_by_cinema(self, cinema_id):
        query = "SELECT * FROM salas WHERE cinema_id = ?"
        rows = self.fetch_all(query, (cinema_id,))
        return [Sala(id=r[0], cinema_id=r[1], nome=r[2], capacidade=r[3]) for r in rows]

    def get_by_id(self, sala_id):
        query = "SELECT * FROM salas WHERE id = ?"
        row = self.fetch_one(query, (sala_id,))
        if row:
            return Sala(id=row[0], cinema_id=row[1], nome=row[2], capacidade=row[3])
        return None
