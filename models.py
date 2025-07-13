#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Matematik Canavarı - Veritabanı Modelleri
Database Models for Math Monster Game
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()

class GameScore(db.Model):
    """Oyun skorlarını saklayan model"""
    __tablename__ = 'game_scores'
    
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(100), nullable=False)
    final_score = db.Column(db.Integer, nullable=False, default=0)
    max_level_reached = db.Column(db.Integer, nullable=False, default=1)
    total_questions_answered = db.Column(db.Integer, nullable=False, default=0)
    game_duration_seconds = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<GameScore {self.player_name}: {self.final_score} points>'
    
    def to_dict(self):
        """Model verisini dictionary'ye çevir"""
        return {
            'id': self.id,
            'player_name': self.player_name,
            'final_score': self.final_score,
            'max_level_reached': self.max_level_reached,
            'total_questions_answered': self.total_questions_answered,
            'game_duration_seconds': self.game_duration_seconds,
            'created_at': self.created_at.isoformat()
        }

class PlayerStats(db.Model):
    """Oyuncu istatistiklerini saklayan model"""
    __tablename__ = 'player_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(100), nullable=False, unique=True)
    total_games_played = db.Column(db.Integer, nullable=False, default=0)
    best_score = db.Column(db.Integer, nullable=False, default=0)
    total_score = db.Column(db.Integer, nullable=False, default=0)
    total_questions_answered = db.Column(db.Integer, nullable=False, default=0)
    correct_answers = db.Column(db.Integer, nullable=False, default=0)
    highest_level_reached = db.Column(db.Integer, nullable=False, default=1)
    total_play_time_seconds = db.Column(db.Integer, nullable=False, default=0)
    first_played_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_played_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PlayerStats {self.player_name}: {self.total_games_played} games, best: {self.best_score}>'
    
    def calculate_accuracy(self):
        """Doğruluk oranını hesapla"""
        if self.total_questions_answered == 0:
            return 0.0
        return round((self.correct_answers / self.total_questions_answered) * 100, 1)
    
    def calculate_average_score(self):
        """Ortalama skoru hesapla"""
        if self.total_games_played == 0:
            return 0.0
        return round(self.total_score / self.total_games_played, 1)
    
    def to_dict(self):
        """Model verisini dictionary'ye çevir"""
        return {
            'id': self.id,
            'player_name': self.player_name,
            'total_games_played': self.total_games_played,
            'best_score': self.best_score,
            'total_score': self.total_score,
            'total_questions_answered': self.total_questions_answered,
            'correct_answers': self.correct_answers,
            'accuracy_percentage': self.calculate_accuracy(),
            'average_score': self.calculate_average_score(),
            'highest_level_reached': self.highest_level_reached,
            'total_play_time_seconds': self.total_play_time_seconds,
            'first_played_at': self.first_played_at.isoformat(),
            'last_played_at': self.last_played_at.isoformat()
        }