"""Oturum CSV'sini data/gercek/ içine numaralı dosya olarak kaydeder (doğrulayarak).

Üç kullanım (hangisi kolay geliyorsa):
  1) Dosyadan (önerilen):  python3 data/kaydet.py ~/Downloads/oturum.csv
     Birden çok dosya aynı anda:  python3 data/kaydet.py ~/Downloads/oturum*.csv
  2) Panodan (Mac):        'Yazıyı kopyala'dan sonra  python3 data/kaydet.py
  3) Başka yerden:         python3 data/kaydet.py < dosya.csv

Doğrulama: başlık şemaya uymalı, tüm satırlar kaynak=gercek olmalı, aynı oturum iki kez eklenemez.
"""
import csv
import glob
import io
import os
import subprocess
import sys

BASLIK = ("oturum_id,seviye,karar_suresi_sn,karar_degistirme_sayisi,tiklama_araligi_ms,"
          "onceki_yanlis_sayisi,ipucu_sayisi,sahne_no,zorlandi,kaynak")
KLASOR = os.path.join("data", "gercek")


class Hata(Exception):
    pass


def panodan_ya_da_stdin():
    try:
        return subprocess.run(["pbpaste"], capture_output=True, text=True, check=True).stdout
    except Exception:
        return sys.stdin.read()


def kaydet(metin):
    metin = metin.replace("\r\n", "\n").strip()
    if not metin:
        raise Hata("içerik boş. 'Yazıyı kopyala'ya bastıktan sonra başka bir şey kopyalamadığından emin ol; ya da dosya yolu ver.")
    if metin.split("\n")[0].strip() != BASLIK:
        raise Hata("ilk satır beklenen başlık değil (oyunun CSV'si değil ya da başlık eksik).")
    kayitlar = list(csv.reader(io.StringIO(metin)))[1:]
    if not kayitlar:
        raise Hata("başlıktan başka satır yok.")
    for n, k in enumerate(kayitlar, start=2):
        if len(k) != 10:
            raise Hata(f"{n}. satırda 10 sütun olmalı, {len(k)} var.")
        if k[9] != "gercek":
            raise Hata(f"{n}. satırda kaynak 'gercek' değil.")
    idler = {k[0] for k in kayitlar}
    if len(idler) != 1:
        raise Hata("tek dosyada birden fazla oturum var. Her oturumu ayrı kaydet.")
    oturum_id = idler.pop()
    os.makedirs(KLASOR, exist_ok=True)
    for yol in glob.glob(os.path.join(KLASOR, "*.csv")):
        with open(yol, encoding="utf-8") as f:
            if oturum_id in f.read():
                raise Hata(f"bu oturum zaten kayıtlı ({os.path.basename(yol)}).")
    mevcut = [int(os.path.basename(p)[7:-4]) for p in glob.glob(os.path.join(KLASOR, "oturum_*.csv"))
              if os.path.basename(p)[7:-4].isdigit()]
    sira = (max(mevcut) if mevcut else 0) + 1   # silinen dosya numarası varsa üstüne yazmaz
    yol = os.path.join(KLASOR, f"oturum_{sira:02d}.csv")
    with open(yol, "w", encoding="utf-8", newline="") as f:
        f.write(metin + "\n")
    print(f"Kaydedildi: {yol} ({len(kayitlar)} satır)")


def main():
    yollar = [os.path.expanduser(a) for a in sys.argv[1:]]
    kaynaklar = []
    if yollar:
        for y in yollar:
            try:
                with open(y, encoding="utf-8") as f:
                    kaynaklar.append((y, f.read()))
            except OSError as e:
                print(f"OKUNAMADI: {y} ({e.strerror})")
    else:
        kaynaklar.append(("pano", panodan_ya_da_stdin()))
    basarisiz = 0
    for ad, metin in kaynaklar:
        try:
            kaydet(metin)
        except Hata as e:
            basarisiz += 1
            print(f"KAYDEDİLMEDİ [{ad}]: {e}")
    toplam = len(glob.glob(os.path.join(KLASOR, "*.csv")))
    print(f"Toplam gerçek oturum: {toplam}  (hedef ≥ 15, {max(0, 15 - toplam)} tane kaldı)")
    sys.exit(1 if basarisiz and toplam == 0 else 0)


if __name__ == "__main__":
    main()
