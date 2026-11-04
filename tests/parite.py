"""Test Kahini (Oracle): model.onnx'i Python'da çalıştırır.
  python tests/parite.py --yaz   -> tests/parite.json'u üretir
  python tests/parite.py         -> parite.json ile yeniden hesabı karşılaştırır (< 1e-4)"""
import json
import sys
import numpy as np
import onnxruntime as ort

TOL = 1e-4
CONFIG = json.load(open("model/config.json", encoding="utf-8"))
OZ = CONFIG["ozellikler"]
GIRDILER = [
    {"seviye": 2, "karar_suresi_sn": 45, "karar_degistirme_sayisi": 4, "tiklama_araligi_ms": 500, "onceki_yanlis_sayisi": 3, "ipucu_sayisi": 2, "sahne_no": 8},
    {"seviye": 1, "karar_suresi_sn": 4, "karar_degistirme_sayisi": 0, "tiklama_araligi_ms": 1100, "onceki_yanlis_sayisi": 0, "ipucu_sayisi": 0, "sahne_no": 2},
    {"seviye": 3, "karar_suresi_sn": 20, "karar_degistirme_sayisi": 2, "tiklama_araligi_ms": 800, "onceki_yanlis_sayisi": 1, "ipucu_sayisi": 1, "sahne_no": 12},
    {"seviye": 1, "karar_suresi_sn": 12, "karar_degistirme_sayisi": 1, "tiklama_araligi_ms": 900, "onceki_yanlis_sayisi": 2, "ipucu_sayisi": 0, "sahne_no": 5},
    {"seviye": 2, "karar_suresi_sn": 30, "karar_degistirme_sayisi": 3, "tiklama_araligi_ms": 600, "onceki_yanlis_sayisi": 5, "ipucu_sayisi": 3, "sahne_no": 15},
]


def tahmin(girdiler):
    s = ort.InferenceSession("model/model.onnx", providers=["CPUExecutionProvider"])
    X = np.array([[g[k] for k in OZ] for g in girdiler], dtype=np.float32)
    return [float(v) for v in s.run(["p"], {"girdi": X})[0][:, 0]]


if __name__ == "__main__":
    p = tahmin(GIRDILER)
    if "--yaz" in sys.argv:
        json.dump([{"girdi": g, "p": v} for g, v in zip(GIRDILER, p)],
                  open("tests/parite.json", "w", encoding="utf-8"), indent=2)
        print("yazıldı:", [round(v, 6) for v in p])
    else:
        ref = json.load(open("tests/parite.json", encoding="utf-8"))
        fark = max(abs(r["p"] - v) for r, v in zip(ref, p))
        print(f"en büyük fark: {fark:.2e}")
        sys.exit(0 if fark < TOL else 1)
