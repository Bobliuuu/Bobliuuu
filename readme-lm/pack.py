#!/usr/bin/env python3
"""Pack lm_k6.npz as int8 (+fp16 row scales) base64 into README.md between markers."""
import sys, io, re, base64, numpy as np
src, readme = sys.argv[1], sys.argv[2]
Z = np.load(src); out = {"emb": Z["emb"].astype(np.float16), "voc": Z["voc"].astype(np.uint8), "k": Z["k"]}
for n in ("0", "1", "2"):
    w = Z["w" + n]; s = np.abs(w).max(1, keepdims=True) / 127 + 1e-12
    out["q" + n] = np.round(w / s).astype(np.int8); out["s" + n] = s.astype(np.float16)
    out["b" + n] = Z["b" + n].astype(np.float16)
buf = io.BytesIO(); np.savez(buf, **out)
b64 = base64.b64encode(buf.getvalue()).decode()
lines = "\n".join(b64[i:i + 120] for i in range(0, len(b64), 120))
block = ("<!--LM-WEIGHTS-START-->\n<details><summary>The model: int8 weights, %d KB (this README <b>is</b> the model)</summary>\n\n```\n%s\n```\n\n</details>\n<!--LM-WEIGHTS-END-->" % (len(b64) // 1024, lines))
r = open(readme).read()
if "<!--LM-WEIGHTS-START-->" in r:
    r = re.sub(r"<!--LM-WEIGHTS-START-->.*<!--LM-WEIGHTS-END-->", lambda m: block, r, flags=re.S)
else:
    r = r.rstrip() + "\n\n" + block + "\n"
open(readme, "w").write(r); print(len(b64), "b64 bytes;", len(r.encode()), "README bytes")
