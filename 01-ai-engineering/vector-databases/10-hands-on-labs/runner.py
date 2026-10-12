"""Reproducible small-prefix ANN experiments on public MNIST image vectors."""
from __future__ import annotations

import argparse
import csv
import gzip
import heapq
import math
import struct
import time
import urllib.request
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
URLS = {
    "train": "https://storage.googleapis.com/cvdf-datasets/mnist/train-images-idx3-ubyte.gz",
    "test": "https://storage.googleapis.com/cvdf-datasets/mnist/t10k-images-idx3-ubyte.gz",
}
K = 10


def load_data(n: int, nq: int):
    DATA.mkdir(parents=True, exist_ok=True)
    arrays=[]
    for split,url in URLS.items():
        path=DATA/f"{split}-images-idx3-ubyte.gz"
        if not path.exists():
            print(f"Downloading public MNIST {split} image vectors to {path}")
            urllib.request.urlretrieve(url,path)
        with gzip.open(path,"rb") as f:
            magic,count,rows,cols=struct.unpack(">IIII",f.read(16))
            if magic != 2051: raise ValueError(f"invalid IDX image file: {path}")
            raw=f.read()
        arrays.append(np.frombuffer(raw,dtype=np.uint8).reshape(count,rows*cols).astype(np.float32))
    x=arrays[0][:n]
    q=arrays[1][:nq]
    # Normalize pixels so angular retrieval has consistent score semantics.
    x /= np.maximum(np.linalg.norm(x, axis=1, keepdims=True), 1e-12)
    q /= np.maximum(np.linalg.norm(q, axis=1, keepdims=True), 1e-12)
    return x, q


def topk_scores(scores, k=K):
    ids = np.argpartition(-scores, k - 1)[:k]
    return ids[np.argsort(-scores[ids])]


def exact(x, q, k=K):
    return np.stack([topk_scores(x @ query, k) for query in q])


def recall(result, truth, k=K):
    return float(np.mean([len(set(a[:k]) & set(b[:k])) / k for a, b in zip(result, truth)]))


def kmeans(x, k, steps=8, seed=17):
    rng = np.random.default_rng(seed)
    centers = x[rng.choice(len(x), k, replace=False)].copy()
    for _ in range(steps):
        labels = np.argmax(x @ centers.T, axis=1)
        sums = np.zeros_like(centers)
        counts = np.bincount(labels, minlength=k)
        np.add.at(sums, labels, x)
        keep = counts > 0
        centers[keep] = sums[keep] / counts[keep, None]
        centers[keep] /= np.maximum(np.linalg.norm(centers[keep], axis=1, keepdims=True), 1e-12)
        if not np.all(keep): centers[~keep] = x[rng.choice(len(x), np.sum(~keep), replace=False)]
    return centers


def timed_eval(name, search, truth, build_seconds, index_bytes, dataset, n, nq):
    rows, times = [], []
    for q in dataset:
        t0 = time.perf_counter(); rows.append(search(q)); times.append(time.perf_counter() - t0)
    r = recall(np.asarray(rows), truth)
    elapsed = sum(times)
    return {"method": name, "rows": n, "queries": nq, "recall_at_10": r,
            "qps": nq / elapsed if elapsed else float("inf"),
            "p50_ms": float(np.percentile(times, 50) * 1000),
            "p95_ms": float(np.percentile(times, 95) * 1000),
            "index_bytes_estimate": int(index_bytes), "build_seconds": build_seconds}


def do_flat(x, q, truth):
    t0 = time.perf_counter()
    rows = exact(x, q)
    build = time.perf_counter() - t0
    return timed_eval("exact-flat", lambda v: topk_scores(x @ v), truth, build, x.nbytes, q, len(x), len(q))


def do_ivf(x, q, truth):
    t0 = time.perf_counter(); centers = kmeans(x, 32)
    assignment = np.argmax(x @ centers.T, axis=1)
    lists = [np.flatnonzero(assignment == i) for i in range(len(centers))]
    build = time.perf_counter() - t0
    rows_out=[]
    for probes in (2, 8, 16):
        def search(v, p=probes):
            selected = topk_scores(centers @ v, p)
            ids = np.concatenate([lists[i] for i in selected if len(lists[i])])
            return ids[topk_scores(x[ids] @ v)]
        rows_out.append(timed_eval(f"ivf-flat-nprobe-{probes}", search, truth, build,
                          x.nbytes + centers.nbytes + x.shape[0]*8, q, len(x), len(q)))
    return rows_out


