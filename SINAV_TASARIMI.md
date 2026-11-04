# Sizinle Uyumlanan Sınav Tasarımı (1 sayfa)

> Soru: *"Bu sınavı siz olsanız nasıl tasarlardınız? The Primer kullanıcıyla uyumlanan bir sistemdi; peki sizinle uyumlanan, ezberi değil kavramların gerçek özünü ve gerekçesini ölçen klasik vize sorusu nasıl olurdu?"*

## Tasarım ilkesi

The Primer, oyuncunun **davranışına** bakıp zorluğu ayarlıyordu. Sınav da öğrencinin **cevabına** değil **gerekçesine** bakmalı: iki öğrenci aynı sonuca farklı nedenlerle varabilir, bir kavramı ezberleyen ile anlayan ancak *kararını savunurken* ayrışır. Bu yüzden soru tek bir doğru cevap değil, **bir karar + o kararın gerekçesi + o kararı çürütecek bir durum** ister (kapalı kitap olsa bile formül ezberi işe yaramaz).

## Örnek soru (30 dakika, kapalı kitap)

**Senaryo.** Bir okul kütüphanesi, öğrencinin kitabı **geç iade etme olasılığını** tahmin eden küçük bir lojistik regresyon yayınladı (v1.0, doğruluk %88). Ekip, v1.1'in doğruluğunu %91 ölçtü ve **cuma akşamı herkese açmak** istiyor. İki tüketici var: mobil uygulama (ONNX) ve ekibin Python test kahini. 300 ortak girdide ikisi arasındaki en büyük olasılık farkı **0.003**; iki girdide ise **sınıf kararı** farklı çıkıyor. Ayrıca v1.1, yalnızca ilk yıl öğrencilerinden toplanan veriyle eğitilmiş.

**Sorular.**
1. 0.003'lük fark bir **hata mı**? "Hata toleransı" nasıl seçilir; bu eşiği **kim, neye göre, ne zaman** (testten önce mi sonra mı) belirler? (6 puan)
2. Doğruluğun %88 → %91 çıkması, "v1.1 daha iyi" demek için **yeterli mi**? Burada **doğrulama (verification)** ile **geçerleme (validation)** farkını, bu senaryoya özgü birer örnekle açıklayın. (6 puan)
3. Cuma günü herkese açmak yerine nasıl bir devreye alma önerirsiniz? Geri dönüşü **tek adım** yapmak için sürümü neye bağlarsınız ve neden? (5 puan)
4. Sınıf kararının ayrıştığı iki girdi için **hangi testi** yazarsınız ve bu test regresyon testinden nasıl ayrılır? (3 puan)

## Beklenen temel kavramlar (ve ayırt edici noktalar)

- **Hata toleransı:** İki sistem (float32/farklı çalışma zamanı) birebir aynı olmak zorunda değildir; ama tolerans **testten önce**, modelin karar kesme noktasına olan uzaklığına göre belirlenir. Fark, karar eşiğine yakın girdilerde sınıfı çevirebiliyorsa 0.003 **önemlidir**. (Çeldirici: "0.003 küçük, sorun yok.")
- **Diferansiyel test + Oracle:** Aynı girdiyi iki bağımsız tüketiciye verip uyuşmayı ölçmek; hangisinin "doğru" olduğunu bilmesek bile **tutarsızlığı** yakalar.
- **Doğrulama vs. geçerleme:** Doğrulama = "ürünü **doğru** yaptık mı?" (şartnameye uyum: eşik, parite). Geçerleme = "**doğru ürünü** yaptık mı?" (ilk yıl verisi tüm öğrencileri temsil ediyor mu; kütüphanenin gerçek ihtiyacı karşılanıyor mu). Yüksek doğruluk yalnızca birinci soruya cevap verir. (Çeldirici: "doğruluk yüksek, o hâlde geçerli.")
- **Dağılım kayması / temsil sorunu:** Eğitim verisi yalnızca ilk yıllardan; üst sınıflarda model ölçülmemiştir.
- **Güvenli devreye alma:** Shadow → Canary (%5) → aşamalı geçiş; cuma akşamı gibi izlemenin zayıf olduğu zamanda risk alınmaz.
- **Sürümleme:** `main` dalı değil **commit'e sabitlenmiş** sürüm; model ile sözleşme (`config.json`) birlikte sürümlenir. Geri alma = bir önceki commit'e dönmek.
- **Karakterizasyon / regresyon:** Karakterizasyon testi mevcut davranışı *olduğu gibi* kaydeder (iyi mi kötü mü demeden); regresyon testi bilinen iyi davranışın bozulmadığını izler.

## Neden bu soru "uyumlanır"?

Aynı senaryo, öğrencinin ilk cevabına göre **ek soru** ile derinleşebilir: tolerans gerekçesini zayıf yazan öğrenciye "eşiğe 0.0005 uzaklıktaki bir girdide aynı tolerans yeterli mi?" gibi bir ayrıntı sorulur (The Primer'ın zorlanana ipucu vermesinin sınav karşılığı). Ezber cevap, ikinci adımda çöker; kavramı anlayan, gerekçesini ona göre genişletir.

<!-- Bu metni kendi cümlelerinle yeniden yaz: senaryoyu kendi dersine/ilgine uyarla; puanlama ve çeldiricileri savunabileceğin hale getir. -->
