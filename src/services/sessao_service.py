from datetime import timedelta
from src.models.entities import Sessao, Filme, Sala
from src.repositories.sessao_repository import SessaoRepository
from src.repositories.filme_repository import FilmeRepository
from src.repositories.sala_repository import SalaRepository

class SessaoService:
    def __init__(self, sessao_repo: SessaoRepository, filme_repo: FilmeRepository, sala_repo: SalaRepository):
        self.sessao_repo = sessao_repo
        self.filme_repo = filme_repo
        self.sala_repo = sala_repo

    def agendar_sessao(self, sala_id, filme_id, data_hora_inicio):
        filme = self.filme_repo.get_by_id(filme_id)
        if not filme:
            raise ValueError("Filme não encontrado.")
        
        if not filme.em_cartaz:
            raise ValueError("O filme não está em cartaz (RN06).")

        # RN03: Calcular término (Duração + 10 min trailers)
        duracao_total = filme.duracao + 10
        data_hora_fim = data_hora_inicio + timedelta(minutes=duracao_total)

        # Validar conflitos
        self.validar_conflitos(sala_id, data_hora_inicio, data_hora_fim)

        sessao = Sessao(
            id=None,
            sala_id=sala_id,
            filme_id=filme_id,
            data_hora_inicio=data_hora_inicio,
            data_hora_fim=data_hora_fim
        )
        return self.sessao_repo.save(sessao)

    def validar_conflitos(self, sala_id, inicio, fim):
        # RN01 e RN02: Sobreposição e Intervalo de 20 min
        sessoes_dia = self.sessao_repo.get_by_sala_and_day(sala_id, inicio.date().isoformat())
        
        intervalo = timedelta(minutes=20)
        
        for s in sessoes_dia:
            # Sessão existente: [s.inicio, s.fim]
            # Nova sessão: [inicio, fim]
            # Com intervalo: [s.inicio - 20min, s.fim + 20min]
            
            # Se o início da nova sessão for antes do fim da existente + 20min
            # E o fim da nova sessão for depois do início da existente - 20min
            # Então há conflito
            if inicio < (s.data_hora_fim + intervalo) and fim > (s.data_hora_inicio - intervalo):
                raise ValueError(f"Conflito de horário! A sala já possui uma sessão das {s.data_hora_inicio.strftime('%H:%M')} às {s.data_hora_fim.strftime('%H:%M')}. (RN01/RN02)")

    def registrar_publico(self, sessao_id, publico):
        sessao = self.sessao_repo.fetch_one("SELECT * FROM sessoes WHERE id = ?", (sessao_id,))
        if not sessao:
            raise ValueError("Sessão não encontrada.")
        
        # Obter capacidade da sala
        sala = self.sala_repo.get_by_id(sessao[1])
        if publico > sala.capacidade:
            raise ValueError(f"Capacidade máxima da sala excedida ({sala.capacidade}). (RN04)")
            
        self.sessao_repo.update_publico(sessao_id, publico)
        return True