def do_pq(x, q, truth):
    # Five 5-D subspaces, each encoded by one of 32 centroids: 5 bytes/vector.
    m, ks, subd = 16, 32, x.shape[1] // 16
    t0=time.perf_counter(); codebooks=[]; codes=np.empty((len(x),m),dtype=np.uint8)
    for j in range(m):
        block=x[:,j*subd:(j+1)*subd]
        cb=kmeans(block,ks,steps=6,seed=17+j); codebooks.append(cb)
        codes[:,j]=np.argmax(block @ cb.T,axis=1)
    build=time.perf_counter()-t0
    codebooks=np.asarray(codebooks)
    def search(v):
        lut=np.stack([codebooks[j] @ v[j*subd:(j+1)*subd] for j in range(m)])
        scores=np.zeros(len(x),dtype=np.float32)
        for j in range(m): scores += lut[j,codes[:,j]]
        return topk_scores(scores)
    return timed_eval("pq-adc-m16-k32", search, truth, build,
                      codes.nbytes + codebooks.nbytes, q, len(x), len(q))


def do_faiss(x, q, truth):
    import faiss
    rows=[]
    t0=time.perf_counter(); index=faiss.IndexFlatIP(x.shape[1]); index.add(x)
    build=time.perf_counter()-t0
    # Exact FAISS baseline validates metric/data semantics before IVF approximation.
    times=[]; ids=[]
    for v in q:
        t0=time.perf_counter(); _,found=index.search(v.reshape(1,-1),K); times.append(time.perf_counter()-t0); ids.append(found[0])
    elapsed=sum(times)
    rows.append({"method":"faiss-flat", "rows":len(x), "queries":len(q), "recall_at_10":recall(np.asarray(ids),truth),
      "qps":len(q)/elapsed, "p50_ms":float(np.percentile(times,50)*1000), "p95_ms":float(np.percentile(times,95)*1000),
      "index_bytes_estimate":len(faiss.serialize_index(index)), "build_seconds":build})
    nlist=32; t0=time.perf_counter(); ivf=faiss.IndexIVFFlat(faiss.IndexFlatIP(x.shape[1]),x.shape[1],nlist,faiss.METRIC_INNER_PRODUCT)
    ivf.train(x); ivf.add(x); build=time.perf_counter()-t0
    for probes in (2,8,16):
        ivf.nprobe=probes; times=[]; ids=[]
        for v in q:
            t0=time.perf_counter(); _,found=ivf.search(v.reshape(1,-1),K); times.append(time.perf_counter()-t0); ids.append(found[0])
        elapsed=sum(times)
        rows.append({"method":f"faiss-ivf-nprobe-{probes}","rows":len(x),"queries":len(q),"recall_at_10":recall(np.asarray(ids),truth),
          "qps":len(q)/elapsed,"p50_ms":float(np.percentile(times,50)*1000),"p95_ms":float(np.percentile(times,95)*1000),
          "index_bytes_estimate":len(faiss.serialize_index(ivf)),"build_seconds":build})
    return rows


def do_hnswlib(x,q,truth):
    import hnswlib
    t0=time.perf_counter(); index=hnswlib.Index(space="cosine",dim=x.shape[1]); index.init_index(max_elements=len(x),ef_construction=100,M=16)
    index.add_items(x,np.arange(len(x))); build=time.perf_counter()-t0
    rows=[]
    for ef in (20,50,100):
        index.set_ef(max(ef,K)); times=[]; ids=[]
        for v in q:
            t0=time.perf_counter(); found,_=index.knn_query(v,k=K); times.append(time.perf_counter()-t0); ids.append(found[0])
        elapsed=sum(times); rows.append({"method":f"hnswlib-ef-{ef}","rows":len(x),"queries":len(q),"recall_at_10":recall(np.asarray(ids),truth),
          "qps":len(q)/elapsed,"p50_ms":float(np.percentile(times,50)*1000),"p95_ms":float(np.percentile(times,95)*1000),
          "index_bytes_estimate":len(x)*x.shape[1]*4 + len(x)*16*2*4,"build_seconds":build})
    return rows


