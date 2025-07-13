#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Matematik Canavarı - Web Tabanlı Matematik Oyunu
Web-based Turkish Children's Math Game
"""

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import random
import json
import os
from datetime import datetime
from models import db, GameScore, PlayerStats

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'matematik_canavari_secret_key_2024')

# Veritabanı konfigürasyonu
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 300,
    'pool_pre_ping': True,
}

# Veritabanını başlat
db.init_app(app)

class MatematikCanavariWeb:
    def __init__(self):
        pass
    
    def reset_game(self):
        """Oyunu sıfırla"""
        session['skor'] = 0
        session['zorluk_seviyesi'] = 1
        session['operasyonlar'] = ['+', '-', '*']
        session['oyun_durumu'] = 'baslamadi'
        session['game_start_time'] = datetime.now().timestamp()
        session['total_questions'] = 0
    
    def sayi_uret(self, zorluk_seviyesi):
        """Zorluk seviyesine göre sayı üret"""
        if zorluk_seviyesi <= 3:
            return random.randint(1, 10)
        elif zorluk_seviyesi <= 6:
            return random.randint(1, 25)
        elif zorluk_seviyesi <= 10:
            return random.randint(1, 50)
        else:
            return random.randint(1, 100)
    
    def soru_olustur(self):
        """Rastgele matematik sorusu oluştur"""
        zorluk = session.get('zorluk_seviyesi', 1)
        sayi1 = self.sayi_uret(zorluk)
        sayi2 = self.sayi_uret(zorluk)
        operasyon = random.choice(session['operasyonlar'])
        
        # Çıkarma işleminde negatif sonuç olmasın
        if operasyon == '-' and sayi1 < sayi2:
            sayi1, sayi2 = sayi2, sayi1
        
        # Çarpma işleminde çok büyük sayılar olmasın
        if operasyon == '*':
            if zorluk <= 3:
                sayi1 = random.randint(1, 5)
                sayi2 = random.randint(1, 5)
            elif zorluk <= 6:
                sayi1 = random.randint(1, 10)
                sayi2 = random.randint(1, 10)
            else:
                sayi1 = random.randint(1, 15)
                sayi2 = random.randint(1, 15)
        
        return sayi1, sayi2, operasyon
    
    def cevap_hesapla(self, sayi1, sayi2, operasyon):
        """Doğru cevabı hesapla"""
        if operasyon == '+':
            return sayi1 + sayi2
        elif operasyon == '-':
            return sayi1 - sayi2
        elif operasyon == '*':
            return sayi1 * sayi2
    
    def zorluk_emoji_al(self, zorluk_seviyesi):
        """Zorluk seviyesine göre emoji döndür"""
        if zorluk_seviyesi <= 3:
            return "🌱"
        elif zorluk_seviyesi <= 6:
            return "🌿"
        elif zorluk_seviyesi <= 10:
            return "🌳"
        else:
            return "🔥"
    
    def dogru_cevap_mesaji(self):
        """Doğru cevap için rastgele teşvik mesajı"""
        mesajlar = [
            "🎉 Harika! Çok güzel! 🌟",
            "✨ Süpersin! Devam et! 🚀",
            "🎯 Mükemmel! Sen bir dâhisin! 🧠",
            "🌈 Bravo! Çok başarılısın! 👏",
            "⭐ İnanılmaz! Harikasın! 🦄",
            "🎊 Fantastik! Matematik yıldızısın! ✨",
            "🏅 Muhteşem! Böyle devam! 💪",
            "🎈 Tebrikler! Çok zekisin! 🧮"
        ]
        return random.choice(mesajlar)
    
    def save_game_result(self):
        """Oyun sonucunu veritabanına kaydet"""
        try:
            player_name = session.get('player_name', 'Misafir')
            final_score = session.get('skor', 0)
            max_level = session.get('zorluk_seviyesi', 1)
            total_questions = session.get('total_questions', 0)
            
            # Oyun süresini hesapla
            game_start_time = session.get('game_start_time', datetime.now().timestamp())
            game_duration = int(datetime.now().timestamp() - game_start_time)
            
            # Oyun skorunu kaydet
            game_score = GameScore(
                player_name=player_name,
                final_score=final_score,
                max_level_reached=max_level,
                total_questions_answered=total_questions,
                game_duration_seconds=game_duration
            )
            
            db.session.add(game_score)
            
            # Oyuncu istatistiklerini güncelle veya oluştur
            player_stats = PlayerStats.query.filter_by(player_name=player_name).first()
            
            if not player_stats:
                # Yeni oyuncu
                player_stats = PlayerStats(
                    player_name=player_name,
                    total_games_played=1,
                    best_score=final_score,
                    total_score=final_score,
                    total_questions_answered=total_questions,
                    correct_answers=final_score,  # Her doğru cevap 1 puan
                    highest_level_reached=max_level,
                    total_play_time_seconds=game_duration
                )
                db.session.add(player_stats)
            else:
                # Mevcut oyuncuyu güncelle
                player_stats.total_games_played += 1
                player_stats.total_score += final_score
                player_stats.total_questions_answered += total_questions
                player_stats.correct_answers += final_score
                player_stats.total_play_time_seconds += game_duration
                player_stats.last_played_at = datetime.utcnow()
                
                if final_score > player_stats.best_score:
                    player_stats.best_score = final_score
                
                if max_level > player_stats.highest_level_reached:
                    player_stats.highest_level_reached = max_level
            
            db.session.commit()
            print(f"Oyun kaydedildi: {player_name} - Skor: {final_score}")
            
        except Exception as e:
            print(f"Veritabanı hatası: {e}")
            db.session.rollback()
            # Hata olsa bile session'ı temizle
            return

# Global oyun instance
oyun = MatematikCanavariWeb()

@app.route('/')
def ana_sayfa():
    """Ana sayfa"""
    if 'skor' not in session:
        oyun.reset_game()
    
    # En iyi skorları getir (her kullanıcının en yüksek skoru)
    subquery = db.session.query(
        GameScore.player_name,
        db.func.max(GameScore.final_score).label('max_score')
    ).group_by(GameScore.player_name).subquery()
    
    top_scores = db.session.query(GameScore).join(
        subquery,
        db.and_(
            GameScore.player_name == subquery.c.player_name,
            GameScore.final_score == subquery.c.max_score
        )
    ).order_by(GameScore.final_score.desc()).limit(5).all()
    
    # Hata mesajını al ve temizle
    error_message = session.pop('error_message', None)
    
    return render_template('index.html', top_scores=top_scores, error_message=error_message)

@app.route('/oyun_basla', methods=['POST'])
def oyun_basla():
    """Oyunu başlat"""
    player_name = request.form.get('player_name', '').strip()
    
    # Ad kontrolü
    if not player_name:
        # Ana sayfaya geri dön hata mesajı ile
        session['error_message'] = 'Lütfen adınızı girin!'
        return redirect(url_for('ana_sayfa'))
    
    oyun.reset_game()
    session['oyun_durumu'] = 'oynuyor'
    session['player_name'] = player_name
    
    # İlk soruyu oluştur
    sayi1, sayi2, operasyon = oyun.soru_olustur()
    session['mevcut_soru'] = {
        'sayi1': sayi1,
        'sayi2': sayi2,
        'operasyon': operasyon,
        'dogru_cevap': oyun.cevap_hesapla(sayi1, sayi2, operasyon)
    }
    
    return redirect(url_for('oyun_sayfasi'))

@app.route('/oyun')
def oyun_sayfasi():
    """Oyun sayfası"""
    if session.get('oyun_durumu') != 'oynuyor':
        return redirect(url_for('ana_sayfa'))
    
    return render_template('oyun.html', 
                         skor=session.get('skor', 0),
                         zorluk_seviyesi=session.get('zorluk_seviyesi', 1),
                         zorluk_emoji=oyun.zorluk_emoji_al(session.get('zorluk_seviyesi', 1)),
                         soru=session.get('mevcut_soru'))

@app.route('/cevap_kontrol', methods=['POST'])
def cevap_kontrol():
    """Cevabı kontrol et"""
    if session.get('oyun_durumu') != 'oynuyor':
        return redirect(url_for('ana_sayfa'))
    
    try:
        kullanici_cevap = int(request.form.get('cevap', 0))
        dogru_cevap = session['mevcut_soru']['dogru_cevap']
        
        if kullanici_cevap == dogru_cevap:
            # Doğru cevap
            session['skor'] += 1
            session['zorluk_seviyesi'] = (session['skor'] // 3) + 1
            session['total_questions'] = session.get('total_questions', 0) + 1
            
            mesaj = oyun.dogru_cevap_mesaji()
            
            # Yeni soru oluştur
            sayi1, sayi2, operasyon = oyun.soru_olustur()
            session['mevcut_soru'] = {
                'sayi1': sayi1,
                'sayi2': sayi2,
                'operasyon': operasyon,
                'dogru_cevap': oyun.cevap_hesapla(sayi1, sayi2, operasyon)
            }
            
            return jsonify({
                'dogru': True,
                'mesaj': mesaj,
                'yeni_skor': session['skor'],
                'yeni_seviye': session['zorluk_seviyesi'],
                'zorluk_emoji': oyun.zorluk_emoji_al(session['zorluk_seviyesi']),
                'yeni_soru': session['mevcut_soru']
            })
        else:
            # Yanlış cevap - Oyun bitti
            session['oyun_durumu'] = 'bitti'
            session['total_questions'] = session.get('total_questions', 0) + 1
            
            # Oyun sonuçlarını veritabanına kaydet
            oyun.save_game_result()
            
            final_skor = session['skor']
            
            return jsonify({
                'dogru': False,
                'dogru_cevap': dogru_cevap,
                'final_skor': final_skor
            })
            
    except ValueError:
        return jsonify({
            'hata': True,
            'mesaj': 'Lütfen geçerli bir sayı girin!'
        })

@app.route('/oyun_bitir')
def oyun_bitir():
    """Oyun bitiş sayfası"""
    final_skor = session.get('skor', 0)
    player_name = session.get('player_name', 'Misafir')
    
    # Oyuncunun istatistiklerini getir
    player_stats = PlayerStats.query.filter_by(player_name=player_name).first()
    
    return render_template('oyun_bitti.html', 
                         final_skor=final_skor, 
                         player_name=player_name,
                         player_stats=player_stats)

@app.route('/yeniden_oyna', methods=['POST'])
def yeniden_oyna():
    """Oyunu yeniden başlat"""
    # Kullanıcı adını koru
    player_name = session.get('player_name', '')
    
    # Ad kontrolü
    if not player_name:
        # Eğer ad yoksa ana sayfaya gönder
        session['error_message'] = 'Lütfen adınızı girin!'
        return redirect(url_for('ana_sayfa'))
    
    oyun.reset_game()
    session['oyun_durumu'] = 'oynuyor'
    session['player_name'] = player_name  # Adı tekrar kaydet
    return redirect(url_for('oyun_sayfasi'))

@app.route('/istatistikler')
def istatistikler():
    """İstatistikler sayfası"""
    # En iyi skorlar (her kullanıcının en yüksek skoru)
    subquery = db.session.query(
        GameScore.player_name,
        db.func.max(GameScore.final_score).label('max_score')
    ).group_by(GameScore.player_name).subquery()
    
    top_scores = db.session.query(GameScore).join(
        subquery,
        db.and_(
            GameScore.player_name == subquery.c.player_name,
            GameScore.final_score == subquery.c.max_score
        )
    ).order_by(GameScore.final_score.desc()).limit(10).all()
    
    # En aktif oyuncular
    top_players = PlayerStats.query.order_by(PlayerStats.total_games_played.desc()).limit(10).all()
    
    # Genel istatistikler
    total_games = GameScore.query.count()
    total_players = PlayerStats.query.count()
    
    if total_games > 0:
        avg_score = db.session.query(db.func.avg(GameScore.final_score)).scalar()
        avg_score = round(avg_score, 1) if avg_score else 0
    else:
        avg_score = 0
    
    return render_template('istatistikler.html',
                         top_scores=top_scores,
                         top_players=top_players,
                         total_games=total_games,
                         total_players=total_players,
                         avg_score=avg_score)

@app.route('/api/player_stats/<player_name>')
def player_stats_api(player_name):
    """Oyuncu istatistiklerini JSON olarak döndür"""
    player_stats = PlayerStats.query.filter_by(player_name=player_name).first()
    if player_stats:
        return jsonify(player_stats.to_dict())
    else:
        return jsonify({'error': 'Player not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        # Veritabanı tablolarını oluştur
        db.create_all()
    
    app.run(host='0.0.0.0', port=5000, debug=True)