"""Bağımlılıksız minimal ONNX yazıcı: p = sigmoid(X @ W + b).
Lojistik regresyon + StandardScaler için yeterlidir (skl2onnx'e alternatif).
Protobuf'u elle kodlar; çıktıyı onnxruntime ile doğrularız (bkz. train.py)."""
import struct
import numpy as np


def _varint(n):
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def _tag(field, wire):
    return _varint((field << 3) | wire)


def _vint(field, n):
    return _tag(field, 0) + _varint(n)


def _bytes(field, b):
    return _tag(field, 2) + _varint(len(b)) + b


def _str(field, s):
    return _bytes(field, s.encode("utf-8"))


def _tensor(name, arr):
    arr = np.asarray(arr, dtype="<f4")
    b = b"".join(_vint(1, d) for d in arr.shape)
    b += _vint(2, 1)  # FLOAT
    b += _str(8, name)
    b += _bytes(9, arr.tobytes())
    return b


def _value_info(name, dims):
    shape = b""
    for d in dims:
        shape += _bytes(1, _str(2, d) if isinstance(d, str) else _vint(1, d))
    tensor_type = _vint(1, 1) + _bytes(2, shape)
    return _str(1, name) + _bytes(2, _bytes(1, tensor_type))


def _node(op, inputs, outputs, name):
    b = b"".join(_str(1, i) for i in inputs)
    b += b"".join(_str(2, o) for o in outputs)
    b += _str(3, name) + _str(4, op)
    return b


def yaz(yol, agirlik, sapma, ozellik_sayisi):
    """agirlik: (n,), sapma: skaler. Girdi 'girdi' [N,n], çıktı 'p' [N,1]."""
    W = np.asarray(agirlik, dtype=np.float32).reshape(ozellik_sayisi, 1)
    B = np.asarray([sapma], dtype=np.float32)
    graph = b""
    graph += _bytes(1, _node("Gemm", ["girdi", "W", "B"], ["z"], "dogrusal"))
    graph += _bytes(1, _node("Sigmoid", ["z"], ["p"], "sigmoid"))
    graph += _str(2, "primer_zorlanma")
    graph += _bytes(5, _tensor("W", W))
    graph += _bytes(5, _tensor("B", B))
    graph += _bytes(11, _value_info("girdi", ["N", ozellik_sayisi]))
    graph += _bytes(12, _value_info("p", ["N", 1]))
    model = _vint(1, 8)  # ir_version
    model += _str(2, "primer-v2")
    model += _bytes(7, graph)
    model += _bytes(8, _str(1, "") + _vint(2, 13))  # opset 13
    with open(yol, "wb") as f:
        f.write(model)
