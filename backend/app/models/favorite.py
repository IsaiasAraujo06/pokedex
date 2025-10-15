from app import db
from datetime import datetime

class Favorite(db.Model):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pokemon_id = db.Column(db.Integer, nullable=False)
    pokemon_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Constraint: um usuário não pode favoritar o mesmo pokemon duas vezes
    __table_args__ = (db.UniqueConstraint('user_id', 'pokemon_id', name='unique_user_pokemon'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'pokemon_id': self.pokemon_id,
            'pokemon_name': self.pokemon_name,
            'created_at': self.created_at.isoformat()
        }