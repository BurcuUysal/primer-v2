"""Sentetik oturum üreticisi. Tohum: 2026 (README'de de yazılı).

Kural: her kişinin gizli bir 'beceri'si var; zorluk = seviye + sahne etkisi.
Yanlış olasılığı ve gözlenen davranışlar (süre, karar değiştirme, tıklama aralığı)
gizli 'zorlanma' halinden doğar. Etiket (zorlandi) GELECEKTEKİ 2 karardaki
yanlıştan türetilir (bkz. spec.md)."""
import csv
import sys

import numpy as np

TOHUM = 2026
KISI, OTURUM_PER_KISI, KARAR = 60, 3, 20


def sig(x):
    return 1 / (1 + np.exp(-x))


def uret(yol):
    rng = np.random.default_rng(TOHUM)
    satirlar = []
    for _ in range(KISI):
        beceri = rng.normal(0, 1)
        for _ in range(OTURUM_PER_KISI):
            oid = "".join(rng.choice(list("0123456789abcdef"), 12))
            seviye = int(rng.integers(1, 4))
            yanlis_say = ipucu_say = 0
            kayit, yanlis_liste = [], []
            for sahne in range(1, KARAR + 1):
                zorluk = 0.6 * seviye + 0.04 * sahne
                zorlanma = sig(-beceri + zorluk - 2.6 + rng.normal(0, 0.9))
                yanlis = rng.random() < sig(7.0 * (zorlanma - 0.5))
                sure = np.clip(rng.normal(4 + 35 * zorlanma, 4), 0.5, 120)
                degis = int(np.clip(rng.poisson(0.1 + 4.0 * zorlanma), 0, 10))
                tikla = float(np.clip(rng.normal(1200 - 800 * zorlanma, 220), 80, 5000))
                kayit.append([oid, seviye, round(float(sure), 2), degis, round(tikla),
                              yanlis_say, ipucu_say, sahne])
                yanlis_liste.append(bool(yanlis))
                yanlis_say += int(yanlis)
                if rng.random() < 0.5 * zorlanma:
                    ipucu_say = min(ipucu_say + 1, 10)
            for i in range(len(kayit) - 1):
                gelecek = yanlis_liste[i + 1:i + 3]
                satirlar.append(kayit[i] + [int(any(gelecek)), "sentetik"])
    with open(yol, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["oturum_id", "seviye", "karar_suresi_sn", "karar_degistirme_sayisi",
                    "tiklama_araligi_ms", "onceki_yanlis_sayisi", "ipucu_sayisi",
                    "sahne_no", "zorlandi", "kaynak"])
        w.writerows(satirlar)
    print(f"{len(satirlar)} satır yazıldı -> {yol}")


if __name__ == "__main__":
    uret(sys.argv[1] if len(sys.argv) > 1 else "data/sentetik.csv")
