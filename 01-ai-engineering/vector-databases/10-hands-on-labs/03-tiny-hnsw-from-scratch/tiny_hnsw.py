"""Small educational HNSW build/search on the shared MNIST-vector experiment."""
from pathlib import Path
import sys, time, heapq, math
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runner import load_data, exact, recall, K, save_plot
import csv

M, EF_CONSTRUCTION, EF_SEARCH = 8, 32, 48

def distance(x,a,b): return 1.0-float(np.dot(x[a],x[b]))

def search_layer(x, graphs, query, entries, layer, ef, upper):
    candidates=[]; best=[]; visited=set()
    for node in entries:
        d=1.0-float(np.dot(query,x[node])); heapq.heappush(candidates,(d,node)); heapq.heappush(best,(-d,-node)); visited.add(node)
    while candidates:
        d,node=heapq.heappop(candidates)
        if len(best)>=ef and d > -best[0][0]: break
        for nb in graphs[layer].get(node,()):
            if nb>=upper or nb in visited: continue
            visited.add(nb); nd=1.0-float(np.dot(query,x[nb]))
            if len(best)<ef or nd < -best[0][0]:
                heapq.heappush(candidates,(nd,nb)); heapq.heappush(best,(-nd,-nb))
                if len(best)>ef: heapq.heappop(best)
    return [(-d,-node) for d,node in sorted(best,reverse=True)]

def build(x):
    rng=np.random.default_rng(12); levels=[]; graphs=[]; entry=None; maxlevel=-1
    for i in range(len(x)):
        level=min(int(-math.log(max(rng.random(),1e-12))/math.log(M)),5)
        levels.append(level)
        while len(graphs)<=level: graphs.append({})
        for layer in range(level+1): graphs[layer][i]=set()
        if entry is None: entry=i; maxlevel=level; continue
        current=entry
        for layer in range(maxlevel,level,-1):
            moved=True
            while moved:
                moved=False; here=1-float(np.dot(x[i],x[current]))
                for nb in graphs[layer].get(current,()):
                    d=1-float(np.dot(x[i],x[nb]))
                    if d<here: current=nb; moved=True; break
        for layer in range(min(level,maxlevel),-1,-1):
            found=search_layer(x,graphs,x[i],[current],layer,EF_CONSTRUCTION,i)
            chosen=[j for _,j in found[:M]]
            for j in chosen:
                graphs[layer][i].add(j); graphs[layer][j].add(i)
                if len(graphs[layer][j])>M:
                    graphs[layer][j]=set(sorted(graphs[layer][j],key=lambda z:distance(x,j,z))[:M])
            if chosen: current=chosen[0]
        if level>maxlevel: entry=i; maxlevel=level
    return graphs,entry,maxlevel

def query(x,graphs,entry,maxlevel,q):
    current=entry
    for layer in range(maxlevel,0,-1):
        moved=True
        while moved:
            moved=False; best=1-float(np.dot(q,x[current]))
            for nb in graphs[layer].get(current,()):
                d=1-float(np.dot(q,x[nb]))
                if d<best: current=nb; moved=True; break
    result=search_layer(x,graphs,q,[current],0,EF_SEARCH,len(x))
    return [i for _,i in result[:K]]

def main():
    x,q=load_data(2000,50); gt=exact(x,q)
    t=time.perf_counter(); graphs,entry,maxlevel=build(x); build_s=time.perf_counter()-t
    times=[]; out=[]
    for v in q:
        t=time.perf_counter(); out.append(query(x,graphs,entry,maxlevel,v)); times.append(time.perf_counter()-t)
    links=sum(len(v) for g in graphs for v in g.values())
    row={"method":"tiny-hnsw-from-scratch", "rows":len(x), "queries":len(q), "recall_at_10":recall(np.asarray(out),gt),
      "qps":len(q)/sum(times), "p50_ms":float(np.percentile(times,50)*1000), "p95_ms":float(np.percentile(times,95)*1000),
      "index_bytes_estimate":x.nbytes+links*4,"build_seconds":build_s}
    result_dir=Path(__file__).resolve().parents[1]/'results'; csvpath=result_dir/'results.csv'
    with csvpath.open('r',newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
    rows.append(row)
    fields=list(dict.fromkeys(key for r in rows for key in r))
    with csvpath.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    save_plot(rows,result_dir/'recall-vs-qps.svg')
    print(f"dataset=MNIST prefix; rows={len(x)}; queries={len(q)}; M={M}; efConstruction={EF_CONSTRUCTION}; efSearch={EF_SEARCH}")
    print(f"recall@10={row['recall_at_10']:.4f}; qps={row['qps']:.2f}; p50_ms={row['p50_ms']:.3f}; p95_ms={row['p95_ms']:.3f}; build_s={build_s:.3f}; estimated_bytes={x.nbytes+links*4}")

if __name__=='__main__': main()
