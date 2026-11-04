# Veri Sözlüğü — `data/oturumlar.csv`

Her satır **bir karar**dır (bir oyuncunun bir sahnedeki seçimi). Bir oturumun **son kararı** veri setine alınmaz, çünkü etiketi gelecekteki kararlara bağlıdır.

| Sütun | Anlamı | Birim / değer | Nasıl ölçülür |
|-------|--------|---------------|---------------|
| `oturum_id` | Bir oyun oturumunun rastgele kimliği | 12 karakterlik rastgele onaltılık metin | Oyun başında `crypto.getRandomValues` ile üretilir; kişiyi tanımlamaz |
| `seviye` | Oyuncunun kendi bildirdiği seviye | 1 = yeni, 2 = orta, 3 = ileri | Başlangıç ekranındaki seçim |
| `karar_suresi_sn` | Sahne ekrana gelişinden "Onayla"ya basışa kadar geçen süre | saniye, 0.5–120 (üstü 120'ye kırpılır) | `performance.now()` farkı |
| `karar_degistirme_sayisi` | Onaydan önce seçenek değiştirme sayısı (ilk seçim sayılmaz) | adet, 0–10 | Seçili seçenek değiştikçe artar |
| `tiklama_araligi_ms` | Sahnedeki ardışık tıklamalar (seçenek, ipucu, onay) arası ortalama süre | milisaniye, 80–5000 | Tıklama zaman damgalarının ardışık farklarının ortalaması |
| `onceki_yanlis_sayisi` | Bu karardan **önce** yapılan yanlış sayısı | adet, 0–20 | Oturum boyunca birikir |
| `ipucu_sayisi` | Bu karardan **önce** oyuncunun kendi isteğiyle açtığı ipucu sayısı | adet, 0–10 | "İpucu" düğmesi; otomatik açılan ipucu sayılmaz |
| `sahne_no` | Sahne sırası | 1–30 (şu an 1–8) | Hikâye sırası |
| `zorlandi` | **Etiket.** Bu karardan sonraki ilk 2 kararda en az 1 yanlış var mı | 1 = evet, 0 = hayır | Gelecekteki kararlardan hesaplanır (özelliklerde gelecek bilgisi yoktur) |
| `kaynak` | Verinin kaynağı | `gercek` \| `sentetik` | Gerçek: uygulamanın `?mod=veri` modu. Sentetik: `data/uret.py` |

## Gizlilik (KVKK)

Ad, e-posta, cihaz kimliği, konum, IP adresi **toplanmaz**. `oturum_id` rastgele üretilir ve kişiyle eşleştirilemez.

## Notlar

- `veri toplama` modunda (`?mod=veri`) model devre dışıdır, yani oyun davranışı veriyi etkilemez.
- Sentetik üreticinin kuralı ve tohumu (`2026`) için `README.md`'ye bakın.
