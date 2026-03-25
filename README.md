# 🗃️ ML Feature Store

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python)](https://python.org)
[![PySpark](https://img.shields.io/badge/PySpark-3.5-E25A1C?style=flat&logo=apache-spark)](https://spark.apache.org)
[![Redis](https://img.shields.io/badge/Redis-7.x-DC382D?style=flat&logo=redis)](https://redis.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Production ML feature store** — batch computation with PySpark, online serving via Redis, point-in-time correct training datasets, and a Python SDK.

## ✨ Highlights

- ⚡ **Online serving** — Redis-backed sub-millisecond feature retrieval for real-time inference
- 🔄 **Batch computation** — PySpark jobs for large-scale feature engineering with scheduling
- 📅 **Point-in-time correctness** — no data leakage in training datasets via temporal joins
- 🔌 **Python SDK** — `feature_store.get_features(entity_ids, feature_names)` in one line
- 📊 **Feature monitoring** — drift detection, null rates, distribution shifts
- 🗂️ **Feature registry** — centralized metadata store for feature discovery and versioning

## Quick Start

```bash
git clone https://github.com/rutvik29/ml-feature-store
cd ml-feature-store
pip install -r requirements.txt

# Define features
from src.sdk import FeatureStore
fs = FeatureStore()

@fs.feature_view(entity="user_id", ttl_hours=24)
def user_features(user_id: str) -> dict:
    return {"age": ..., "purchase_count_7d": ..., "avg_order_value": ...}

# Retrieve for inference
features = fs.get_features(["user_123", "user_456"], ["age", "purchase_count_7d"])

# Build training dataset
df = fs.get_training_dataset(entity_df, timestamp_col="event_time", features=["age", "purchase_count_7d"])
```

## Architecture

```
Raw Data Sources (S3 / Kafka)
        │
   PySpark Jobs (batch)
        │
   ┌────┴────────────┐
   │  Offline Store  │  ←── Point-in-time correct training data
   │  (Parquet/S3)   │
   └─────────────────┘
        │ materialization
   ┌────┴────────────┐
   │  Online Store   │  ←── Real-time inference (<1ms)
   │  (Redis)        │
   └─────────────────┘
        │
   Feature Registry (PostgreSQL)
```

## License
MIT © Rutvik Trivedi
