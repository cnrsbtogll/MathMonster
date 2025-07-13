#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Matematik Canavarı - Çocuklar için Terminal Tabanlı Matematik Oyunu
Turkish Children's Math Game with Progressive Difficulty
"""

import random
import sys
import os

class MatematikCanavari:
    def __init__(self):
        self.skor = 0
        self.zorluk_seviyesi = 1
        self.operasyonlar = ['+', '-', '*']
        
    def temizle_ekran(self):
        """Ekranı temizle"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def hosgeldin_mesaji(self):
        """Hoşgeldin mesajını göster"""
        print("🎮" * 50)
        print("🧮        MATEMATİK CANAVARI        🧮")
        print("🎮" * 50)
        print()
        print("🌟 Merhaba küçük matematik yıldızı! 🌟")
        print("🦄 Matematik canavarı ile birlikte eğlenceli")
        print("   matematik soruları çözeceğiz! 🎯")
        print()
        print("📝 KURALLAR:")
        print("   ✅ Her doğru cevap = 1 puan")
        print("   📈 Her doğru cevapla sorular zorlaşır")
        print("   ❌ Yanlış cevap = Oyun biter")
        print()
        print("🚀 Hazır mısın? Enter'a bas!")
        input()
        self.temizle_ekran()
    
    def sayi_uret(self):
        """Zorluk seviyesine göre sayı üret"""
        if self.zorluk_seviyesi <= 3:
            # Kolay seviye: 1-10 arası
            return random.randint(1, 10)
        elif self.zorluk_seviyesi <= 6:
            # Orta seviye: 1-25 arası
            return random.randint(1, 25)
        elif self.zorluk_seviyesi <= 10:
            # Zor seviye: 1-50 arası
            return random.randint(1, 50)
        else:
            # Çok zor seviye: 1-100 arası
            return random.randint(1, 100)
    
    def soru_olustur(self):
        """Rastgele matematik sorusu oluştur"""
        sayi1 = self.sayi_uret()
        sayi2 = self.sayi_uret()
        operasyon = random.choice(self.operasyonlar)
        
        # Çıkarma işleminde negatif sonuç olmasın
        if operasyon == '-' and sayi1 < sayi2:
            sayi1, sayi2 = sayi2, sayi1
        
        # Çarpma işleminde çok büyük sayılar olmasın
        if operasyon == '*':
            if self.zorluk_seviyesi <= 3:
                sayi1 = random.randint(1, 5)
                sayi2 = random.randint(1, 5)
            elif self.zorluk_seviyesi <= 6:
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
    
    def zorluk_emoji_al(self):
        """Zorluk seviyesine göre emoji döndür"""
        if self.zorluk_seviyesi <= 3:
            return "🌱"  # Kolay
        elif self.zorluk_seviyesi <= 6:
            return "🌿"  # Orta
        elif self.zorluk_seviyesi <= 10:
            return "🌳"  # Zor
        else:
            return "🔥"  # Çok zor
    
    def skor_goster(self):
        """Mevcut skoru ve seviyeyi göster"""
        emoji = self.zorluk_emoji_al()
        print(f"🏆 Skor: {self.skor} | {emoji} Seviye: {self.zorluk_seviyesi}")
        print("=" * 40)
    
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
    
    def oyun_basla(self):
        """Ana oyun döngüsü"""
        self.hosgeldin_mesaji()
        
        while True:
            # Skor ve seviye bilgisini göster
            self.skor_goster()
            
            # Yeni soru oluştur
            sayi1, sayi2, operasyon = self.soru_olustur()
            dogru_cevap = self.cevap_hesapla(sayi1, sayi2, operasyon)
            
            # Soruyu göster
            print(f"🤔 Soru: {sayi1} {operasyon} {sayi2} = ?")
            print()
            
            try:
                # Kullanıcıdan cevap al
                print("💭 Cevabın nedir? ", end="")
                kullanici_cevap = int(input())
                print()
                
                # Cevabı kontrol et
                if kullanici_cevap == dogru_cevap:
                    # Doğru cevap
                    print(self.dogru_cevap_mesaji())
                    self.skor += 1
                    self.zorluk_seviyesi = (self.skor // 3) + 1  # Her 3 doğru cevapta seviye artar
                    print(f"🎁 +1 Puan! Toplam: {self.skor}")
                    print()
                    print("⏳ Bir sonraki soru geliyor...")
                    input("📱 Enter'a bas!")
                    self.temizle_ekran()
                else:
                    # Yanlış cevap - Oyun bitti
                    self.oyun_bitti(dogru_cevap)
                    break
                    
            except ValueError:
                # Geçersiz giriş
                print("❌ Lütfen sadece sayı gir!")
                print(f"🔢 Doğru cevap: {dogru_cevap}")
                self.oyun_bitti(dogru_cevap)
                break
            except KeyboardInterrupt:
                # Ctrl+C ile çıkış
                print("\n\n👋 Görüşürüz! Tekrar gel! 🌟")
                sys.exit(0)
    
    def oyun_bitti(self, dogru_cevap):
        """Oyun bittiğinde gösterilecek mesaj"""
        print("💥" * 30)
        print("🎮        OYUN BİTTİ!        🎮")
        print("💥" * 30)
        print()
        print(f"😔 Maalesef yanlış cevap...")
        print(f"✅ Doğru cevap: {dogru_cevap}")
        print()
        print("🏆" * 20)
        print(f"🎊 FINAL SKOR: {self.skor} 🎊")
        print("🏆" * 20)
        print()
        
        # Skoruna göre mesaj
        if self.skor == 0:
            print("🌱 Başlangıç güzel! Bir daha dene! 💪")
        elif self.skor <= 5:
            print("🌟 İyi bir başlangıç! Daha da iyisini yapabilirsin! 🚀")
        elif self.skor <= 10:
            print("✨ Harika! Sen gerçek bir matematik yıldızısın! ⭐")
        elif self.skor <= 20:
            print("🔥 İnanılmaz! Sen bir matematik dâhisisin! 🧠")
        else:
            print("👑 EFSANE! Sen matematik kralısın! 🦄")
        
        print()
        print("🎮 Tekrar oynamak ister misin? (e/h): ", end="")
        
        try:
            devam = input().lower()
            if devam == 'e' or devam == 'evet':
                # Oyunu yeniden başlat
                self.skor = 0
                self.zorluk_seviyesi = 1
                self.temizle_ekran()
                self.oyun_basla()
            else:
                print("\n👋 Hoşçakal! Tekrar görüşmek üzere! 🌈")
        except KeyboardInterrupt:
            print("\n\n👋 Görüşürüz! 🌟")

def main():
    """Ana fonksiyon"""
    try:
        oyun = MatematikCanavari()
        oyun.oyun_basla()
    except KeyboardInterrupt:
        print("\n\n👋 Oyunu kapattın! Görüşürüz! 🌟")
    except Exception as e:
        print(f"\n❌ Bir hata oluştu: {e}")
        print("🔧 Lütfen oyunu yeniden başlat!")

if __name__ == "__main__":
    main()
