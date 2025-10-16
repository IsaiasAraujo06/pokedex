from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensões
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.pokemon import pokemon_bp
    from app.routes.user import user_bp
    from app.routes.favorites import favorites_bp
    from app.routes.battle_team import battle_team_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(pokemon_bp, url_prefix='/api/pokemon')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(favorites_bp, url_prefix='/api/favorites')
    app.register_blueprint(battle_team_bp, url_prefix='/api/battle-team')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    return app