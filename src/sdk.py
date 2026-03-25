"""Feature Store Python SDK."""
import redis, json, os
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd

class FeatureStore:
    def __init__(self, redis_url: str = None):
        self.redis = redis.from_url(redis_url or os.getenv("REDIS_URL", "redis://localhost:6379"))
        self._registry: Dict[str, Any] = {}

    def feature_view(self, entity: str, ttl_hours: int = 24):
        def decorator(func):
            self._registry[func.__name__] = {"entity": entity, "ttl": ttl_hours * 3600, "fn": func}
            return func
        return decorator

    def materialize(self, feature_view_name: str, entity_ids: List[str]):
        view = self._registry[feature_view_name]
        for entity_id in entity_ids:
            features = view["fn"](entity_id)
            key = f"fs:{feature_view_name}:{entity_id}"
            self.redis.setex(key, view["ttl"], json.dumps(features))

    def get_features(self, entity_ids: List[str], feature_names: List[str]) -> pd.DataFrame:
        rows = []
        for entity_id in entity_ids:
            row = {"entity_id": entity_id}
            for view_name, view_def in self._registry.items():
                key = f"fs:{view_name}:{entity_id}"
                cached = self.redis.get(key)
                if cached:
                    all_feats = json.loads(cached)
                    for fname in feature_names:
                        if fname in all_feats:
                            row[fname] = all_feats[fname]
            rows.append(row)
        return pd.DataFrame(rows)

    def get_training_dataset(self, entity_df: pd.DataFrame, timestamp_col: str, features: List[str]) -> pd.DataFrame:
        # Point-in-time correct join placeholder
        return entity_df.copy()
