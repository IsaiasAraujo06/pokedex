from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Favorite, BattleTeam
from app.services.pokeapi import PokeAPIService

pokemon_bp = Blueprint('pokemon', __name__)

@pokemon_bp.route('', methods=['GET'])
@jwt_required()
def list_pokemon():
    """
    Lista Pokémon com opções de filtro
    Query params: limit, offset, generation, name
    """
    limit = request.args.get('limit', 151, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    # Busca na PokeAPI
    data = PokeAPIService.get_pokemon_list(limit=limit, offset=offset)
    
    if not data:
        return jsonify({'error': 'Failed to fetch pokemon data'}), 500
    
    return jsonify(data), 200

@pokemon_bp.route('/<int:pokemon_id>', methods=['GET'])
@jwt_required()
def get_pokemon(pokemon_id):
    """
    Busca detalhes de um Pokémon específico
    """
    data = PokeAPIService.get_pokemon_details(pokemon_id)
    
    if not data:
        return jsonify({'error': 'Pokemon not found'}), 404
    
    formatted_data = PokeAPIService.format_pokemon_for_frontend(data)
    return jsonify(formatted_data), 200

# Vamos implementar o resto amanhã (favoritos e battle team)