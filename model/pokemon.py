from sqlalchemy import Column, String, Integer

from  model import Base

class Pokemon(Base):
    __tablename__ = 'pokemon'

    id = Column("pk_pokemon", Integer, primary_key=True)
    nome = Column(String(80), unique=True)
    tipo = Column(String(50))
    nivel = Column(Integer)
    foto = Column(String(255))
    audio = Column(String(255))

    # Definição do relacionamento entre o pokemon e o comentário.
    # Essa relação é implicita, não está salva na tabela 'pokemon',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.

    def __init__(self, nome:str, tipo:str, nivel:int,
        foto:str, audio:str):
        """
        Cria um pokemon

        Arguments:
            nome: Nome do pokemon.
            tipo:  Categorias que classificam cada pokemon com base em suas características elementares e habilidades naturais
            nivel: Crescimento e a força de um pokemon conforme ele é treinado.
            foto: Foto do pokemon
            audio: Descrição pokemon
        """
        self.nome = nome
        self.tipo = tipo
        self.nivel = nivel
        self.foto = foto
        self.audio = audio
