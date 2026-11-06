---
license: mit
tags: [tabular-classification, onnx, education, logistic-regression]
---

# The Primer v2 — "Zorlanma" modeli (v2.0)

## Amaç

Bir oyuncunun hikâye oyununda **bir sonraki 2 kararda zorlanıp zorlanmayacağını** tahmin eder. Çıktı `p` (0–1) oyunun davranışını değiştirir: `p ≥ 0.60` → süre baskısı kalkar, ipucu açılır, anlatım derinleşir; `p < 0.30` → kısa anlatım. Ders ödevi kapsamında küçük, göreve özel bir modeldir.

## Model

Lojistik regresyon (sklearn), StandardScaler ağırlıklara katlanmış. ONNX, `onnx_yaz.py` ile üretilir. Girdi `girdi` `[N, 7]` float32, çıktı `p` `[N, 1]`. Özellik adları ve sırası `config.json` içindedir; **istemci bu sırayı ve adı sözleşme olarak kabul etmelidir**.

## Veri

`data/oturumlar.csv` (`kaynak` sütunu: `gercek` | `sentetik`): **3455 satır; 180 sentetik oturum (3420 satır) ve 5 gerçek oturum (35 satır)**. Sentetik üretici tohumu 2026. Gerçek oturumlar uygulamanın veri toplama modunda (`?mod=veri`) oynanmıştır; **gerçek veri toplam verinin yaklaşık %1'idir**, yani model ağırlıklı olarak sentetik veriden öğrenmiştir.
Kişisel veri yoktur (ad, e-posta, cihaz kimliği, konum toplanmaz).

## Metrikler (test: oturum bazlı %25, `random_state=42`, kesme noktası 0.40; test seti 881 satır, %99,2'si sentetik)

| Metrik | Değer | Kabul eşiği |
|--------|-------|-------------|
| Recall (zorlandi=1) | 0.7328 | ≥ 0.70 |
| F1 (zorlandi=1) | 0.6977 | ≥ 0.65 |
| ROC-AUC | 0.7818 | ≥ 0.75 |
| ONNX–sklearn en büyük fark | 1.3e-07 | < 1e-4 |

**Dürüstlük notu:** Kesme noktası 0.50 iken recall 0.636 çıktı ve eval kapısı modeli reddetti. Eşikler değiştirilmedi; "zorlanan oyuncuyu kaçırmamak" önceliği gereği kesme noktası sonuç görüldükten sonra 0.40'a çekildi (bkz. `spec.md` §6).

## Gerçek veride dış doğrulama (dürüstlük notu)

Yukarıdaki metrikler çoğunlukla **sentetik** satırlarda ölçüldüğü için gerçek davranışı iyi temsil etmez. Bu yüzden gerçek 35 satır (5 oturum, 8 pozitif satır) ayrıca denendi:

| Ölçüm | Recall | Precision | F1 | ROC-AUC |
|---|---|---|---|---|
| Ön sürüm (yalnızca sentetikle eğitilmiş, `7e2b1e0`), gerçek 35 satırda | 0.375 | 0.750 | 0.500 | 0.741 |
| Güncel eğitim tarifi, **bir-oturum-dışarıda** doğrulama (gerçek 35 satır) | 0.250 | 0.667 | 0.364 | 0.727 |
| *Kabul eşikleri (spec.md)* | *≥ 0.70* | – | *≥ 0.65* | *≥ 0.75* |

**Okuma:** Gerçek oturumlarda model "zorlanıyor" demekte çekingen (gerçekte %23 pozitif, modelin işaretlediği %9); zorlanan oyuncuların yalnızca dörtte biri yakalanıyor. **Eşikler gerçek veride sağlanmıyor.** Örneklem çok küçük (5 oturum, 8 pozitif satır), bu yüzden sonuç kesin hüküm değil, ama yönü açık: sentetik üretici gerçek oyuncuları olduğundan daha çok zorlanır varsayıyor (sentetik pozitif oranı yaklaşık %43-55, gerçek %23).

## Sınırlar

- Eşikler **gerçek veride sağlanmıyor** (yukarıdaki tablo); kabul kapısı büyük ölçüde sentetik veri üzerinde geçildi. Sentetik veri, üreticinin varsayımlarını (ör. telaşlı tıklama = zorlanma) yansıtır.
- Gerçek veri yalnızca 5 oturumdur; daha fazla gerçek oturumla model yeniden eğitilmelidir.
- Yalnızca bu hikâyenin 8 sahnesi ve 3 seviyesi için tasarlanmıştır.
- Lojistik regresyon doğrusaldır; etkileşimleri (ör. süre × seviye) yakalamaz.
- Küçük örneklem: test seti 881 satırdır (%99,2'si sentetik) ve gerçek veri yalnızca 35 satırdır; metrikler ±birkaç puan oynayabilir.

## Kullanılmaması gereken durumlar

- Bir kişinin yeteneğini, başarısını ya da işe uygunluğunu **değerlendirmek** için.
- Çocuklar veya hassas gruplar hakkında karar vermek için; model yalnızca oyun içi anlatım/ipucu ayarı içindir.
- Kimlik ya da kişisel veriyle birleştirilerek profil çıkarmak için.

## Sürümleme

Tüketiciler modeli `main` dalından değil, **commit'e sabitlenmiş** URL'den indirmelidir:
`https://huggingface.co/burcuuysal/primer-v2-zorlanma/resolve/<commit>/model.onnx`

Güncel sürümün sabitlenen commit'i ve geri alma planı için uygulama deposundaki `RELEASE.md` dosyasına bakın: <https://github.com/BurcuUysal/primer-v2>
