"""data/sentetik.csv + data/gercek/*.csv  ->  data/oturumlar.csv
Gerçek dosyalar uygulamanın veri toplama modundan (?mod=veri) inen oturum.csv dosyalarıdır.
Her dosyada 'kaynak' sütunu zaten 'gercek' yazar. Kullanım: python data/birlestir.py"""
import glob
import pandas as pd

parcalar = [pd.read_csv("data/sentetik.csv")]
for yol in sorted(glob.glob("data/gercek/*.csv")):
    d = pd.read_csv(yol)
    assert (d["kaynak"] == "gercek").all(), f"{yol}: kaynak 'gercek' olmalı"
    parcalar.append(d)
tum = pd.concat(parcalar, ignore_index=True)
tum.to_csv("data/oturumlar.csv", index=False)
g = tum[tum.kaynak == "gercek"]["oturum_id"].nunique()
print(f"{len(tum)} satır | gerçek oturum: {g} (hedef ≥ 15) | sentetik oturum: {tum[tum.kaynak=='sentetik']['oturum_id'].nunique()}")
