# RELEASE.md — The Primer v2

## 1. v2.0'da ne değişti

| | v1 (geçen hafta) | v2.0 (bu hafta) |
|---|---|---|
| Uyum | Sabit kurallar (girişteki 3 soru) | Oyuncu davranışından öğrenen lojistik regresyon (`model.onnx`) |
| Girdi | 3 giriş sorusu | 7 davranış özelliği (süre, karar değiştirme, tıklama aralığı, yanlış/ipucu sayısı, seviye, sahne) |
| Etki | Dal seçimi | Süre baskısı, ipucu ve anlatım derinliği |

**Sabitlenen commit (güncel sürüm):** `9a09a5de74bc36cc59934e34eaffaa6d69253ab9`
**Model URL'si:** `https://huggingface.co/burcuuysal/primer-v2-zorlanma/resolve/9a09a5de74bc36cc59934e34eaffaa6d69253ab9/model.onnx`
**Önceki sürüm (rollback hedefi):** `7e2b1e034c9f7798786adaba36698bb8dffbe5c0`: yalnızca sentetik veriyle eğitilmiş ön sürüm.
Uygulamada bu URL `index.html` içindeki `HF_MODEL_URL` sabitine yazılmıştır (indirme başarısız olursa aynı dosyanın yerel kopyası yedek olarak denenir; `body[data-model-kaynak]` hangisinin kullanıldığını gösterir). Tüketici `main` dalına **asla** bağlanmaz: `main` kayabilir, commit kayamaz.

## 2. Geri alma (Rollback)

Sorun çıkarsa kod değiştirmeden önceki bilinen iyi sürüme dönülür:

1. `index.html` içinde `HF_MODEL_URL` değerini bir önceki sürümün commit'ine çevirin (ör. `.../resolve/<ESKI_COMMIT>/model.onnx`).
2. `config.json`'ı da **aynı commit**'ten alın (model ile sözleşme birlikte sürümlenir; özellik sırası farklıysa yanlış sonuç verir).
3. GitHub Pages'e gönderin; birkaç dakikada yayına girer.

Acil durumda sayfa `?model=<eski_url>&config=<eski_config_url>` parametreleriyle de geçici olarak eski sürümle açılabilir. Bu, geri almanın tek adım olduğunu gösterir, çünkü sürüm bir **commit sabitidir**.

*Not: Hugging Face'te önceki bir sürüm vardır (`7e2b1e0`, yalnızca sentetikle eğitilmiş ön sürüm); geri dönüş hedefi budur. Ayrıca model yüklenemezse uygulama otomatik olarak sabit `normal` davranışa düşer (`index.html` içinde kodlu), yani oyun çalışmaya devam eder; tamamen v1'e dönmek için geçen haftaki sürümün git etiketine/commit'ine geri dönülür.*

## 3. Yeni sürümü güvenle devreye alma (planın nasıl işleyeceği)

> Bu bölüm bir **plandır**; uygulamada henüz kodlanmamıştır. Model tarayıcıda çalıştığı için üç adım da istemci tarafında, kişisel veri toplamadan işler.

- **Shadow (Gölge) Dağıtım:** Yeni model (v2.1) oyuncuya görünmeden, mevcut v2.0 ile **aynı girdilerde** sessizce çalıştırılır. Yalnızca `|p_yeni − p_eski|` farkı ve "farklı davranış seçildi mi" bilgisi *toplu sayaç* olarak tutulur; kimlik yoktur. Oyuncunun deneyimi v2.0 ile devam eder. Çıkış koşulu: davranış ayrışması beklenen aralıkta (ör. < %15) ve hata/istisna yok.
- **Canary (Kanarya) Dağıtım:** Rastgele oturum kimliğinin özetine göre oturumların **%5'i** gerçekten v2.1 ile oynar (`oturum_id` rastgele olduğundan kişiyle eşleşmez). İzlenen metrikler: bitiş oranı, "derin" modun görülme oranı, hata sayısı. Kötüleşme varsa §2'deki rollback.
- **Progressive Rollout (Aşamalı Geçiş):** %5 → **%25 → %50 → %100**. Her aşama, ancak önceki aşamada metrikler bozulmadıysa ve en az N oturum görüldüyse ilerler. Yüzde, `index.html`'e gömülü değil, ayrı küçük bir JSON'dan okunursa, kod değiştirmeden yükseltilir veya düşürülür.

## 4. Mimari dağıtım kararı ve ödünleşim matrisi

**Karar:** Model **tarayıcıda** (`onnxruntime-web`) çalışır; statik site GitHub Pages'te, model dosyası Hugging Face'te commit'e sabit URL'den indirilir.

| Soru | Tarayıcı (`onnxruntime-web`) ✅ seçilen | Cihaz içi mobil (React Native / Expo, gömülü ONNX) | Kendi sunucu (Render.com / Rails veya FastAPI) |
|---|---|---|---|
| **1. İnternet zorunlu mu, gecikme?** | İlk açılışta model + wasm indirilir (gecikme); sonrasında çıkarım yerel ve milisaniyelerdedir, önbellekle çevrimdışına yakın çalışır | İnternet gerekmez; model uygulamayla gelir, gecikme en düşük; güncelleme için yeni uygulama sürümü gerekir | Her kararda ağ gidiş-dönüşü; ücretsiz katmanda soğuk başlangıç gecikmesi; internet zorunlu |
| **2. Veri cihazdan çıkar mı?** (KVKK) | **Çıkmaz**: özellikler tarayıcıda hesaplanır, sunucuya gönderilmez | **Çıkmaz** | **Çıkar**: her istekte davranış özellikleri sunucuya gider; saklama/ günlük politikası gerekir |
| **3. Model gizli kalır mı?** | **Hayır**: model dosyası istemciye iner, herkes indirip inceleyebilir | **Kısmen**: pakete gömülü ama çıkarılabilir | **Daha çok**: model sunucuda kalır; yine de çok sayıda istek-yanıtla tersine mühendislik (model çıkarma) mümkündür |
| Sürümleme / rollback | Commit sabiti + `index.html` değişikliği; hızlı | Mağaza onayı gerekebilir; yavaş | Sunucu tarafında anında; tüm kullanıcılar aynı anda etkilenir |
| Bu proje için sonuç | Gizlilik güçlü, ücretsiz, basit | Ek kurulum/derleme yükü | Bonus için ayrı tüketici olarak değerlendirilebilir |

**Neden tarayıcı?** Model küçüktür (~200 bayt), gizlilik öncelikli (veri cihazdan çıkmıyor), ücretsiz barındırma yeterli. Bedeli: modelin **gizli olmaması**. Bu modelde (lojistik regresyon, 7 ağırlık + 1 sapma) gizlenecek ticari sır olmadığı için kabul edilebilir bir ödünleşimdir.

## 5. Kaynaklar (okuyup referans verilecekler)

Amershi vd. (2019), Shankar vd. (2022, 3V), Mitchell vd. (2019, Model Cards), Breck vd. (2017, ML Test Score), Sommerville Bl. 8 ve Bl. 25, Hugging Face Hub `revision`/`resolve` belgeleri.
> Yukarıdaki matris ve plan derste anlatılan çerçeveye dayanır; kaynakları **kendin okuyup** kendi cümlelerinle hangi kararı hangi kaynağa dayandırdığını buraya ekle.
