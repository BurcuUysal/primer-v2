"""Tek komut: python train.py
Sabit tohum, oturum bazlı ayrım, eval kapısı, ONNX üretimi ve doğrulama.
Eşik altındaysa hata koduyla durur ve model.onnx YAZILMAZ."""
import json
import os
import sys

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, recall_score, roc_auc_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler

import onnx_yaz

SEED = 42
KESME = 0.40  # karar kesme noktası (spec.md "Değişiklik kaydı"na bakın)
OZELLIKLER = ["seviye", "karar_suresi_sn", "karar_degistirme_sayisi",
              "tiklama_araligi_ms", "onceki_yanlis_sayisi", "ipucu_sayisi", "sahne_no"]
# spec.md ile aynı eşikler (eğitimden ÖNCE yazıldı):
ESIK = {"recall": 0.70, "f1": 0.65, "roc_auc": 0.75, "onnx_fark_max": 1e-4}


def main():
    df = pd.read_csv("data/oturumlar.csv")
    X, y, g = df[OZELLIKLER].to_numpy(float), df["zorlandi"].to_numpy(int), df["oturum_id"]
    gss = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=SEED)
    tr, te = next(gss.split(X, y, g))

    olcek = StandardScaler().fit(X[tr])
    clf = LogisticRegression(max_iter=1000, random_state=SEED).fit(olcek.transform(X[tr]), y[tr])
    p = clf.predict_proba(olcek.transform(X[te]))[:, 1]
    tahmin = (p >= KESME).astype(int)
    metrik = {
        "recall": round(float(recall_score(y[te], tahmin)), 4),
        "f1": round(float(f1_score(y[te], tahmin)), 4),
        "roc_auc": round(float(roc_auc_score(y[te], p)), 4),
        "n_egitim": int(len(tr)), "n_test": int(len(te)),
        "pozitif_oran_test": round(float(y[te].mean()), 4),
    }

    # Ölçekleyiciyi ağırlıklara katla: sigmoid(((x-mu)/s)·w + b) = sigmoid(x·(w/s) + b - Σ w·mu/s)
    w = clf.coef_[0] / olcek.scale_
    b = float(clf.intercept_[0] - np.sum(clf.coef_[0] * olcek.mean_ / olcek.scale_))
    os.makedirs("model", exist_ok=True)
    gecici = "model/.model.onnx.tmp"
    onnx_yaz.yaz(gecici, w, b, len(OZELLIKLER))

    import onnxruntime as ort
    oturum = ort.InferenceSession(gecici, providers=["CPUExecutionProvider"])
    onnx_p = oturum.run(["p"], {"girdi": X[te].astype(np.float32)})[0][:, 0]
    fark = float(np.max(np.abs(onnx_p - p)))
    metrik["onnx_sklearn_max_fark"] = fark

    hatalar = []
    if metrik["recall"] < ESIK["recall"]: hatalar.append(f"recall {metrik['recall']} < {ESIK['recall']}")
    if metrik["f1"] < ESIK["f1"]: hatalar.append(f"f1 {metrik['f1']} < {ESIK['f1']}")
    if metrik["roc_auc"] < ESIK["roc_auc"]: hatalar.append(f"roc_auc {metrik['roc_auc']} < {ESIK['roc_auc']}")
    if fark >= ESIK["onnx_fark_max"]: hatalar.append(f"ONNX farkı {fark:.2e} >= {ESIK['onnx_fark_max']}")
    print(json.dumps(metrik, indent=2, ensure_ascii=False))
    if hatalar:
        os.remove(gecici)
        print("EVAL KAPISI: BAŞARISIZ ->", "; ".join(hatalar), file=sys.stderr)
        sys.exit(1)

    os.replace(gecici, "model/model.onnx")
    config = {
        "surum": "v2.0",
        "girdi_adi": "girdi", "cikti_adi": "p",
        "ozellikler": OZELLIKLER,
        "siniflar": {"0": "zorlanmiyor", "1": "zorlaniyor"},
        "karar_esikleri": {"derin_anlatim_ve_ipucu": 0.60, "kisa_anlatim": 0.30},
        "karar_kesme_noktasi": KESME,
        "kabul_esikleri": ESIK,
        "metrikler": metrik,
        "veri": {"dosya": "data/oturumlar.csv", "satir": int(len(df)),
                 "kaynak_dagilimi": df["kaynak"].value_counts().to_dict()},
        "egitim": {"model": "LogisticRegression", "random_state": SEED, "olcekleyici": "StandardScaler (ağırlıklara katlı)"},
    }
    with open("model/config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print("EVAL KAPISI: GEÇTİ -> model/model.onnx ve model/config.json yazıldı")


if __name__ == "__main__":
    main()
