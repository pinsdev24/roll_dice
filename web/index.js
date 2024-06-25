// app.js
const express = require('express');
const session = require('express-session');
const path = require('path');
const axios = require('axios');
const { log } = require('console');
const app = express();

// Configuration de l'application
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'public/views'));
app.use(express.static(path.join(__dirname, 'public')));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.use(session({
  secret: 'votre_secret_ici',
  resave: false,
  saveUninitialized: true,
  cookie: {
    maxAge: 30*60*1000
  }
}));

// Configuration de l'URL de base de l'API
const API_BASE_URL = 'http://localhost:5000';

// Middleware pour ajouter l'URL de base de l'API à chaque requête
app.use((req, res, next) => {
  req.apiClient = axios.create({
    baseURL: API_BASE_URL
  });
  next();
});

// Routes
app.get('/', (req, res) => {
  res.render('home');
});

app.post('/start-game', async (req, res) => {
  try {
    let player;
    if (req.body.playerName) {
      // Vérifier si le joueur existe déjà
      const existingPlayers = await req.apiClient.get(`/get_player/${req.body.playerName}`);
      if (Object.keys(existingPlayers.data).length === 0) {
        // Créer un nouveau joueur
        player = (await req.apiClient.post('/players', { name: req.body.playerName })).data;
      } else {
        player = existingPlayers.data;
        //return res.render('confirm-player', { player });
      }
    } else {
      // Générer un nom aléatoire pour les visiteurs
      const visitorName = `Visitor${Math.floor(Math.random() * 1000)}`;
      player = (await req.apiClient.post('/players', { name: visitorName })).data;
    }

    const date = new Date()
    // Créer une nouvelle session
    const session = (await req.apiClient.post('/sessions', { start_date: date.toISOString(), creator_id: player.id, players: [player.id] })).data;
    req.session.playerId = player.id;
    req.session.sessionId = session.id;

    res.redirect(`/game?sessionId=${session.id}&name=${player.name}`);
  } catch (error) {
    console.error('Erreur lors du démarrage du jeu:', error);
    res.status(500).send('Une erreur est survenue lors du démarrage du jeu');
    //res.render('page-error-404')
  }
});

app.get('/game', async (req, res) => {
  if (!req.session.playerId || !req.session.sessionId) {
    return res.redirect('/');
  }

  const sessionId = req.query.sessionId;
  const playerName = req.query.name;

  try {
    res.render('game', { sessionId, playerName });
  } catch (error) {
    console.error('Erreur lors du chargement du jeu:', error);
    res.status(500).send('Une erreur est survenue lors du chargement du jeu');
  }
});

app.post('/roll-dice', async (req, res) => {
  if (!req.session.playerId || !req.session.sessionId) {
    return res.status(400).json({ error: 'Session invalide' });
  }

  try {
    const game = (await req.apiClient.post('/games', {
      session_id: req.session.sessionId,
      player_id: req.session.playerId,
      score: req.body.score,
      start_date: req.body.start,
      end_date: req.body.end,
    })).data;

    res.json(game);
  } catch (error) {
    console.error('Erreur lors du lancer de dés:', error);
    res.status(500).json({ error: 'Une erreur est survenue lors du lancer de dés' });
  }
});

app.put('/end-session', async (req, res) => {
  if (!req.session.sessionId) {
    return res.status(400).json({ error: 'Session invalide' });
  }

  try {
    await req.apiClient.put(`/sessions`, {session_id: req.session.sessionId});
    req.session.destroy();
    res.status(200).json({'message': 'Session terminer', 'success': true});
  } catch (error) {
    console.error('Erreur lors de la fin de session:', error);
    res.status(500).json({ error: 'Une erreur est survenue lors de la fin de session', 'success': false});
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Serveur démarré sur le port ${PORT}`);
});