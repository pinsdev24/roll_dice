from flask import request, redirect, flash
from flask_restful import Resource, reqparse
from models import db, Player, Session, Game, Configuration
from datetime import datetime

player_parser = reqparse.RequestParser()
player_parser.add_argument('name', type=str, required=True, help="Name of the player")

class PlayerResource(Resource):
    def get(self, player_id=None):
        if player_id:
            player = Player.query.get(player_id)
            
            if player:
                return player.serialize(), 200
            return {'message': 'Player not found'}, 404
        else:
            players = Player.query.all()
            return [player.serialize() for player in players], 200

    def post(self):
        if request.form:
            player = Player(name=request.form['name'], created_at=datetime.now())
        else:
            args = player_parser.parse_args()
            player = Player(name=args['name'])

        db.session.add(player)
        db.session.commit()
        if request.form:
            return redirect('/gamers')
        else:
            return {'message': 'Player created', 'id': player.id}, 201

session_parser = reqparse.RequestParser()
session_parser.add_argument('start_date', type=str, required=True, help="Start date of the session")
session_parser.add_argument('end_date', type=str)
session_parser.add_argument('creator_id', type=int, required=True)
session_parser.add_argument('players', type=list, location='json')

class SessionResource(Resource):
    def get(self, session_id=None):
        if session_id:
            session = Session.query.get(session_id)
            if session:
                return {
                    'id': session.id,
                    'start_date': session.start_date,
                    'end_date': session.end_date,
                    'creator_id': session.creator_id,
                    'players': [player.id for player in session.players]
                }, 200
            return {'message': 'Session not found'}, 404
        else:
            sessions = Session.query.all()
            return [session.serialize() for session in sessions], 200

    def post(self):
        args = session_parser.parse_args()
        session = Session(start_date=args['start_date'], end_date=args.get('end_date'), creator_id=args['creator_id'])
        db.session.add(session)
        if args['players']:
            for player_id in args['players']:
                player = Player.query.get(player_id)
                if player:
                    session.players.append(player)
        db.session.commit()
        return {'message': 'Session created', 'id': session.id}, 201

game_parser = reqparse.RequestParser()
game_parser.add_argument('start_date', type=str, required=True)
game_parser.add_argument('end_date', type=str)
game_parser.add_argument('score', type=int, required=True)
game_parser.add_argument('session_id', type=int, required=True)
game_parser.add_argument('player_id', type=int, required=True)

class GameResource(Resource):
    def get(self, game_id=None):
        if game_id:
            game = Game.query.get(game_id)
            if game:
                return {
                    'id': game.id,
                    'start_date': game.start_date,
                    'end_date': game.end_date,
                    'score': game.score,
                    'session_id': game.session_id,
                    'player_id': game.player_id
                }, 200
            return {'message': 'Game not found'}, 404
        else:
            games = Game.query.all()
            return [game.serialize() for game in games], 200

    def post(self):
        args = game_parser.parse_args()
        game = Game(start_date=args['start_date'], end_date=args.get('end_date'), score=args['score'], session_id=args['session_id'], player_id=args['player_id'])
        db.session.add(game)
        db.session.commit()
        return {'message': 'Game created', 'id': game.id}, 201

class ConfigurationResource(Resource):
    def get(self):
        config = Configuration.query.first()
        if config is None:
            return {"message": "No configuration found"}, 404
        return config.serialize()

    def post(self):
        if request.form.get('_method') == 'PUT':
            return self.put()
        print('HERE POST')
        data = request.get_json()
        config = Configuration(
            default_dice_count=data['default_dice_count'],
            max_games_per_session=data['max_games_per_session'],
            max_sessions=data['max_sessions'],
            created_at= datetime.now(),
            updated_at=datetime.now()
        )
        db.session.add(config)
        db.session.commit()
        return {"message": "Configuration created"}, 201

    def put(self):
        data = request.form

        config = Configuration.query.first()
        if config is None:
            return {"message": "No configuration found"}, 404
        config.default_dice_count = data['default_dice_count']
        config.max_games_per_session = data['max_games_per_session']
        config.max_sessions = data['max_sessions']
        config.updated_at = datetime.utcnow()
        db.session.commit()
        return redirect('/settings')