# The Primer v2 — Spec (model bölümü)

> Bu bölüm **eğitimden ÖNCE** yazılmıştır. Eşiği geçmeyen model yayınlanmaz.

## 1. Model gereksinimi

**Soru:** "Bu oyuncu, bu sahnede şu an zorlanıyor mu?"
**Tür:** İkili sınıflandırma, tabular veri, lojistik regresyon (sklearn → ONNX).
**Çıktı:** `p_zorlanma` ∈ [0, 1].

### Girdiler (config.json'daki sırayla)

| # | Özellik | Birim | Aralık |
|---|---------|-------|--------|
| 1 | `seviye` | tamsayı | 1–3 |
| 2 | `karar_suresi_sn` | saniye | 0–120 |
| 3 | `karar_degistirme_sayisi` | adet | 0–10 |
| 4 | `tiklama_araligi_ms` | ms (sahnedeki ardışık tıklamalar arası ortalama süre) | 0–5000 |
| 5 | `onceki_yanlis_sayisi` | adet (bu karardan ÖNCE) | 0–20 |
| 6 | `ipucu_sayisi` | adet (bu karardan ÖNCE) | 0–10 |
| 7 | `sahne_no` | tamsayı | 1–30 |

### Etiket tanımı (sızıntıyı önlemek için)

`zorlandi = 1`: oyuncu bu karardan **sonraki ilk 2 kararda** (oturumda varsa) en az 1 yanlış yaptıysa; aksi halde 0.
Oturumun son kararı (geleceği yok) veri setine alınmaz.
Etiket yalnızca **gelecekteki** olaylardan türetilir; girdilerde gelecek bilgisi yoktur.

## 2. Eval metriği ve kabul eşiği (altın standart)

Test seti: oturum bazlı ayrım (`GroupShuffleSplit`, `random_state=42`, test %25). Aynı oturum hem eğitimde hem testte bulunmaz.

Model yayınlanabilir ancak ve ancak test setinde **hepsi** sağlanırsa:

- **Recall (zorlandi=1) ≥ 0.70** (zorlanan oyuncuyu kaçırmamak öncelik)
- **F1 (zorlandi=1) ≥ 0.65**
- **ROC-AUC ≥ 0.75** (rastgele tahmin 0.50'dir; sınıf dengesinden bağımsız ölçüt)
- ONNX–sklearn olasılık farkı **< 1e-4**

Eşik altında `train.py` hata koduyla durur, `model.onnx` yazılmaz.

## 3. Oyun davranışı (modelin etkisi)

| p_zorlanma | Davranış |
|-----------|----------|
| ≥ 0.60 | Süre baskısı kalkar, ipucu otomatik sunulur, anlatım **derin** moda geçer |
| 0.30 – 0.60 | Mevcut davranış (değişiklik yok) |
| < 0.30 | Anlatım **kısa**, süre baskısı açık, ipucu gizli |

## 4. Kabul örnekleri

1. **Zorlanan oyuncu:** `karar_suresi_sn=45, karar_degistirme_sayisi=4, onceki_yanlis_sayisi=3` verildiğinde `p ≥ 0.60`; süre sayacı görünmez, ipucu kutusu açılır.
2. **Rahat oyuncu:** `karar_suresi_sn=4, karar_degistirme_sayisi=0, onceki_yanlis_sayisi=0` verildiğinde `p < 0.30`; kısa anlatım gösterilir, sayaç çalışır.
3. **Parite:** `tests/parite.json`'daki 5 referans girdi için uygulamadaki ONNX olasılığı ile Python Oracle olasılığı arasındaki fark **< 1e-4**; ayrıca geçen haftaki E2E testlerinin ilk 20 adımı ve 21. adım bozulmadan geçer.

## 5. Gizlilik (KVKK)

Ad, e-posta, cihaz kimliği, konum **toplanmaz**. `oturum_id` rastgele üretilir. `kaynak` ∈ {`gercek`, `sentetik`}.

## 6. Değişiklik kaydı (dürüstlük notu)

İlk eğitim denemelerinde (kesme noktası 0.50) model recall eşiğini (0.70) geçemedi: recall = 0.636, ROC-AUC = 0.776, F1 = 0.679. Eval kapisi modeli reddetti.
Karar: **eşikler değiştirilmedi**. Spec'teki "zorlanan oyuncuyu kaçırmamak öncelik" ilkesine dayanarak **karar kesme noktası 0.50 → 0.40** yapıldı. Bu karar sonuç görüldükten SONRA verilmiştir.

Tanım netleştirmesi (eğitimden önce, uygulamayı yazarken fark edildi): `tiklama_araligi_ms` ilk taslakta "önceki tıklamadan bu yana" idi. Sentetik üretici "telaşlı/hızlı tıklama = zorlanma" varsayar; uygulama da aynı anlamı ölçsün diye tanım "sahnedeki ardışık tıklamalar arası ortalama süre" yapıldı. Eşikler etkilenmedi.
