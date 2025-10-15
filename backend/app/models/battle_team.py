from app import db
from datetime import datetime

class BattleTeam(db.Model):
    __tablename__ = 'battle_team'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pokemon_id = db.Column(db.Integer, nullable=False)
    pokemon_name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.Integer, nullable=False)  # 1 a 6
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint('user_id', 'pokemon_id', name='unique_user_pokemon_team'),
        db.UniqueConstraint('user_id', 'position', name='unique_user_position'),
        db.CheckConstraint('position >= 1 AND position <= 6', name='valid_position')
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'pokemon_id': self.pokemon_id,
            'pokemon_name': self.pokemon_name,
            'position': self.position,
            'created_at': self.created_at.isoformat()
        }