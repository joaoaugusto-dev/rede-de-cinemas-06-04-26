from src.services.sessao_service import SessaoService
from datetime import datetime

class SessaoController:
    def __init__(self, sessao_service: SessaoService):
        self.sessao_service = sessao_service

    def agendar_sessao(self, sala_id, filme_id, data_hora_str):
        try:
            data_hora = datetime.fromisoformat(data_hora_str)
            sessao = self.sessao_service.agendar_sessao(sala_id, filme_id, data_hora)
            return {"status": "sucesso", "data": sessao, "message": "Sessão agendada com sucesso!"}
        except Exception as e:
            return {"status": "erro", "message": str(e)}

    def registrar_publico(self, sessao_id, publico):
        try:
            self.sessao_service.registrar_publico(sessao_id, publico)
            return {"status": "sucesso", "message": "Público registrado com sucesso!"}
        except Exception as e:
            return {"status": "erro", "message": str(e)}
