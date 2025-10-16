from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import User, Favorite, BattleTeam
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users/<int:user_id>/favorites', methods=['GET'])
@jwt_required()
@admin_required()
def get_user_favorites(user_id):
    """Admin: Ver favoritos de qualquer usuário"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'user': user.to_dict(),
        'total': len(favorites),
        'favorites': [fav.to_dict() for fav in favorites]
    }), 200

@admin_bp.route('/users/<int:user_id>/battle-team', methods=['GET'])
@jwt_required()
@admin_required()
def get_user_battle_team(user_id):
    """Admin: Ver time de batalha de qualquer usuário"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    team = BattleTeam.query.filter_by(user_id=user_id).order_by(BattleTeam.position).all()
    
    return jsonify({
        'user': user.to_dict(),
        'total': len(team),
        'team': [member.to_dict() for member in team]
    }), 200

@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
@admin_required()
def get_stats():
    """Admin: Estatísticas gerais do sistema"""
    total_users = User.query.count()
    total_favorites = Favorite.query.count()
    total_teams = db.session.query(BattleTeam.user_id).distinct().count()
    
    # Top 10 Pokémon favoritos
    top_favorites = db.session.query(
        Favorite.pokemon_id,
        Favorite.pokemon_name,
        db.func.count(Favorite.id).label('count')
    ).group_by(Favorite.pokemon_id).order_by(db.desc('count')).limit(10).all()
    
    # Top 10 Pokémon em times
    top_team = db.session.query(
        BattleTeam.pokemon_id,
        BattleTeam.pokemon_name,
        db.func.count(BattleTeam.id).label('count')
    ).group_by(BattleTeam.pokemon_id).order_by(db.desc('count')).limit(10).all()
    
    return jsonify({
        'total_users': total_users,
        'total_favorites': total_favorites,
        'users_with_battle_team': total_teams,
        'top_favorites': [
            {'pokemon_id': f[0], 'pokemon_name': f[1], 'count': f[2]}
            for f in top_favorites
        ],
        'top_battle_team': [
            {'pokemon_id': t[0], 'pokemon_name': t[1], 'count': t[2]}
            for t in top_team
        ]
    }), 200