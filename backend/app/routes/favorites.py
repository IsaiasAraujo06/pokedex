from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Favorite
from app.services.pokeapi import PokeAPIService

favorites_bp = Blueprint('favorites', __name__)

@favorites_bp.route('', methods=['GET'])
@jwt_required()
def list_favorites():
    """Lista todos os favoritos do usuário atual"""
    current_user_id = int(get_jwt_identity())
    
    favorites = Favorite.query.filter_by(user_id=current_user_id).all()
    
    return jsonify({
        'total': len(favorites),
        'favorites': [fav.to_dict() for fav in favorites]
    }), 200

@favorites_bp.route('', methods=['POST'])
@jwt_required()
def add_favorite():
    """Adiciona um Pokémon aos favoritos"""
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data or not data.get('pokemon_id'):
        return jsonify({'error': 'pokemon_id is required'}), 400
    
    pokemon_id = data['pokemon_id']
    
    # Verifica se já existe nos favoritos
    existing = Favorite.query.filter_by(
        user_id=current_user_id,
        pokemon_id=pokemon_id
    ).first()
    
    if existing:
        return jsonify({'error': 'Pokemon already in favorites'}), 409
    
    # Busca dados do Pokémon na PokeAPI
    pokemon_data = PokeAPIService.get_pokemon_details(pokemon_id)
    
    if not pokemon_data:
        return jsonify({'error': 'Pokemon not found'}), 404
    
    # Cria favorito
    favorite = Favorite(
        user_id=current_user_id,
        pokemon_id=pokemon_id,
        pokemon_name=pokemon_data['name']
    )
    
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({
        'message': 'Pokemon added to favorites',
        'favorite': favorite.to_dict()
    }), 201

@favorites_bp.route('/<int:pokemon_id>', methods=['DELETE'])
@jwt_required()
def remove_favorite(pokemon_id):
    """Remove um Pokémon dos favoritos"""
    current_user_id = int(get_jwt_identity())
    
    favorite = Favorite.query.filter_by(
        user_id=current_user_id,
        pokemon_id=pokemon_id
    ).first()
    
    if not favorite:
        return jsonify({'error': 'Pokemon not in favorites'}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({'message': 'Pokemon removed from favorites'}), 200

@favorites_bp.route('/check/<int:pokemon_id>', methods=['GET'])
@jwt_required()
def check_favorite(pokemon_id):
    """Verifica se um Pokémon está nos favoritos"""
    current_user_id = int(get_jwt_identity())
    
    favorite = Favorite.query.filter_by(
        user_id=current_user_id,
        pokemon_id=pokemon_id
    ).first()
    
    return jsonify({
        'is_favorite': favorite is not None
    }), 200