def do_filtered(x,q):
    rng=np.random.default_rng(21); tenant=rng.integers(0,20,size=len(x))
    out=[]
    for qi,v in enumerate(q[:50]):
        eligible=np.flatnonzero(tenant == qi % 20)
        out.append(topk_scores(x[eligible] @ v))
    truth=np.stack([np.flatnonzero(tenant == qi % 20)[r] for qi,r in enumerate(out)])
    rows=[]
    for depth in (10,100,500):
        result=[]; under=0; times=[]
        for qi,v in enumerate(q[:50]):
            t0=time.perf_counter()
            global_ids=topk_scores(x @ v, min(depth,len(x)))
            kept=[i for i in global_ids if tenant[i] == qi % 20][:K]
            under += len(kept)<K
            result.append(kept)
            times.append(time.perf_counter()-t0)
        r=float(np.mean([len(set(a)&set(b))/K for a,b in zip(result,truth)]))
        rows.append({"method":f"postfilter-depth-{depth}","rows":len(x),"queries":50,"recall_at_10":r,
          "qps":len(times)/sum(times),"p50_ms":float(np.percentile(times,50)*1000),"p95_ms":float(np.percentile(times,95)*1000),"index_bytes_estimate":x.nbytes,"build_seconds":0,
          "underfilled_queries":under})
    return rows


def save_plot(rows,out):
    points=[r for r in rows if r.get("qps") and float(r["qps"])>0 and r.get("recall_at_10") is not None]
    w,h=900,480; left,right,top,bottom=90,30,35,70
    xmin=0; xmax=max(float(r["qps"]) for r in points)*1.08; ymin=0; ymax=1.02
    def xy(r): return left+(w-left-right)*float(r["qps"])/xmax, h-bottom-(h-top-bottom)*float(r["recall_at_10"])/ymax
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
         '<rect width="100%" height="100%" fill="white"/>',
         f'<path d="M {left} {top} V {h-bottom} H {w-right}" fill="none" stroke="#263238"/>',
         f'<text x="{w/2}" y="{h-20}" text-anchor="middle" font-family="sans-serif">Queries per second (higher is faster)</text>',
         f'<text x="22" y="{h/2}" transform="rotate(-90 22 {h/2})" text-anchor="middle" font-family="sans-serif">Recall@10</text>']
    for i in range(6):
        y=top+(h-top-bottom)*i/5; val=1-i/5
        svg.append(f'<path d="M {left} {y:.1f} H {w-right}" stroke="#e0e0e0"/><text x="{left-10}" y="{y+4:.1f}" text-anchor="end" font-family="sans-serif" font-size="12">{val:.1f}</text>')
    for r in points:
        x,y=xy(r); label=r['method']
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#1565c0"/><text x="{x+8:.1f}" y="{y-6:.1f}" font-family="sans-serif" font-size="11">{label}</text>')
    svg.append('</svg>'); out.write_text('\n'.join(svg),encoding='utf-8')


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--rows',type=int,default=10000); ap.add_argument('--queries',type=int,default=100)
    ap.add_argument('--methods',default='flat,ivf,pq,faiss,hnswlib,filtered'); args=ap.parse_args()
    x,q=load_data(args.rows,args.queries); t0=time.perf_counter(); truth=exact(x,q); gt_s=time.perf_counter()-t0
    rows=[]
    for method in args.methods.split(','):
        method=method.strip()
        if method=='flat': rows.append(do_flat(x,q,truth))
        elif method=='ivf': rows.extend(do_ivf(x,q,truth))
        elif method=='pq': rows.append(do_pq(x,q,truth))
        elif method=='faiss': rows.extend(do_faiss(x,q,truth))
        elif method=='hnswlib': rows.extend(do_hnswlib(x,q,truth))
        elif method=='filtered': rows.extend(do_filtered(x,q))
        else: raise ValueError(f'unknown method: {method}')
    out=HERE/'results'; out.mkdir(exist_ok=True)
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with (out/'results.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader(); writer.writerows(rows)
    save_plot(rows,out/'recall-vs-qps.svg')
    print(f'dataset=MNIST train/test image vectors (public); metric=cosine after L2 normalization; rows={len(x)}; queries={len(q)}; d={x.shape[1]}; exact_gt_seconds={gt_s:.3f}')
    print('method,recall@10,qps,p50_ms,p95_ms,index_bytes_estimate')
    for r in rows: print(f"{r['method']},{r['recall_at_10']:.4f},{r.get('qps')},{r.get('p50_ms')},{r.get('p95_ms')},{r['index_bytes_estimate']}")
    print(f'outputs={out}')

if __name__=='__main__': main()
