from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Cinema:
    id: Optional[int]
    nome: str
    endereco: str
    capacidade_total: int

@dataclass
class Sala:
    id: Optional[int]
    cinema_id: int
    nome: str
    capacidade: int

@dataclass
class Filme:
    id: Optional[int]
    titulo: str
    duracao: int
    sinopse: str
    elenco: str
    diretor: str
    genero: str
    em_cartaz: bool = True

@dataclass
class Sessao:
    id: Optional[int]
    sala_id: int
    filme_id: int
    data_hora_inicio: datetime
    data_hora_fim: datetime
    publico_registrado: int = 0
