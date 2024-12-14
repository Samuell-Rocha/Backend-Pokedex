from pydantic import BaseModel, Field
from typing import Optional, List
from model.pokemon import Pokemon

class PokemonSchema(BaseModel):
    """Define como um novo Pokemon a ser inserido deve ser representado."""
    nome: str = "Banana Prata"
    tipo: str = "Água"
    nivel: Optional[int] = 3
    foto: Optional[str] = None
    audio: Optional[str] = None 

class PokemonBuscaSchema(BaseModel):
    """Define a estrutura para busca de um Pokemon com base no nome."""
    nome: str

class ListagemPokemonsSchema(BaseModel):
    """Define como uma listagem de Pokemons será retornada."""
    pokemons: List[PokemonSchema]

def apresenta_pokemons(pokemons: List[Pokemon]):
    """Retorna uma representação dos Pokemons seguindo o schema definido."""
    return {
        "pokemons": [
            {
                "nome": pokemon.nome,
                "tipo": pokemon.tipo,
                "nivel": pokemon.nivel,
                "foto": pokemon.foto,
                "audio": pokemon.audio
            } for pokemon in pokemons
        ]
    }

class PokemonViewSchema(BaseModel):
    """Define como um Pokemon será retornado."""
    id: int = 1
    nome: str = "Squirtle"
    tipo: str = "Água"
    nivel: Optional[int] = 1
    foto: str = "test"
    audio: str = "squirtle"

class PokemonDelSchema(BaseModel):
    """Define a estrutura do dado retornado após uma requisição de remoção."""
    message: str
    nome: str

def apresenta_pokemon(pokemon: Pokemon):
    """Retorna uma representação do Pokemon seguindo o schema definido."""
    return {
        "id": pokemon.id,
        "nome": pokemon.nome,
        "tipo": pokemon.tipo,
        "nivel": pokemon.nivel,
        "foto": pokemon.foto,
        "audio": pokemon.audio
    }
