# Sizinle Uyumlanan Sınav Tasarımı

**Fikir.** The Primer, oyuncunun cevabına değil davranışına bakıp zorluğu ayarlıyordu. Sınav da öğrencinin cevabından çok gerekçesine bakmalı: iki kişi aynı sonuca farklı nedenlerle varabilir ve kavramı ezberleyen ile anlayan ancak kararını savunurken ayrışır. Bu yüzden soru tek bir doğru cevap değil, bir karar, o kararın gerekçesi ve onu çürütebilecek bir durum ister.

## Örnek soru (30 dakika, kapalı kitap)

**Senaryo.** Bir okul kütüphanesi, öğrencinin kitabı geç iade etme olasılığını tahmin eden küçük bir model kullanıyor (v1.0, doğruluk %88). Ekip, doğruluğu %91 çıkan v1.1'i cuma akşamı herkese açmak istiyor. Mobil uygulama ile ekibin Python test kahini arasında en büyük olasılık farkı 0.003; iki girdide ise sınıf kararı farklı çıkıyor. v1.1 yalnızca ilk yıl öğrencilerinin verisiyle eğitilmiş.

1. 0.003'lük fark bir hata mı? Hata toleransı nasıl seçilir; bunu kim, neye göre ve ne zaman (testten önce mi sonra mı) belirler? (6 puan)
2. Doğruluğun %88'den %91'e çıkması "v1.1 daha iyi" demek için yeterli mi? Doğrulama ile geçerleme farkını bu senaryodan birer örnekle açıklayın. (6 puan)
3. Cuma akşamı herkese açmak yerine ne önerirsiniz? Geri dönüşü tek adım yapmak için sürümü neye bağlarsınız? (5 puan)
4. Sınıf kararı farklı çıkan iki girdi için hangi testi yazarsınız ve bu test regresyon testinden nasıl ayrılır? (3 puan)

## İyi bir cevapta olması gerekenler

- Toleransın testten önce, modelin karar eşiğine uzaklığına göre belirlenmesi; eşiğe yakın girdilerde 0.003'ün sınıfı çevirebileceği.
- Doğrulama "ürünü doğru yaptık mı?" (şartnameye uyum), geçerleme "doğru ürünü yaptık mı?" (eğitim verisi tüm öğrencileri temsil ediyor mu).
- Shadow, canary ve aşamalı geçiş; `main` dalı değil commit'e sabitlenmiş sürüm; geri alma bir önceki commit'e dönmek.

## Çeldiriciler

- "0.003 çok küçük, sorun yok."
- "Doğruluk yüksek, o hâlde model geçerli."

## Neden bu soru "uyumlanır"?

Öğrenci tolerans gerekçesini zayıf yazarsa ek soru gelir: "Karar eşiğine 0.0005 uzaklıktaki bir girdide aynı tolerans yeterli mi?" Ezber cevap bu noktada çöker; kavramı anlayan öğrenci gerekçesini genişletir. The Primer'ın zorlanan oyuncuya ipucu vermesinin sınav karşılığı budur.
