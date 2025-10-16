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
    Lista Pokémon com filtros e paginação
    Query params:
    - limit: número de resultados (default: 20)
    - offset: offset para paginação (default: 0)
    - generation: filtrar por geração (1-9)
    - search: buscar por nome
    """
    current_user_id = int(get_jwt_identity())
    
    limit = request.args.get('limit', 20, type=int)
    offset = request.args.get('offset', 0, type=int)
    generation = request.args.get('generation', type=int)
    search = request.args.get('search', type=str)
    
    # Se tem busca por nome
    if search:
        pokemon_data = PokeAPIService.get_pokemon_by_name(search)
        if not pokemon_data:
            return jsonify({'error': 'Pokemon not found'}), 404
        
        formatted = PokeAPIService.format_pokemon_for_frontend(pokemon_data)
        
        # Adiciona status de favorito e battle team
        formatted['is_favorite'] = Favorite.query.filter_by(
            user_id=current_user_id,
            pokemon_id=formatted['id']
        ).first() is not None
        
        team_member = BattleTeam.query.filter_by(
            user_id=current_user_id,
            pokemon_id=formatted['id']
        ).first()
        
        formatted['in_battle_team'] = team_member is not None
        formatted['battle_team_position'] = team_member.position if team_member else None
        
        return jsonify({
            'count': 1,
            'results': [formatted]
        }), 200
    
    # Se filtrar por geração
    if generation:
        generation_data = PokeAPIService.get_generation(generation)
        if not generation_data:
            return jsonify({'error': 'Generation not found'}), 404
        
        # PokeAPI retorna species, precisa buscar dados completos
        pokemon_species = generation_data.get('pokemon_species', [])
        results = []
        
        for species in pokemon_species[offset:offset+limit]:
            # Extrai ID do URL
            species_url = species['url']
            species_id = int(species_url.split('/')[-2])
            
            pokemon_data = PokeAPIService.get_pokemon_details(species_id)
            if pokemon_data:
                formatted = PokeAPIService.format_pokemon_for_frontend(pokemon_data)
                
                # Adiciona status
                formatted['is_favorite'] = Favorite.query.filter_by(
                    user_id=current_user_id,
                    pokemon_id=formatted['id']
                ).first() is not None
                
                team_member = BattleTeam.query.filter_by(
                    user_id=current_user_id,
                    pokemon_id=formatted['id']
                ).first()
                
                formatted['in_battle_team'] = team_member is not None
                formatted['battle_team_position'] = team_member.position if team_member else None
                
                results.append(formatted)
        
        return jsonify({
            'count': len(pokemon_species),
            'results': results
        }), 200
    
    # Lista normal com paginação
    data = PokeAPIService.get_pokemon_list(limit=limit, offset=offset)
    
    if not data:
        return jsonify({'error': 'Failed to fetch pokemon data'}), 500
    
    # Busca favoritos e battle team do usuário
    user_favorites = {f.pokemon_id for f in Favorite.query.filter_by(user_id=current_user_id).all()}
    user_team = {t.pokemon_id: t.position for t in BattleTeam.query.filter_by(user_id=current_user_id).all()}
    
    # Adiciona status aos resultados
    results = []
    for pokemon in data['results']:
        # Extrai ID do URL
        pokemon_id = int(pokemon['url'].split('/')[-2])
        
        results.append({
            'id': pokemon_id,
            'name': pokemon['name'],
            'url': pokemon['url'],
            'is_favorite': pokemon_id in user_favorites,
            'in_battle_team': pokemon_id in user_team,
            'battle_team_position': user_team.get(pokemon_id)
        })
    
    return jsonify({
        'count': data['count'],
        'next': data['next'],
        'previous': data['previous'],
        'results': results
    }), 200

@pokemon_bp.route('/<int:pokemon_id>', methods=['GET'])
@jwt_required()
def get_pokemon(pokemon_id):
    """Busca detalhes de um Pokémon específico"""
    current_user_id = int(get_jwt_identity())
    
    data = PokeAPIService.get_pokemon_details(pokemon_id)
    
    if not data:
        return jsonify({'error': 'Pokemon not found'}), 404
    
    formatted_data = PokeAPIService.format_pokemon_for_frontend(data)
    
    # Adiciona status de favorito e battle team
    formatted_data['is_favorite'] = Favorite.query.filter_by(
        user_id=current_user_id,
        pokemon_id=pokemon_id
    ).first() is not None
    
    team_member = BattleTeam.query.filter_by(
        user_id=current_user_id,
        pokemon_id=pokemon_id
    ).first()
    
    formatted_data['in_battle_team'] = team_member is not None
    formatted_data['battle_team_position'] = team_member.position if team_member else None
    
    return jsonify(formatted_data), 200