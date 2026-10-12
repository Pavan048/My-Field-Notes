# FAISS parameter sweep lab

> **TL;DR:** Sweep a compact IVF or HNSW parameter grid and plot the recall/latency frontier against exact ground truth.

```mermaid
flowchart LR
 GT[exact neighbors] --> S[sweep settings]
 S --> R[recall@k]
 S --> L[latency distribution]
 R --> P[quality-speed frontier]
 L --> P
```

**Visual takeaway:** The diagram shows the main data or decision path; labels are conceptual, not performance guarantees.

## Field notes

Pin `faiss-cpu`, NumPy, dataset ID, and hardware. Use a public dataset such as a documented ANN-Benchmarks corpus when available; store downloaded data outside the repo and record its checksum. Sweep one search parameter at a time after fixing the build. Report build time, index bytes, recall, p50/p95/p99, concurrency, and exact-ground-truth settings.

## Run this experiment

The data source is the public [MNIST dataset](https://ann-benchmarks.com/), downloaded from the [dataset mirror](https://storage.googleapis.com/cvdf-datasets/mnist/). The runner uses a fixed prefix of train images and test images, flattens 28×28 pixels to 784 dimensions, and L2-normalizes vectors for cosine ranking. This is a small reproducible teaching workload, not a production benchmark.

**Experiment:** The pinned FAISS CPU index compares exact Flat with IVF-Flat at nprobe 2, 8, and 16.

```powershell
python ../runner.py --rows 2000 --queries 50 --methods faiss
```

Measured output and the generated [CSV](../results/results.csv) and [recall/QPS plot](../results/recall-vs-qps.svg) are shared across the runnable labs. Values are machine-specific; see the parent [lab results table](../README.md).

