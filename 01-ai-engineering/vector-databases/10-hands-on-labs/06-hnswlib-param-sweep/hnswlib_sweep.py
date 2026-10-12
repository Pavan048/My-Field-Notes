"""hnswlib recall/latency sweep using the common public MNIST vector subset."""
from pathlib import Path
import sys, time
import numpy as np
import hnswlib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runner import load_data, exact, recall, K

x,q=load_data(10000,100); gt=exact(x,q)
for m in (16,32):
    t=time.perf_counter(); index=hnswlib.Index(space='cosine',dim=x.shape[1])
    index.init_index(max_elements=len(x),ef_construction=100,M=m); index.add_items(x,np.arange(len(x)))
    build=time.perf_counter()-t
    for ef in (20,50,100):
        index.set_ef(max(ef,K)); times=[]; ids=[]
        for v in q:
            t=time.perf_counter(); found,_=index.knn_query(v,k=K); times.append(time.perf_counter()-t); ids.append(found[0])
        print(f'M={m},ef={ef},recall@10={recall(np.asarray(ids),gt):.4f},qps={len(q)/sum(times):.2f},p50_ms={np.percentile(times,50)*1000:.3f},p95_ms={np.percentile(times,95)*1000:.3f},build_s={build:.3f},estimated_index_bytes={x.nbytes+len(x)*m*2*4}')
