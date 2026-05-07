import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="cinema.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Table: Cinemas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cinemas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    endereco TEXT NOT NULL,
                    capacidade_total INTEGER NOT NULL
                )
            ''')
            
            # Table: Salas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS salas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cinema_id INTEGER NOT NULL,
                    nome TEXT NOT NULL,
                    capacidade INTEGER NOT NULL,
                    FOREIGN KEY (cinema_id) REFERENCES cinemas (id)
                )
            ''')
            
            # Table: Filmes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS filmes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    duracao INTEGER NOT NULL,
                    sinopse TEXT,
                    elenco TEXT,
                    diretor TEXT,
                    genero TEXT,
                    em_cartaz BOOLEAN DEFAULT 1
                )
            ''')
            
            # Table: Sessoes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sala_id INTEGER NOT NULL,
                    filme_id INTEGER NOT NULL,
                    data_hora_inicio DATETIME NOT NULL,
                    data_hora_fim DATETIME NOT NULL,
                    publico_registrado INTEGER DEFAULT 0,
                    FOREIGN KEY (sala_id) REFERENCES salas (id),
                    FOREIGN KEY (filme_id) REFERENCES filmes (id)
                )
            ''')
            
            conn.commit()

if __name__ == "__main__":
    db = DatabaseManager()
    print("Banco de dados inicializado com sucesso.")
