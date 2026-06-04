"""
cohort_analysis.py
──────────────────
K-Means regional demand segmentation.

Features (standardised with StandardScaler before clustering)
──────────────────────────────────────────────────────────────
  avg_demand    — average monthly demand per region
  cv_demand     — coefficient of variation (σ/μ) — demand volatility
  growth_proxy  — total demand / average demand — relative growth signal

Clusters (k=3)
──────────────
  HIGH_DEMAND_STABLE    — high volume, low CV  → JIT replenishment, tight ROP
  MED_DEMAND_GROWING    — moderate volume, growing → invest in capacity
  LOW_DEMAND_VOLATILE   — low volume, high CV  → safety stock buffers, frequent review

Cluster labels are assigned post-hoc by avg_demand rank
(highest avg_demand = HIGH_DEMAND_STABLE).
"""

import pandas as pd
import numpy as np
from sklearn.cluster      import KMeans
from sklearn.preprocessing import StandardScaler
from config import N_COHORTS, RANDOM_SEED

COHORT_LABELS = ["HIGH_DEMAND_STABLE", "MED_DEMAND_GROWING", "LOW_DEMAND_VOLATILE"]


def cohort_analysis(demand_df: pd.DataFrame) -> pd.DataFrame:
    """
    Segment regions into demand-profile cohorts using K-Means.

    Parameters
    ----------
    demand_df : pd.DataFrame  Monthly region demand data

    Returns
    -------
    pd.DataFrame  One row per region with cluster assignment + features
    """
    # ── Build region-level feature matrix ─────────────────────────────────────
    features = (
        demand_df.groupby("region")
        .agg(
            avg_demand  =("demand", "mean"),
            std_demand  =("demand", "std"),
            total_demand=("demand", "sum"),
        )
        .reset_index()
    )
    features["cv_demand"]    = (features["std_demand"] / features["avg_demand"]).round(4)
    features["growth_proxy"] = (features["total_demand"] / features["avg_demand"]).round(4)

    # ── Standardise and cluster ───────────────────────────────────────────────
    X        = features[["avg_demand", "cv_demand", "growth_proxy"]].values
    X_scaled = StandardScaler().fit_transform(X)

    kmeans = KMeans(n_clusters=N_COHORTS, random_state=RANDOM_SEED, n_init=10)
    features["cluster_id"] = kmeans.fit_predict(X_scaled)

    # ── Assign human-readable labels by avg_demand rank ──────────────────────
    cluster_means = (
        features.groupby("cluster_id")["avg_demand"]
        .mean()
        .sort_values(ascending=False)
    )
    label_map = {cid: COHORT_LABELS[rank] for rank, cid in enumerate(cluster_means.index)}
    features["cohort"] = features["cluster_id"].map(label_map)
    features = features.drop(columns=["cluster_id"]).round(2)

    print(f"[COHORTS]    {N_COHORTS} segments identified:")
    for cohort, grp in features.groupby("cohort"):
        regions = grp["region"].tolist()
        print(f"             {cohort}: {regions} "
              f"(avg demand={grp['avg_demand'].mean():.0f}, "
              f"avg CV={grp['cv_demand'].mean():.3f})")
    return features
