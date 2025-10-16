from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, BattleTeam
from app.services.pokeapi import PokeAPIService

battle_team_bp = Blueprint('battle_team', __name__)

@battle_team_bp.route('', methods=['GET'])
@jwt_required()
def list_battle_team():
    """Lista o time de batalha do usuário (ordenado por posição)"""
    current_user_id = int(get_jwt_identity())
    
    team = BattleTeam.query.filter_by(user_id=current_user_id).order_by(BattleTeam.position).all()
    
    return jsonify({
        'total': len(team),
        'team': [member.to_dict() for member in team]
    }), 200

@battle_team_bp.route('', methods=['POST'])
@jwt_required()
def add_to_battle_team():
    """Adiciona um Pokémon ao time de batalha"""
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data or not data.get('pokemon_id'):
        return jsonify({'error': 'pokemon_id is required'}), 400
    
    pokemon_id = data['pokemon_id']
    
    # Verifica se já existe no time
    existing = BattleTeam.query.filter_by(
        user_id=current_user_id,
        pokemon_id=pokemon_id
    ).first()
    
    if existing:
        return jsonify({'error': 'Pokemon already in battle team'}), 409
    
    # Verifica se já tem 6 Pokémon
    team_count = BattleTeam.query.filter_by(user_id=current_user_id).count()
    
    if team_count >= 6:
        return jsonify({'error': 'Battle team is full (max 6 pokemon)'}), 400
    
    # Busca dados do Pokémon
    pokemon_data = PokeAPIService.get_pokemon_details(pokemon_id)
    
    if not pokemon_data:
        return jsonify({'error': 'Pokemon not found'}), 404
    
    # Define próxima posição disponível
    position = team_count + 1
    
    # Cria membro do time
    team_member = BattleTeam(
        user_id=current_user_id,
        pokemon_id=pokemon_id,
        pokemon_name=pokemon_data['name'],
        position=position
    )
    
    db.session.add(team_member)
    db.session.commit()
    
    return jsonify({
        'message': 'Pokemon added to battle team',
        'team_member': team_member.to_dict()
    }), 201

@battle_team_bp.route('/<int:pokemon_id>', methods=['DELETE'])
@jwt_required()
def remove_from_battle_team(pokemon_id):
    """Remove um Pokémon do time de batalha"""
    current_user_id = int(get_jwt_identity())
    
    team_member = BattleTeam.query.filter_by(
        user_id=current_user_id,
        pokemon_id=pokemon_id
    ).first()
    
    if not team_member:
        return jsonify({'error': 'Pokemon not in battle team'}), 404
    
    removed_position = team_member.position
    
    db.session.delete(team_member)
    
    # Reorganiza posições
    remaining_members = BattleTeam.query.filter_by(user_id=current_user_id).filter(
        BattleTeam.position > removed_position
    ).all()
    
    for member in remaining_members:
        member.position -= 1
    
    db.session.commit()
    
    return jsonify({'message': 'Pokemon removed from battle team'}), 200

@battle_team_bp.route('/reorder', methods=['PUT'])
@jwt_required()
def reorder_battle_team():
    """Reordena o time de batalha"""
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data or not data.get('order'):
        return jsonify({'error': 'order array is required'}), 400
    
    order = data['order']  # Esperado: [pokemon_id1, pokemon_id2, ...]
    
    if len(order) > 6:
        return jsonify({'error': 'Maximum 6 pokemon allowed'}), 400
    
    # Verifica se todos os Pokémon pertencem ao usuário
    for idx, pokemon_id in enumerate(order, start=1):
        team_member = BattleTeam.query.filter_by(
            user_id=current_user_id,
            pokemon_id=pokemon_id
        ).first()
        
        if not team_member:
            return jsonify({'error': f'Pokemon {pokemon_id} not in your team'}), 404
        
        team_member.position = idx
    
    db.session.commit()
    
    return jsonify({'message': 'Battle team reordered successfully'}), 200

@battle_team_bp.route('/check/<int:pokemon_id>', methods=['GET'])
@jwt_required()
def check_in_battle_team(pokemon_id):
    """Verifica se um Pokémon está no time de batalha"""
    current_user_id = int(get_jwt_identity())
    
    team_member = BattleTeam.query.filter_by(
        user_id=current_user_id,
        pokemon_id=pokemon_id
    ).first()
    
    return jsonify({
        'in_battle_team': team_member is not None,
        'position': team_member.position if team_member else None
    }), 200