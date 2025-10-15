from app import create_app, db
from app.models import User, Favorite, BattleTeam  # ← ADICIONA ISSO

app = create_app()

@app.route('/health')
def health_check():
    return {'status': 'healthy', 'message': 'API is running'}, 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)