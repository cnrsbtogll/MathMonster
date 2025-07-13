#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Matematik Canavarı - Web Tabanlı Matematik Oyunu
Web-based Turkish Children's Math Game
"""

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import random
import json

app = Flask(__name__)
app.secret_key = 'matematik_canavari_secret_key_2024'

class MatematikCanavariWeb:
    def __init__(self):
        pass
    
    def reset_game(self):
        """Oyunu sıfırla"""
        session['skor'] = 0
        session['zorluk_seviyesi'] = 1
        session['operasyonlar'] = ['+', '-', '*']
        session['oyun_durumu'] = 'baslamadi'
    
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

# Global oyun instance
oyun = MatematikCanavariWeb()

@app.route('/')
def ana_sayfa():
    """Ana sayfa"""
    if 'skor' not in session:
        oyun.reset_game()
    return render_template('index.html')

@app.route('/oyun_basla', methods=['POST'])
def oyun_basla():
    """Oyunu başlat"""
    oyun.reset_game()
    session['oyun_durumu'] = 'oynuyor'
    
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
    return render_template('oyun_bitti.html', final_skor=final_skor)

@app.route('/yeniden_oyna', methods=['POST'])
def yeniden_oyna():
    """Oyunu yeniden başlat"""
    return redirect(url_for('ana_sayfa'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)