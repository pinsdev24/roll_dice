from flask import Flask, render_template
from flask_restful import Api, Resource
from models import db, Player, Game, Configuration
from resources import PlayerResource, SessionResource, GameResource, ConfigurationResource
from swagger import swagger_ui_blueprint, SWAGGER_URL
from flask_migrate import Migrate

app = Flask(__name__, static_url_path='/static')

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/roll_dice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Add resources to the API
api.add_resource(PlayerResource, '/players', '/players/<int:player_id>')
api.add_resource(SessionResource, '/sessions', '/sessions/<int:session_id>')
api.add_resource(GameResource, '/games', '/games/<int:game_id>')
api.add_resource(ConfigurationResource, '/configuration')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/gamers')
def players():
    players = Player.query.all()
    data= [player.serialize() for player in players]
    
    return render_template('players.html', data=data)

@app.route('/games/all')
def games():
    games = Game.query.all()
    data= [game.serialize() for game in games]
    
    return render_template('games.html', data=data)

@app.route('/settings')
def settings():
    config = Configuration.query.first()
    data=  config.serialize()
    return render_template('settings.html', data=data)

@app.route('/get_player/<username>')
def get_user_by_name(username):
    player = Player.query.filter_by(name=username).first()
    if player:
        return player.serialize(), 200
    else:
        return {}, 200

@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages-error-404.html'), 404

# Register the Swagger UI blueprint
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)
