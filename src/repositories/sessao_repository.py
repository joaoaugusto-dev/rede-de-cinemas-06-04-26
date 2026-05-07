from src.repositories.base_repository import BaseRepository
from src.models.entities import Sessao
from datetime import datetime

class SessaoRepository(BaseRepository):
    def save(self, sessao: Sessao):
        query = '''
            INSERT INTO sessoes (sala_id, filme_id, data_hora_inicio, data_hora_fim, publico_registrado)
            VALUES (?, ?, ?, ?, ?)
        '''
        params = (
            sessao.sala_id, 
            sessao.filme_id, 
            sessao.data_hora_inicio.isoformat(), 
            sessao.data_hora_fim.isoformat(), 
            sessao.publico_registrado
        )
        cursor = self.execute(query, params)
        sessao.id = cursor.lastrowid
        return sessao

    def get_by_sala_and_day(self, sala_id, day_str):
        query = "SELECT * FROM sessoes WHERE sala_id = ? AND date(data_hora_inicio) = ?"
        rows = self.fetch_all(query, (sala_id, day_str))
        return [self._map_row_to_sessao(r) for r in rows]

    def _map_row_to_sessao(self, row):
        return Sessao(
            id=row[0],
            sala_id=row[1],
            filme_id=row[2],
            data_hora_inicio=datetime.fromisoformat(row[3]),
            data_hora_fim=datetime.fromisoformat(row[4]),
            publico_registrado=row[5]
        )

    def get_all(self):
        query = "SELECT * FROM sessoes"
        rows = self.fetch_all(query)
        return [self._map_row_to_sessao(r) for r in rows]
        
    def update_publico(self, sessao_id, publico):
        query = "UPDATE sessoes SET publico_registrado = ? WHERE id = ?"
        self.execute(query, (publico, sessao_id))
