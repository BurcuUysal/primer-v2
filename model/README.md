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

`data/oturumlar.csv` (`kaynak` sütunu: `gercek` | `sentetik`). **Bu sürüm yalnızca sentetik veriyle eğitilmiştir** (180 oturum, 3420 satır, üretici tohumu 2026). Gerçek oturumlar eklendiğinde bu bölüm ve metrikler güncellenmelidir.
Kişisel veri yoktur (ad, e-posta, cihaz kimliği, konum toplanmaz).

## Metrikler (test: oturum bazlı %25, `random_state=42`, kesme noktası 0.40)

| Metrik | Değer | Kabul eşiği |
|--------|-------|-------------|
| Recall (zorlandi=1) | 0.7315 | ≥ 0.70 |
| F1 (zorlandi=1) | 0.6864 | ≥ 0.65 |
| ROC-AUC | 0.7758 | ≥ 0.75 |
| ONNX–sklearn en büyük fark | 1.1e-7 | < 1e-4 |

**Dürüstlük notu:** Kesme noktası 0.50 iken recall 0.636 çıktı ve eval kapısı modeli reddetti. Eşikler değiştirilmedi; "zorlanan oyuncuyu kaçırmamak" önceliği gereği kesme noktası sonuç görüldükten sonra 0.40'a çekildi (bkz. `spec.md` §6).

## Sınırlar

- Yalnızca sentetik veride ölçülmüştür; **gerçek oyuncu davranışında başarısı bilinmiyor**. Sentetik veri, üreticinin varsayımlarını (ör. telaşlı tıklama = zorlanma) yansıtır.
- Yalnızca bu hikâyenin 8 sahnesi ve 3 seviyesi için tasarlanmıştır.
- Lojistik regresyon doğrusaldır; etkileşimleri (ör. süre × seviye) yakalamaz.
- Küçük örneklem: test seti 855 satırdır, metrikler ±birkaç puan oynayabilir.

## Kullanılmaması gereken durumlar

- Bir kişinin yeteneğini, başarısını ya da işe uygunluğunu **değerlendirmek** için.
- Çocuklar veya hassas gruplar hakkında karar vermek için; model yalnızca oyun içi anlatım/ipucu ayarı içindir.
- Kimlik ya da kişisel veriyle birleştirilerek profil çıkarmak için.

## Sürümleme

Tüketiciler modeli `main` dalından değil, **commit'e sabitlenmiş** URL'den indirmelidir:
`https://huggingface.co/<kullanici>/<repo>/resolve/<commit>/model.onnx`
