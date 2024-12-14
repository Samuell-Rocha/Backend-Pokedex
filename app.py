from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request, jsonify, send_from_directory
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
import os
from model import Session, Pokemon
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
pokemon_tag = Tag(name="Pokemon", description="Adição, visualização e Remoção de pokemons à base")

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__))) 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp3', 'wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

print("Caminho do diretório de uploads:", app.config['UPLOAD_FOLDER'])


if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')

@app.post('/pokemon', tags=[pokemon_tag],
          responses={"200": PokemonViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_pokemon():
    """Adiciona um novo pokemon à base de dados e retorna sua representação."""
    # Pegando os campos do formulário
    nome = request.form.get('nome')
    tipo = request.form.get('tipo')
    nivel = request.form.get('nivel', type=int)
    foto = request.form.get('foto')  # Recebe o nome do arquivo ou caminho
    audio = request.form.get('audio')
    
    # Tratando upload de arquivos
    foto_file = request.files.get('foto')
    audio_file = request.files.get('audio')

    foto_path = None
    audio_path = None

    if foto_file and allowed_file(foto_file.filename):
        foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto_file.filename)
        foto_file.save(foto_path)

    if audio_file and allowed_file(audio_file.filename):
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
        audio_file.save(audio_path)

    # Validando os campos obrigatórios
    if not nome or not tipo:
        return jsonify({"error": "Campos 'nome' e 'tipo' são obrigatórios"}), 400

    # Criando o objeto Pokémon
    pokemon = Pokemon(nome=nome, tipo=tipo, nivel=nivel, foto=foto_file.filename, audio=audio_file.filename)
    
    try:
        session = Session()
        session.add(pokemon)
        session.commit()
        return apresenta_pokemon(pokemon), 200
    except IntegrityError:
        return {"message": "Pokemon já existe na base"}, 409
    except Exception as e:
        return {"message": f"Erro inesperado: {e}"}, 400

@app.get('/pokemons', tags=[pokemon_tag],
         responses={"200": ListagemPokemonsSchema, "404": ErrorSchema})
def get_pokemons():
    """Busca todos os pokemons cadastrados e retorna sua listagem."""
    logger.debug("Coletando pokemons")
    session = Session()
    pokemons = session.query(Pokemon).all()
    if not pokemons:
        return {"pokemons": []}, 200
    logger.debug(f"{len(pokemons)} pokemons encontrados")
    return apresenta_pokemons(pokemons), 200

@app.get('/pokemon', tags=[pokemon_tag],
         responses={"200": PokemonViewSchema, "404": ErrorSchema})
def get_pokemon(query: PokemonBuscaSchema):
    """Busca um pokemon pelo nome e retorna sua representação."""
    logger.debug(f"Coletando dados sobre pokemon '{query.nome}'")
    session = Session()
    pokemon = session.query(Pokemon).filter(Pokemon.nome == query.nome).first()
    if not pokemon:
        logger.warning(f"Pokemon '{query.nome}' não encontrado na base.")
        return {"mesage": "Pokemon não encontrado na base :/"}, 404
    logger.debug(f"Pokemon encontrado: '{pokemon.nome}'")
    return apresenta_pokemon(pokemon), 200

@app.delete('/pokemon', tags=[pokemon_tag],
            responses={"200": PokemonDelSchema, "404": ErrorSchema})
def del_pokemon(query: PokemonBuscaSchema):
    """Deleta um pokemon pelo nome e retorna mensagem de confirmação."""
    print("ok", query)
    pokemon_nome = query.nome.strip()
    logger.debug(f"Deletando pokemon '{pokemon_nome}'")
    session = Session()
    count = session.query(Pokemon).filter(Pokemon.nome == pokemon_nome).delete()
    session.commit()
    if count:               
        logger.debug(f"Pokemon '{pokemon_nome}' deletado com sucesso.")
        return {"mesage": "Pokemon removido", "id": pokemon_nome}
    logger.warning(f"Pokemon '{pokemon_nome}' não encontrado para deleção.")
    return {"message": "Pokemon não encontrado na base :/"}, 404

@app.post('/upload', tags=[home_tag])
def upload_file():
    """Faz o upload de um arquivo para o servidor."""
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    file = request.files['file']
    if not file.filename:
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return jsonify({'message': 'Upload realizado com sucesso', 'filename': file.filename}), 200
    return jsonify({'error': 'Formato de arquivo não suportado'}), 400

@app.get('/uploads/<filename>', tags=[home_tag])
def get_file(filename):
    """Retorna uma imagem ou áudio específico do diretório de uploads."""
    try:
        print(f"Recebido arquivo: {filename}")
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        logger.error(f"Erro ao tentar enviar o arquivo {filename}: {e}")
        return jsonify({"error": "Arquivo não encontrado"}), 404

