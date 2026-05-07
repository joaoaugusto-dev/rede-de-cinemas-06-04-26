from src.repositories.base_repository import BaseRepository
from src.models.entities import Cinema

class CinemaRepository(BaseRepository):
    def save(self, cinema: Cinema):
        query = "INSERT INTO cinemas (nome, endereco, capacidade_total) VALUES (?, ?, ?)"
        cursor = self.execute(query, (cinema.nome, cinema.endereco, cinema.capacidade_total))
        cinema.id = cursor.lastrowid
        return cinema

    def get_all(self):
        query = "SELECT * FROM cinemas"
        rows = self.fetch_all(query)
        return [Cinema(id=r[0], nome=r[1], endereco=r[2], capacidade_total=r[3]) for r in rows]

    def get_by_id(self, cinema_id):
        query = "SELECT * FROM cinemas WHERE id = ?"
        row = self.fetch_one(query, (cinema_id,))
        if row:
            return Cinema(id=row[0], nome=row[1], endereco=row[2], capacidade_total=row[3])
        return None
